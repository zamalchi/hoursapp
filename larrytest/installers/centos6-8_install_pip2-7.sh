#!/usr/bin/env bash

sudo yum install -y epel-release
wget https://ius.io/GettingStarted/ | rpm -i
sudo yum install python27-pip
sudo pip2.7 install --upgrade pip
sudo pip2.7 install markdown
sudo pip2.7 install Crypto
