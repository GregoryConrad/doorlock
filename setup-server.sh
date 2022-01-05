#!/bin/bash
set -e

if (( $EUID != 0 ))
then
    echo "Needs to be run as root. Try 'sudo $0'"
    exit 1
fi

NEW_USER=doorlock

apt update
apt install python3 python3-rpi.gpio python3-pip supervisor
# FIXME not sure which packages above are already installed
pip3 install gunicorn
useradd -m -G gpio $NEW_USER
runuser -l $NEW_USER -c 'git clone https://github.com/GregoryConrad/doorlock'
runuser -l $NEW_USER -c 'pip3 install -r doorlock/requirements.txt'

DOORLOCK_PATH=/home/$NEW_USER/doorlock
cat << EOF >> /etc/supervisor/supervisord.conf
[program:doorlock]
command=/usr/local/bin/gunicorn doorlock:app -c $DOORLOCK_PATH/gunicorn.conf.py
directory=$DOORLOCK_PATH
user=$NEW_USER
autostart=true
autorestart=true
redirect_stderr=true
EOF

echo "Rebooting in 10 seconds (CTRL-C to cancel)..."
sleep 10
reboot
