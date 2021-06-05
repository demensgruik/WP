# WP

Wordpress_Launcher
Version : 1.0

Developped by : C.Chanal

Release date : 01 04 2021

Contexte :
Ce script est écrit en Python 3.
Le script permet d’installer et effectuer une configuration de base d’un wordpress.
Cela comprend également la création de la base de données mysql et du user de connexion.
Une fois l’installation effectuée, le site de base est accessible.
http://localhost:80/nomduprojet

Avant l’exécution du script, un certain nombre de prérequis sont nécessaires. Ils sont principalement déjà préinstallés, une vérification est donc a faire ainsi qu’un update du système et de ses composants pour avoir la dernière version.

Prérequis :

### Librairies
Sur DEBIAN
Mettre à jour les packages déjà installés
sudo apt-get update
sudo apt-get upgrade
installer les packages suivants :
wget dnsutils curl
libapache2-mod-php
ELinks

apache2
php-mysqlnd php-fpm php-json
php php-opcache php-cli php-gd php-curl

### INSTALL MYSQL DEBIAN

wget https://dev.mysql.com/downloads/repo/apt/ https://dev.mysql.com/get/mysql-apt-config_0.8.17-1_all.deb
sudo dpkg -i mysql-apt-config*
Faire ok et installer par defaut mysql 8.0
Mettre ensuite à jour les packages une nouvelle fois
sudo apt update

### installer mysql-server 
sudo apt-get install mysql-server
entrer le mot de passe root
choisir l’authentification forte => STRONG

Vérifier l’état du server mysql :
systemctl status mysql.service
si pas en automatique le mettre de la façon suivante :
systemctl enable mysql.service

###Modifier le mot "root" de mysql
Le mot de passe a déjà été défini lors de l’installation. Cependant, si vous souhaitez le reconfigurer, faire d’autres configurations etc … il faut lancer
sudo mysql_secure_installation

les prompts suivant vont apparaitre :
répondre comme suit :
Change the password for root? – Press y and change root password
Remove anonymous users? Press y
Disallow root login remotely? Press y
Remove test database and access to it? y
Reload privilege tables now? Press y

### autorisation firewall
Ne pas oublier, sur votre firewall, d’ouvrir les ports http, https

Utilisation :

Copier le script wp-launcher.py dans /var/www/html

Modifier la ligne 
'EXEC':" -uroot -pAZERTYUI --host=localhost -f -e '",
AZERTYUI doit être remplacé par le mot de passe root du système

Aller dans /var/www/html
wp-launcher.py <Nom_Projet> <Password> <VotreMail>
Attention, le mot de passe doit être un minimum complexe ou le user ne pourra pas se créer dans mysql.

License :
WordPress is free software, and is released under the terms of the GPL(GNU General Public License) version 2 or (at your option) any later version. 

