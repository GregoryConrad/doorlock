#!/bin/bash

# Preliminary setup & check(s)
set -e
if (( $EUID != 0 ))
then
    echo "Needs to be run as root. Try 'sudo $0'"
    exit 1
fi

# Add needed system packages
apt update
apt -y install git supervisor gunicorn python3-pip python3-pigpio
systemctl enable pigpiod

# Application specific setup
NEW_USER=doorlock
APPLICATION_PATH=/home/$NEW_USER/doorlock
useradd -m -G gpio $NEW_USER
runuser -l $NEW_USER -c "git clone https://github.com/GregoryConrad/doorlock $APPLICATION_PATH"
runuser -l $NEW_USER -c "pip3 install -r $APPLICATION_PATH/requirements.txt"
cat << EOF >> /etc/supervisor/supervisord.conf
[include]
files=$APPLICATION_PATH/config/supervisor.conf
EOF

# Finalization
printf "\n\n"
echo "Please configure the needed files in $APPLICATION_PATH/config in accordance with $APPLICATION_PATH/README.md"
echo "After configuration is complete, reboot the Raspberry Pi"
