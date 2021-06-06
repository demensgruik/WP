#! /usr/bin/python3
# -*- encoding:utf-8 -*-

#####################################################################
# Usage :
        # cd /var/www/html
	# wp-launcher <Nom_Projet> <Password> <VotreMail>
	# open your browser and go to http://localhost/project-name
#Auteur:CCL
#Date: 05.2021
#Révision:
#####################################################################

#LIBRAIRIES

import os
import sys
#
import urllib
from urllib import request
#tester sans lib3 et requsts exceptions
import urllib3
import requests
#insecure => appel url dtectate prob securité et bloquait
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#
import zipfile
#a verifier si commenter
import re

#Déclaration des dictionnaires => nom des dictionnaires
#self.WP
#self.CLI
#self.MYSQL


class WpLauncher(object):

    def __init__(self, argv):
        # Define global variables.
        if(len(argv) == 4):
            self.PROJECT_NAME = argv[1].replace(' ', '-').strip("'\"").lower()
            # USERNAME in mysql database can't be longer than 16 characters.
            self.USER_NAME = self.PROJECT_NAME + "user"
            if(len(self.USER_NAME) > 16):
                self.USER_NAME = self.USER_NAME[0:16]
            self.PWD = argv[2]
            self.MAIL = argv[3]
        else:
            sys.exit(
                "Merci de fournir un nom_projet, "
                + "un mot de passe, et un e-mail.\n"
                + "Usage : $>wp-launcher <Project name> <Password> <Mail>"
            )

        LOCAL_FOLDER = os.getcwd()
        if(os.path.exists(LOCAL_FOLDER + '/' + self.PROJECT_NAME)):
            exit("Folder %s already exists, please select another name."
                % self.PROJECT_NAME)

        # URL et chemin des dictionnaires pour l'installation.
        self.WP = {
            'URL':'https://wordpress.org/latest.zip',
            'ZIP_PATH':'%s/latest.zip' % LOCAL_FOLDER,
            'INSTALL_FOLDER':LOCAL_FOLDER,
            # Addresse des Wordpress API pour le salt.
            'SALT':'https://api.wordpress.org/secret-key/1.1/salt/',
            'CONFIG':'%s/%s/wp-config.php'
                % (LOCAL_FOLDER, self.PROJECT_NAME),
            'CONFIG_LOCAL':'%s/%s/local-config.php'
                % (LOCAL_FOLDER, self.PROJECT_NAME),
            'CONFIG_SALT':'%s/salt.txt' % LOCAL_FOLDER,    
            'CONFIG_SAMPLE':(
                '%s/%s/wp-config-sample.php'
                % (LOCAL_FOLDER, self.PROJECT_NAME)
            )
        }
        # Retrait des errors non necessaire.
        self.CLI = {
            'NO_ERR':" 2> /dev/null",
            'NO_OUT':" > /dev/null"
        }
        # Méthode pour création de la DATABASE
        self.MYSQL = {
            'BIN':'mysql',
            'CREATE_DB':(
                'CREATE DATABASE IF NOT EXISTS `%s`' % self.PROJECT_NAME
            ),
            'EXEC':" -uroot -pAZERTYUI --host=localhost -f -e '",
            'FLUSH':'FLUSH PRIVILEGES',
            'CREATE':(
                'CREATE USER `%s`@`localhost`' % self.USER_NAME
                + 'IDENTIFIED BY "%s"' % self.PWD
            ),
            'GRANT':(
                'GRANT ALL ON `%s`.* TO `%s`@`localhost`'
                % (self.PROJECT_NAME, self.USER_NAME)
            ),
            'USER_MAX_LEN':16
        }
        # Gitignore path.
        self.GIT = {
            'IGNORE':('%s/%s/.git/.gitignore'
                % (LOCAL_FOLDER, self.PROJECT_NAME))
        }

        # Start the installation.
        self.download()
        self.editWPConfig()
        self.createDB()

        sys.stdout.write("Installation de votre projet [%s] est terminé.\n" % self.PROJECT_NAME)
        sys.stdout.flush()
        print ('Vous pouvez maintenant utiliser votre navigateur.\n')
        print (
            'Votre URL est : http://localhost:80/%s/'
            % self.PROJECT_NAME
        )
        print (
                'Voici les identifiants : USER: %s, MDP: %s'
            % (self.USER_NAME, self.PWD)
        )
        print ('Prenez soin de les conserver.\n')
        print ('Ne faites pas le professeur Tournessol.\n')

    def download(self):
        """
        Get de la dernier version wordpress (fr).
        dépot en local sur os.getcwd
        """

        sys.stdout.flush()

        print ( "Download de la dernière version: %s\nVERS : %s" % (self.WP['URL'], self.WP['ZIP_PATH']))
        archive = urllib.request.urlretrieve(
            self.WP['URL'],
            self.WP['ZIP_PATH']
        )
        sys.stdout.write("\n")

        if(archive):
            self.unzip()
        else:
            exit("Downloading failed")

    def unzip(self):
        """
        Unzip de l'archive.
        Delete archive.
        Rename wordpress folder to PROJECT_NAME .
        """
        sys.stdout.write("Extracting/Renaming...")
        archive = zipfile.ZipFile(self.WP['ZIP_PATH'], 'r')
        archive.extractall(self.WP['INSTALL_FOLDER'])

        os.unlink(self.WP['ZIP_PATH'])
        try:
            os.system(
                'mv wordpress %s'
                % self.PROJECT_NAME
                + self.CLI['NO_ERR']
            )
        except OSError as err:
            exit(
                "Echec du renommage : %s/%s already exists !"
                % (self.WP['INSTALL_FOLDER'],self.PROJECT_NAME)
            )

        sys.stdout.write("Done\n")
        sys.stdout.write("\n")

        
    def editWPConfig(self):
        # Get des SALTS from Wordpress API
        # Sauvegarde de ceux-ci dans un objet TXT
        salts = urllib.request.urlopen('https://api.wordpress.org/secret-key/1.1/salt/').read()
        SALTS_LIST = (salts.decode("utf-8")).split('\n')
        with open(self.WP['CONFIG_SALT'], 'w') as filehandle:
            filehandle.write("/** Authentication Unique Keys ans Salts. */\n")
            for saltsitem in SALTS_LIST:
                filehandle.write('%s\n' % saltsitem)
                #file_object.close()

        sys.stdout.write(
            "Edition du wp-config.php avec les salt et les config online.\n"
        )
        # Get actual config file content.
        #try:
         #   configFile = open(self.WP['CONFIG_SAMPLE'], 'r')
         #   config = configFile.readlines()
         #   configFile.close()
        #except IOError:
         #   exit("Can't open %s" % self.WP['CONFIG_SAMPLE'])
        
        # Get salt configuration.
        try:
            saltFile = open(self.WP['CONFIG_SALT'], 'r')
            saltconfig = saltFile.readlines()
            saltFile.close()
        except IOError:
            exit("Can't open %s" % self.WP['CONFIG_SALT'])

        # Début de la confection du fichier config.
        dbConfig = [
            ""
        ]
        beginning = '// ** Réglages MySQL - '
        start = 0
        ending = "define('DB_HOST', 'localhost');"
        end = 0
       
        sys.stdout.write(
            "Edition du wp-config.php"
            + " with user: %s, password: %s ..."
            % (self.USER_NAME, self.PWD)
        )
        localDbConfig = [
            "<?php\n",
            "// ** Réglages MySQL - Récupération des informations. ** //\n",
            "/** Nom de la base de données de WordPress. */\n",
            "define('DB_NAME', '%s');\n" % self.PROJECT_NAME,
            "/** Utilisateur de la base de données MySQL. */\n",
            "define('DB_USER', '%s');\n" % self.USER_NAME,
            "/** Mot de passe de la base de données MySQL. */\n",
            "define('DB_PASSWORD', '%s');\n" % self.PWD,
            "/** Adresse de l'hébergement MySQL. */\n",
            "define('DB_HOST', 'localhost');\n",
            "/** Database charset to use for create DB tables. */\n",
            "define('DB_CHARSET', 'utf8mb4');\n",
            "/** The Database collate type. */\n",
            "define('DB_COLLATE', '');\n",

            "/** WordPress Database Table prefix. */\n",
            "$table_prefix = 'wp_';\n"
           "\n",
            "/** Debugging mode WordPress for Developpers. */\n",
            "define('WP_DEBUG', false);\n",
           "\n",    
           "/* That's all, stop editing! Happy publishing. */\n",
           "/** Absolute path to the WordPress directory. */\n",
           "if ( ! defined( 'ABSPATH' ) ) {\n",
	   "     define( 'ABSPATH', __DIR__ . '/' );\n",
           "}\n",
           "\n", 
           "/** Sets up WordPress vars and included files. */\n",
           "require_once ABSPATH . 'wp-settings.php';\n",
           "\n" 
 
        ]
        try:
            localConfigFile = open(self.WP['CONFIG'], "w")
            localConfigFile.writelines(localDbConfig)
            localConfigFile.writelines(saltconfig)
            localConfigFile.close()
        except IOError:
            exit("Can't save local config.")
        sys.stdout.write("Done\n")
        sys.stdout.write("\n")

        sys.stdout.write(
            "Rajout des informations SALTS et cookies dans wp-config.php.\n"
        )
        sys.stdout.write("Done\n")
        sys.stdout.write("\n")

    def createDB(self):
        """
        Create table wordpress.
        Will fail silently if table already exists
        """
        sys.stdout.write("Creation de la Database et du user MYSQL...\n")
        try:
            result = os.system(
                self.MYSQL['BIN']
                + self.MYSQL['EXEC']
                + self.MYSQL['CREATE_DB'].strip(';')
                + ";'"
            )

            self.createUser()
        except OSError as err:
            exit("Can't create DB")

    def createUser(self):
        """
        Create user wordpress.
        Grant ALL.
        Will fail silently if user already exists.
        """

        def mysqlExec(sql='', noErr=True):
            sql = (
                self.MYSQL['BIN']
                + self.MYSQL['EXEC']
                + sql.strip(';')
                + ";'"
            )
            if(noErr):
                sql += self.CLI['NO_ERR']
            return os.system(sql)

        try:
            create = mysqlExec(self.MYSQL['CREATE'])
            grant = mysqlExec(self.MYSQL['GRANT'])
            if((create + grant) == 0):
                sys.stdout.write("Done\n")
                sys.stdout.write("\n")
            else:
                sys.stdout.write("\n")
        except OSError as err:
            exit("Can't create user")


WpLauncher(sys.argv)
