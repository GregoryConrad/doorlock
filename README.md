# doorlock
**Created by Gregory Conrad**

Raspberry Pi project that will lock/unlock a door attached to a servo.
This is done through:
- A Python Flask web application
  - Google accounts used for authentication (with an email whitelist)
- Two background processes that monitor for lock/unlock button presses

# Server Setup Suggestions
- Raspberry Pi OS Lite
- `setup-server.sh` to set up doorlock to run in the background
  - Configures a new `doorlock` user with the necessary permissions
- GPIO pins (see `servo_control.py`)
  - Servo: `17`
  - Lock door push button: `5`
  - Unlock door push button: `13`
- Files needed for the server:
  - `client_secret.json` for Google OAuth 2
  - `authorized_emails.txt` for email whitelisting (with one authorized email per line)
  - `server.crt` for HTTPS
    - You can run the following command (replacing `your-domain` as appropriate) if you are using Let's Encrypt
    - `ln -s /etc/letsencrypt/live/your-domain/fullchain.pem server.crt`
  - `server.key` for HTTPS
    - You can run the following command (replacing `your-domain` as appropriate) if you are using Let's Encrypt
    - `ln -s /etc/letsencrypt/live/your-domain/privkey.pem server.key`
- Server running on port `39420` (see `gunicorn.conf.py`)
- Use ssh key login and change the default password for `pi`
- Port forward the needed port to your pi
  - Use a static ip! I'd recommend making a DHCP reservation
  - Don't port forward for ssh unless you need to
