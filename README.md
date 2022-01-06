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
- Port forward the needed port to your pi
  - Use a static ip! I'd recommend making a DHCP reservation
  - Don't port forward for ssh unless you need to
- Use ssh key login and change the default password for `pi`

# Siri Shortcuts
While you can use doorlock's web interface, you can also use Siri Shortcuts
(there is probably some easy equivalent for Android).
See the below screenshots for reference when creating your own Siri Shortcuts:

| Siri Shortcut Application | Lock Shortcut Example | Unlock Shortcut Example |
| --- | --- | --- |
| ![](/screenshots/shortcut-app.png?raw=true) | ![](/screenshots/lock-shortcut.png?raw=true) | ![](/screenshots/unlock-shortcut.png?raw=true) |

Notes:
- Replace `example.com` with your domain or your Raspberry Pi's static ip (and port if needed)
- Replace `<your-session-here>` with the session in your cookie
  - As configured, sessions expire after 365 days for easier use with automation
    - You'll have to update your automation with the new session id once a year for it to work
    - You can change the expiration time with `app.config["PERMANENT_SESSION_LIFETIME"] = ...` in `doorlock.py`
  - Don't know how to get your session id from your cookie? 
    1. Use your browser's devtools and listen to network requests. Open the index page (e.g. `https://your-raspberry-pi.example.com/`)
    2. Click on the last request made
    3. Scroll to the Request Headers
    4. Your session id will be to the right of `Cookie:`. Paste this as-is into the automation
    5. Screenshot from Chrome: ![Chrome Devtools Screenshot](/screenshots/get-cookie-devtools.jpeg?raw=true)
