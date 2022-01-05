#!/bin/bash
set -e

if (( $EUID != 0 ))
then
    echo "Needs to be run as root. Try 'sudo $0'"
    exit 1
fi

NEW_USER=doorlock

apt update
apt -y install supervisor gunicorn
useradd -m -G gpio $NEW_USER
runuser -l $NEW_USER -c 'git clone https://github.com/GregoryConrad/doorlock'
runuser -l $NEW_USER -c 'pip3 install -r doorlock/requirements.txt'

DOORLOCK_PATH=/home/$NEW_USER/doorlock
cat << EOF >> /etc/supervisor/supervisord.conf
[program:doorlock]
command=gunicorn doorlock:app
directory=$DOORLOCK_PATH
user=$NEW_USER
autostart=true
autorestart=true
redirect_stderr=true

[program:lock-door-monitor]
command=python3 servo_control.py lock_monitor
directory=$DOORLOCK_PATH
user=$NEW_USER
autostart=true
autorestart=true
redirect_stderr=true

[program:unlock-door-monitor]
command=python3 servo_control.py unlock_monitor
directory=$DOORLOCK_PATH
user=$NEW_USER
autostart=true
autorestart=true
redirect_stderr=true
EOF

echo "Please create the 4 required files (see $DOORLOCK_PATH/README.md) in $DOORLOCK_PATH/"
echo "After the 4 files are created, reboot the Raspberry Pi"
