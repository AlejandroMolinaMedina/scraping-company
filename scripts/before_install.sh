
#!/bin/bash
HOME=/home/ubuntu
PATH=$HOME/app

cd $PATH
mkdir $HOME/backup
#Hacer respaldo db
#pg_dump -h 127.0.0.1 -U admin -d analizertest -f ./backup/respaldo.sql
cp .env $HOME/backup
cp -rf $PATH/app/json $HOME/backup
rm -rf app/*