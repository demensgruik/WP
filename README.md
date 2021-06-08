# WP

Wordpress_Launcher
Version : 1.0

Developped by : CCL

Release date : 05 2021

### Contexte :
Ce script est écrit en Python 3.
L'environnement testé et détaillé dans la procédure ci-dessous est CENTOS.
Le script permet d’installer et effectuer une configuration de base d’un wordpress.
Cela comprend également la création de la base de données mysql et du user de connexion.
Une fois l’installation effectuée, le site de base est accessible avant d'approfondir la configuration.
http://localhost:80/nomduprojet

Avant l’exécution du script, un certain nombre de prérequis sont nécessaires. Ils sont principalement déjà préinstallés, une vérification est donc a faire ainsi qu’un update du système et de ses composants pour avoir les dernières versions.

### Prérequis :

### Librairies
Sur CENTOS
>dnf install wget bind-utils curl
>rpm -Uvh https://repo.mysql.com/mysql80-community-release-el8-1.noarch.rpm
>sed -i '/enbaled=1/enabled=0' /etc/yum.repos.d/mysql-community-repo
>dnf repolist enabled

>dnf install httpd 
>dnf install php-mysqlnd php-fpm php-json
>dnf install php php-opcache php-cli php-gd php-curl
>systemctl start httpd
>systemctl enable httpd


### Installer MYSQL

>yum --enablerepo=mysql80-community install mysql mysql-server mysql-libs
>systemctl enable mysqld.service
>systemctl start mysqld.service
  ## Modifier le mot "root" de mysql
>sudo mysql_secure_installation
Change the password for root? – Press y and change root password
Remove anonymous users? Press y
Disallow root login remotely? Press y
Remove test database and access to it? y
Reload privilege tables now? Press y

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
firewall-cmd --permanent --zone=public --add-service=http
firewall-cmd --permanent --zone=public --add-service=https
firewall-cmd --reload

### Utilisation :
Copier le script wp-launcher.py dans /var/www/html
si besoin le rendre éxécutable

Modifier la ligne 
'EXEC':" -uroot -pAZERTYUI --host=localhost -f -e '",
AZERTYUI doit être remplacé par le mot de passe root MYSQL => attention a bien indiquer un mot de passe complexe ou le user ne pourra pas se créer dans mysql.

Lancer dans /var/www/html
wp-launcher.py <Nom_Projet> <Password> <VotreMail>

### changement des droits :
chown -R apache:apache /var/www/html/[nom_projet_wordpress]

### License :
WordPress is free software, and is released under the terms of the GPL(GNU General Public License) version 2 or (at your option) any later version. 
