#!/bin/bash
cd ../../Application
npm install file-saver
npm run build --prod
cp -R dist/Application/* /var/www/LPM/