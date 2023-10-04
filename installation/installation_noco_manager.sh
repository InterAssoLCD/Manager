#!/bin/bash

# Mise à jour du raspberry
apt update
apt full-upgrade -y

# Installations des services

# => PostgreSQL
apt install postgresql -y
su postgres
createuser pi -P --interactive
psql -c "CREATE DATABASE pi;"
exit

# => Nginx
apt install nginx -y
# rm /var/www/html/index.nginx-debian.html

# => DNSMasq

apt install dnsmasq -y
systemctl stop dnsmasq
cp /etc/dhcpcd.conf /etc/original.dhcpcd.conf
printf "interface wlan0\nstatic ip_address=192.168.255.253/16\n" | tee -a /etc/dhcpcd.conf
mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
printf "interface wlan0\ndhcp-range=192.168.0.2,192.168.253.254,255.255.0.0,12h\n" | tee /etc/dhcpcd.conf

# => HostAPd

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

# => FIN

echo "============"
echo "SSID : NoCo"
echo "PASSWORD : $password"
echo "IP Manager : 192.168.255.253"
echo "============"

printf "faites\nreboot\npour finir l'installation"

