#!/bin/bash

echo "Installing needed dependencies for CityVisualizer1.0 tool"

sudo apt-get update
sudo apt-get install python3
sudo apt-get install apache2
sudo service httpd start

echo "Configuring execution permissions"

chmod +x code/generate_city.sh

echo "Moving needed files to their locations"

sudo mv html/ /var/www/
