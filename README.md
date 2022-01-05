# doorlock
Raspberry Pi project that will lock/unlock a door attached to a servo.
This is done through:
- A Python Flask web application
  - Google accounts used for authentication (only allows certain accounts)
- Two background scripts that monitor for lock/unlock button presses

# My Setup
Here is my setup:
- Raspberry Pi OS Lite
- Servo connected to `__`
- Push button connected to `__` to lock the door
- Push button connected to `__` to unlock the door
- Server running on port `39420` (see `gunicorn.conf.py`)

# General Pi Setup
- `setup-server.sh` will set up doorlock to run in the background
- Use ssh key login and change the default password for `pi`
- Port forward the desired port (I used `39420`) to your pi
  - Use a static ip! I'd recommend making a DHCP reservation
- Don't port forward for ssh unless you need to
- You can switch to wifi with `sudo raspi-config`
