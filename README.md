# SignalRelay

SignalRelay is a tool designed to forward Signal messages to various messaging platforms, starting with Telegram and with plans to expand to more messaging apps in the future. This README provides comprehensive instructions on setting up Signal-Cli, configuring the destination app (such as Telegram), and running SignalRelay effectively.

## Table of Contents
- [Setting up Signal-Cli](#setting-up-signal-cli)
    - [Install Signal-Cli](#install-signal-cli)
    - [Linking devices](#linking-devices)
    - [Configure D-Bus](#configure-d-bus)
- [Setting up the destination](#setting-up-the-destination)
    - [Telegram](#telegram)
    - More on the way...
- [Running SignalRelay](#running-signalrelay)
    - [Install Dependencies](#install-dependencies)
    - [Setup .env File](#setup-env-file)
    - [Run signal_relay.py](#run-signal_relaypy)


## Setting Up Signal-Cli

SignalRelay is built using [Signal-Cli](https://github.com/AsamK/signal-cli).

### Install Signal-CLI

Follow the [Prerequisites](https://github.com/AsamK/signal-cli/wiki/Quickstart#prerequisites) and [Installation](https://github.com/AsamK/signal-cli/wiki/Quickstart#installation) sections of the Signal-Cli quickstart guide.

You can also add Signal-Cli to your `/bin` directory.
```bash
# You must change the ~/signal-cli/ path to the path where you unpacked the release.
sudo ln -sf ~/signal-cli/bin/signal-cli /usr/local/bin/
```

If you're trying to install the Signal-Cli on an architecture other than amd64, you need to also replace the `libsignal-client-X.XX.X.jar` with the native one. You can follow the [libsignal-client wiki](/wiki/libsignal-client_setup.md).

*Note that SignalRelay was tested on version 0.13.2 of Signal-Cli.*

### Linking Devices

The easient way to link a device is with a QR code. This command will output a QR code in the terminal that can then be scanned with the Signal mobile app (Settings -> Linked devices -> + button).

*You can find more info on the Signal-Cli [linking](https://github.com/AsamK/signal-cli/wiki/Linking-other-devices-%28Provisioning%29) wiki.*

```bash
# Install dependencies
sudo apt install libpng-dev
sudo apt install qrencode

# Link a new device
signal-cli link -n "device name" | tee >(xargs -L 1 qrencode -t utf8)
```

### Configure D-Bus

You will need to modify the files found in the `SignalRelay/signal-cli-files` directory and copy them to the proper locations.

*All files that should be edited/copied can also be found in the [data directory](https://github.com/AsamK/signal-cli/tree/master/data) of the Signal-Cli repo.*

*See the [Signal-Cli D-Bus wiki](https://github.com/AsamK/signal-cli/wiki/DBus-service#system-bus) for additional information.*

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

# You can also stop or view the status of the service with the following commands.
sudo systemctl stop signal-cli.service
sudo systemctl status signal-cli.service
```

## Setting Up The Destination

In this section you will set up the destination where you want the Signal messages to get forwarded. You can skip to app that you want.

### Telegram

You can follow the [Telegram Wiki](/wiki/telegram_setup.md) to easily setup your Telegram bot.


## Running SignalRelay

### Install Dependencies

- Install Python
- Install necessary Python libraries

```bash
pip install pydbus

# And necessary destination library
# For example if you're using Telegram as a destination:
pip install python-telegram-bot
```

### Setup .env File

- Copy the contents of `src/.env_template` to a new file in the `config/` directory.
- Specify the values for those fields.

In order to get the ID of the Signal group you can execute:
```
signal-cli -u "phoneNumber" listGroups
```
*Sometimes there are group IDs that have `null` as a name. Usually, the names appear once a message is received in that group. You might need to run this command after receiving a message in a specific group.*

### Run signal_relay.py

```bash
# Run normally
python3 signal_relay.py path_to_env

# Run as a process
nohup python3 -u signal_relay.py path_to_env > path_to_log_file &
```

## Useful Links

- [Signal-Cli Github](https://github.com/AsamK/signal-cli/)
- [Signal-Cli Quickstart](https://github.com/AsamK/signal-cli/wiki/Quickstart)
- [Signal-Cli Linking](https://github.com/AsamK/signal-cli/wiki/Linking-other-devices-%28Provisioning%29)
- [Signal-Cli D-Bus](https://github.com/AsamK/signal-cli/wiki/DBus-service#system-bus)
- [Signal Bot Guide](https://fabiobarbero.eu/posts/signalbot/)
- [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [Signal-Cli Native builds for libsignal](https://github.com/AsamK/signal-cli/wiki/Provide-native-lib-for-libsignal)
- [Signal libs](https://github.com/exquo/signal-libs-build/)
