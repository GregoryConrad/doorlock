#!/bin/bash
set -e

if (( $EUID != 0 ))
then
    echo "Needs to be run as root. Try 'sudo $0'"
    exit 1
fi

NEW_USER=doorlock

apt update
apt -y install git supervisor gunicorn python3-pip python3-pigpio
systemctl enable pigpiod
useradd -m -G gpio $NEW_USER
DOORLOCK_PATH=/home/$NEW_USER/doorlock
runuser -l $NEW_USER -c "git clone https://github.com/GregoryConrad/doorlock $DOORLOCK_PATH"
runuser -l $NEW_USER -c "pip3 install -r $DOORLOCK_PATH/requirements.txt"

cat << EOF >> /etc/supervisor/supervisord.conf
[program:doorlock-server]
command=gunicorn server:app
directory=$DOORLOCK_PATH
user=$NEW_USER
autostart=true
autorestart=true
redirect_stderr=true

[program:doorlock-monitor]
command=python3 monitor.py
directory=$DOORLOCK_PATH
user=$NEW_USER
autostart=true
autorestart=true
redirect_stderr=true
EOF

echo "Please create the 2 required files (see $DOORLOCK_PATH/README.md) in $DOORLOCK_PATH/"
echo "After the 2 files are created, reboot the Raspberry Pi"
