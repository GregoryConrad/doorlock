# doorlock
**Created by Gregory Conrad**

Raspberry Pi project that will lock/unlock a door attached to a servo.
This is done through:
- A Python Flask web application
  - Google accounts used for authentication (with an email whitelist)
- Two background processes that listen to lock/unlock button presses
  - Used as a manual override in case your internet goes down or you don't want to get out your phone

Here it is on my door, configured with a battery backup:
![Final Product](/images/final-product.jpg?raw=true)

# Setup Suggestions
- Raspberry Pi OS Lite
- `setup.sh` to set up doorlock to run in the background
  - Run `sudo /bin/bash -c "$(curl -fsSL https://github.com/GregoryConrad/doorlock/raw/main/setup.sh)"` as the `pi` user to automatically install/configure everything
  - Configures a new `doorlock` user with the necessary permissions
- Files needed for the server:
  - `client_secret.json` for Google OAuth 2
  - `doorlock.json` for all doorlock configuration (see `example-doorlock.json`)
    - `authorizedEmails` is a list of authorized emails
    - `pins` is the GPIO pin mapping
    - `servoMapping` is what position the servo should be in for lock/unlock
      - Useful if your mount has the servo positioned in a certain way
      - Supported values are `max`, `min`, and `mid`
    - `certfile` is for HTTPS (make sure the `doorlock` user has permission to access the file!)
    - `keyfile` is for HTTPS (make sure the `doorlock` user has permission to access the file!)
    - `onStartup` indicates whether the lock should lock or unlock when the pi starts up
      - Useful in case of a power outage
    - `serverPort` is the port the server will run on
    - `ipcPort` is the port the monitor process will listen on
      - You probably don't need to change this
    - `sessionLifetime` is the number of days for a session lifetime
    - `sessionSignKey` is the key to sign sessions with
      - If you omit this field or leave it blank, one will be automatically created for you
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
| ![](/images/shortcut-app.png?raw=true) | ![](/images/lock-shortcut.png?raw=true) | ![](/images/unlock-shortcut.png?raw=true) |

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
    5. Screenshot from Chrome: ![Chrome Devtools Screenshot](/images/get-cookie-devtools.jpeg?raw=true)
