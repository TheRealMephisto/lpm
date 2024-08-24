#!/bin/bash

mkdir -p /etc/lpm/API
rm -r /etc/lpm/API/*
cp ../../Backend/API/* /etc/lpm/API/ #  might still have to chmod in that directory!
cp ../files/LPM_API.service /etc/systemd/system/

apt-get install python3-venv
cd /etc/lpm/API
python3 -m venv LPM_API
source LPM_API/bin/activate
pip install wheel uwsgi flask mysql-connector