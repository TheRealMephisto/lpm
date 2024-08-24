#!/bin/bash

./installConfigs.sh
./installLibraries.sh
./installApplication.sh
sudo nginx -s reload
systemctl stop LPM_API.service
systemctl start LPM_API.service