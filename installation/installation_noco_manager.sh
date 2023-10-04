#!/bin/bash

# Mise à jour du raspberry
echo "== Mise à jour=="

apt update
apt full-upgrade -y

# Installations des services

# => PostgreSQL
echo "== Installation de POSTGRESQL=="
apt install postgresql -y
echo "Création de l'utilisateur PI dans PostgreSQL"
sudo -u postgres createuser pi -P --interactive
sudo -u postgres psql -c "CREATE DATABASE pi;"



# => Nginx
echo "== Installation de NGINX=="
apt install nginx -y
# rm /var/www/html/index.nginx-debian.html

# => DNSMasq
echo "== Installation de DNSMasq =="
apt install dnsmasq -y
systemctl stop dnsmasq
cp /etc/dhcpcd.conf /etc/original.dhcpcd.conf
printf "interface wlan0\nstatic ip_address=192.168.255.253/16\n" | tee -a /etc/dhcpcd.conf
mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
printf "interface wlan0\ndhcp-range=192.168.0.2,192.168.253.254,255.255.0.0,12h\n" | tee /etc/dhcpcd.conf

# => HostAPd
echo "== Installation de HostAPd =="
apt install hostapd -y
systemctl stop hostapd

read -p "Mot de passe du wifi : " password
cat << EOF | tee /etc/hostapd/hostapd.conf
interface=wlan0
bridge=br0
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
ssid=NoCo
wpa_passphrase=$password
EOF

echo 'DAEMON_CONF="/etc/hostapd/hostapd.conf"' >> /etc/default/hostapd

systemctl unmask hostapd.service
systemctl enable hostapt.service

# => FIN
echo "== Fin de l'Installation=="
echo "============"
echo "SSID : NoCo"
echo "PASSWORD : $password"
echo "IP Manager : 192.168.255.253"
echo "============"

printf "faites\nreboot\npour finir l'installation"

