# Native libsignal-client

## Find the correct version

You need to find the correct version needed of the libsignal-client in order to download the correct native build.

- Navigate to the `/lib` directory of you signal-cli installation. 
  - For example: `/opt/signal-cli-0.13.2/lib/`
- Look for the a file called `libsignal-client-VERSION.jar
  - For example: `libsignal-client-0.40.1.jar`

This means that version 0.13.2 of the Signal-Cli uses version 0.40.1 of the libsignal-client.

## Use The Pre-Built Native Build

Pre-built files can be found here: https://github.com/exquo/signal-libs-build/releases. 

Make sure to get the current version. Check the version number of `/opt/signal-cli-0.13.2/lib/libsignal-client-X.Y.Z.jar/`

```bash
# Unpack the `tar.gz` with
tar -xvf libsignal_jni.so-v0.40.1-aarch64-unknown-linux-gnu.tar.gz

# Remove the existing libsignal_jni.so
zip signal-cli-0.13.7/lib/libsignal-client-0.58.0.jar -d '*signal_jni*'

# Add the new one that was just extracted
zip signal-cli-0.13.7/lib/libsignal-client-0.58.0.jar -uj libsignal_jni.so
```
