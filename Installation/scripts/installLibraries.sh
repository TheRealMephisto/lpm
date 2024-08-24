#!/bin/bash

mkdir -p /etc/lpm/libraries
rm -r /etc/lpm/libraries/*
cp -R ../../Backend/libraries/* /etc/lpm/libraries/