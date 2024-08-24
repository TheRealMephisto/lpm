#!/bin/bash
./installAPI.sh
./installConfigs.sh
./installLibraries.sh
./installApplication.sh
./setupDatabase.sh
systemctl start LPM_API.sercice
systemctl enable LPM_API.service