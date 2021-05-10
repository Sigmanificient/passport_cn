#!/usr/bin/env bash

# retrieve selenium server
mkdir server
cd server/
wget https://selenium-release.storage.googleapis.com/3.141/selenium-server-standalone-3.141.59.jar
cd -

# create python venv
python3 -m venv venv/
