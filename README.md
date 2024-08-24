# LPM - LaTeX Project Manager

## Installation

 - Set up your database (e.g mariadb) and provide a user and a database with Permission to create tables inside that database
 - Install nginx and copy the config files found in /Installation/files into their place
 - execute installApi.sh, installConfigs.sh, installLibraries.sh
 - execute "npm run build --prod" in /Application, then copy the compiled application into the webdirectory for nginx to serve

## Needed software:

### Python packages to be installed in the virtualenv
 - configparser
 - mysql-connector
 - flask
 - uwsgi

 ### Tipps:

 - Setting up database and user:
    
    Create database and user
    CREATE DATABASE LPMdb;
    CREATE USER 'LPMdbUSER'@'localhost' IDENTIFIED BY '...';
    GRANT ALL PRIVILEGES ON LPMdb.* TO 'LPMdbUSER'@'localhost';
    FLUSH PRIVILEGES;
