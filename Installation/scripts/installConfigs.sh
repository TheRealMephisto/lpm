#!/bin/bash

mkdir -p /etc/lpm/config
rm -r /etc/lpm/config/*
cp -R ../../Backend/config/* /etc/lpm/config/