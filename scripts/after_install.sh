#!/bin/bash
HOME=/home/ubuntu
PATH=$HOME/app
BACKUP=$HOME/backup

cp $BACKUP/.env $PATH
cp $BACKUP/json $PATH/app/json
rm -rf $PATH/*
