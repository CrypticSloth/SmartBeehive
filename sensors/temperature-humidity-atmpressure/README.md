## Activating i2c
First need to activate i2c on raspberry pi using raspi-config:
https://pi3g.com/enabling-and-checking-i2c-on-the-raspberry-pi-using-the-command-line-for-your-own-scripts/

Check if i2c is active (NOTE: 1 means False):
`sudo raspi-config nonint get_i2c`

If it returns 1, then run the below to activate i2c:
`sudo raspi-config nonint do_i2c 0` 

## Checking i2c addresses
To check what addresses are active we can use the i2cdetect command.

If not installed, first install using `sudo apt-get install i2c-tools`

Then run `i2cdetect -y 1` to check active addresses, where `-y` runs in non interactive mode and `1` specifies the bus

## Wiring
[Raspberry pi Wiring diagram](https://learn.adafruit.com/assets/97130)
