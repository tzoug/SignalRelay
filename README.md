# signal-telegram-forwarding

## Signal Setup

### Install Java

#### On x64

```bash
# Install openjdk-21-jre
sudo apt install openjdk-21-jre

# Export JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
```

#### On arm/aarch64

https://sdkman.io/install

```bash
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk version
sdk install java 21.0.2-oracle

# Add the following to your ~/.bashrc
export JAVACMD=/home/USERNAME/.sdkman/candidates/java/current/bin/java
export JAVA_HOME=~/.sdkman/candidates/java/current
export PATH=$JAVA_HOME/bin:$PATH
export JAVA_LIBRARY_PATH="-Djava.library.path=/usr/java/packages/lib"

# Make sure this is at the end

#THIS MUST BE AT THE END OF THE FILE FOR SDKMAN TO WORK!!!
export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"
. "$HOME/.cargo/env"
```

### Install Signal-CLI

#### On x64
Unpack the `tar.gz`

```bash
# Navigate to the /signal-cli-files director and execute
sudo tar -xvf signal-cli-0.13.2.tar.gz -C /opt
```

#### On arm/aarch64

*If you're on an arm/aarch64 based system you need to modify the `libsignal-client.jar` with the proper `libsignal_jni.so`*

Pre-built files can be found here: https://github.com/exquo/signal-libs-build/releases. Make sure to get the current version. Check the version number of `/opt/signal-cli-0.13.2/lib/libsignal-client-X.Y.Z.jar/`

```bash
# Unpack the `tar.gz` with
tar -xvf libsignal_jni.so-v0.40.1-aarch64-unknown-linux-gnu.tar.gz

# Remove the existing libsignal_jni.so
zip -d /opt/signal-cli-0.13.2/lib/libsignal-client-0.40.1.jar libsignal_jni.so

# Add the new one that was just extracted
zip /opt/signal-cli-0.13.2/lib/libsignal-client-0.40.1.jar libsignal_jni.so
```

#### Common Steps

```bash
# Add signal-cli to /usr/local/bin
sudo ln -sf /opt/signal-cli-0.13.2/bin/signal-cli /usr/local/bin/

# Install dependencies (if you will be scanning the QR code when linking a device)
sudo apt install libpng-dev
sudo apt install qrencode
export PATH=$PATH:/usr/bin/

# Link the device
signal-cli link -n "device name" | tee >(xargs -L 1 qrencode -t utf8)
```


### Setup dbus

*All files that should be copied can also be found in the `signal-cli-master/data/` directory.*

*See https://github.com/AsamK/signal-cli/wiki/DBus-service#system-bus*

#### Modify and copy necessary service files

```bash
# 1. Replace <YOUR_USERNAME> in org.asamk.Signal.conf and copy it to /etc/dbus-1/system.d/
cp signal-cli-files/org.asamk.Signal.conf /etc/dbus-1/system.d/

# 2. Copy org.asamk.Signal.service to /usr/share/dbus-1/system-services/
cp signal-cli-files/org.asamk.Signal.service /usr/share/dbus-1/system-services/

# 3. Replace <YOUR_USERNAME> in signal-cli.service and copy it to /etc/systemd/system/
cp signal-cli-files/signal-cli.service /etc/systemd/system/
```

#### Run the service

```bash
# Reload the daemon
systemctl daemon-reload

# Enable the service
sudo systemctl enable signal-cli.service

# Start the service
sudo systemctl start signal-cli.service

# View the status of the service (should be Active)
systemctl status signal-cli.service

# To stop the service
systemctl stop signal-cli.service
```

## Python Setup

Install Python (if not already installed): `sudo apt install python3`

### Install Dependencies

```bash
pip install pydbus
pip install python-telegram-bot

# If you run into a "externally-managed-environment" error (commonly on Raspbery Pi), add the --break-system-packages flag at the end of the pip command.
# Ex: pip install pydbus --break-system-packages
```

### Setup .env

1. Navigate to the `src/` directory.
2. Copy the contents of `.env_template.txt` to a new file called `.env`.
3. Specify the values for those fields.
4. Run `python3 telegram.chat_id.py` to get the chat ID of the Telegram bot.
    - Alternatively, you can go to `https://api.telegram.org/bot<YourBOTToken>/getUpdates`
5. Add the chat ID from **step 4** to `TELEGRAM_CHAT_ID` field in the `.env` file.
6. Get the Signal groupID using the `signal-cli listGroups` command.
    - Copy the ID to the `SIGNAL_GROUP_ID` field in the `.env` file.

### Run Python Script

#### Using the shell script

The shell script starts the signal-cli.service and runs the python file.

*The following paths a relative to the home dir.*

1. Run `./signal-telegram-forwarding/helper/start_receiver.sh`
    - If it's not executable use `chmod +x ~/signal-telegram-forwarding/helper/start_receiver.sh`
2. Enter the password to start the services

*You can stop the service you can run `./signal-telegram-forwarding/helper/stop_receiver.sh`*

---

#### Manually

6. Run `python3 receive.py`
   - Can also be done in `tmux`
       - Install tmux (if not done already): `sudo apt install tmux`
       - Create a new session: `tmux new -s session_name`
       - Attach to a session: `tmux attach -d -t session_name` or `tmux attach` (if only 1 session)
       - Leave the session (still runs): `CTRL + B` then `D`
       - List sessions: `tmux ls`
       - Kill a session: `tmux kill-session -t session_name`


## Useful Links

- https://github.com/AsamK/signal-cli/
- https://github.com/AsamK/signal-cli/wiki/Quickstart
- https://github.com/AsamK/signal-cli/wiki/Linking-other-devices-%28Provisioning%29
- https://github.com/AsamK/signal-cli/wiki/DBus-service#system-bus
- https://fabiobarbero.eu/posts/signalbot/
- https://github.com/python-telegram-bot/python-telegram-bot
- https://github.com/AsamK/signal-cli/wiki/Provide-native-lib-for-libsignal
- https://github.com/exquo/signal-libs-build/
- https://github.com/exquo/signal-libs-build/releases
