# NOCO Manager <!-- omit from toc -->

*NoCo Manager* est le serveur central qui permettra de profiter des projets hors ligne (Ticketer, CashLess, ...)

Il a été imaginé pour tourner sur un RaspberryPi 4 (4GB ram / 64GB storage).

## Sommaire <!-- omit from toc -->

## En Bref

NoCo Manager est un serveur central permettant à n'importe qui sur son réseau wifi de profiter des projets complémentaire installés.

Il dispose :

- d'une base de données PostgreSQL utilisées par les différents projets
- d'un DNS local (pour l'accès aux applications web des projets)
- d'un DHCP local (pour faciliter l'utilisation sur des postes clients ex: smartphones, tablettes)
- d'un reverse proxy Nginx pour faire les traitements HTTP

## Installation rapide

> L'installation se fait en tant qu'utilisateur `pi` assurez vous d'avoir les droits SUDO ou ROOT

Vous pouvez utiliser le script [installation_noco_manager.sh](./installation_noco_manager.sh) pour automatiquement installer les services.

Pour cela faites :

```bash

curl https://XXX | sudo bash
```

## Installation Manuelle

> L'installation se fait en tant qu'utilisateur `pi` assurez vous d'avoir les droits SUDO ou ROOT

Avant de procéder au installation des services, vérifier que le raspberry est à jour :

```bash
sudo apt update
sudo apt full-upgrade -y
```

L'installation se fera dans l'ordre suivant :

1. PostgreSQL
2. Nginx
3. Dnsmasq
4. Hostapd

### PostgreSQL

Premièrement il faut installer le service :

```bash
sudo apt install postgresql -y
```

Nous allons ensuite le configurer pour utiliser l'utilisateur `pi` au lieu de `postgres`:

> Attention à bien exécuter les commandes les une après les autres et non en même temps

```bash
sudo su postgres
createuser pi -P --interactive
```

Cette commande va vous demander de remplir quelques informations.

- Créer un mot de passe
- Est-ce que l'utiliateur `pi` doit être superutilisateur répondez **Y**
  
Il ne nous reste plus qu'à créer une base de données pour l'utilisateur `pi`

```bash
psql
```

puis dans l'interface de PostgreSQL

```sql
CREATE DATABASE pi;
```

Vous pouvez ensuite sortir de l'interface de PostgreSQL puis de l'utilisateur postgres :

```bash
exit
exit
```

Maintenant l'utilisateur `pi` peut se connecter facilement à la base de données

### NGINX

L'installation de NGINX est simple, il suffit de faire la commande suivante :

```bash
sudo apt install nginx -y
```

Normalement vous devriez avoir accès à une page HTML disponible sur votre adresse ip `http://localhost` ou `http://A.B.C.D`

Cette page est la page par défaut de Nginx. Le Manager n'en a pas besoin alors nous allons la supprimer

```bash
sudo rm /var/www/html/index.nginx-debian.html
```

Vous devriez avoir désormais une page indiquant `403 Forbidden`.

### DNSMasq

Installation du package:

```bash
sudo apt install dnsmasq -y
sudo systemctl stop dnsmasq
```

Sauvegardons la configuration de base au cas où:

```bash
sudo cp /etc/dhcpcd.conf /etc/original.dhcpcd.conf
```

En suite nous ajoutons la configuration de l'interface wifi

```bash
sudo printf "interface wlan0\nstatic ip_address=192.168.255.253/16\n" | sudo tee -a /etc/dhcpcd.conf
```

Configurons maintenant le DHCP

```bash
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig 
sudo printf "interface wlan0\ndhcp-range=192.168.0.2,192.168.253.254,255.255.0.0,12h\n" | sudo tee /etc/dnsmasq.conf
```

Les ips du réseau `192.168.254.0/24` sont réservées aux services NoCo (les “TPE“ du Cashless par exemple)

### Hostapd

```bash
sudo apt install hostapd -y
sudo systemctl stop hostapd
```

Création du mot de passe du wifi :

```bash
password="VOTRE_MOT_DE_PASSE"
```

Ajout de la configuration

```bash
cat << EOF | sudo tee /etc/hostapd/hostapd.conf
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
```

### Fin

## Utilisation
