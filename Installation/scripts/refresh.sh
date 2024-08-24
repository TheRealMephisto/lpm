#!/bin/bash
./installConfigs.sh
./installLibraries.sh
./setupDatabase.sh
cd ../../DataExtraction
./extract.sh
cd ../Installation/scripts