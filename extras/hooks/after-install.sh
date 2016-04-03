#!/usr/bin/env bash

# Install libmysqlclient-dev which is used by mysqlclient pip package
sudo apt-get install libmysqlclient-dev -y

# Activate virtual environment
source /home/ubuntu/PuppetEnv/bin/activate
# Resolve dependencies
pip install -r /opt/puppet/requirements.txt
# Deactivate virtual environment
deactivate

sudo ln -s /etc/nginx/sites-available/puppet /etc/nginx/sites-enabled