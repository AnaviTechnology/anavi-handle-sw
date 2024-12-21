# ANAVI Handle Improved


# Changes

- **Adjust sensitivity:** Hold both buttons for a few seconds, then turn the nunchuk left or right to change mouse sensitivity

- **Bugfixes:** nunchuk used to break after a while; mouse would only move in positive x or y directions

- **Scrolling:** tap both buttons at the same time to enter **SCROLL MODE**. The original creators did not use the accelerometer, but after looking thru the original Nintendo specs, I was able to hook this up to scrolling.


# Rest of info:

[CircuitPython](https://circuitpython.org/) firmware for the open source hardware development board [ANAVI Handle](https://anavi.technology/) which converts Nintendo Wii Nunchuk compatible controllers to USB HID devices such as mouse.

ANAVI Handle lets you easily connect Nintendo Wii Nunchuk-compatible controller to any USB-equipped personal computer (PC). It is equipped with [Seeed Studio’s XIAO RP2040 module](https://www.seeedstudio.com/XIAO-RP2040-v1-0-p-5026.html?utm_source=github&utm_medium=ANAVI&utm_campaign=Handle) that provides a USB-C connector and a Raspberry Pi RP2040 microcontroller.

[Stay tuned for the upcoming crowdfunding campaign of ANAVI Handle on Crowd Supply. Subscribe now to receive notifications about news and stock updates.](https://www.crowdsupply.com/anavi-technology/anavi-handle). For more details please visit https://anavi.technology/

# Hardware

ANAVI Handle is an open source hardware project designed with [KiCad](https://www.kicad.org/). ou can access [all hardware schematics on GitHub](https://github.com/AnaviTechnology/anavi-handle).

# Dependencies

## Installing to a Connected ANAVI Handle with Circup

Make sure that you have ``circup`` installed in your Python environment. On Ubuntu 24.04 you can setup a virtual environment for Python3 as follows:

```
sudo apt update
sudo apt install python3-pip
sudo apt install python3-virtualenv
sudo apt install python3.12-venv
python3 -m venv test_env ~/env
source ~/env/bin/activate
```

Install ``circup`` with the following command if necessary:

```
pip3 install circup
```

With ``circup`` installed and your CircuitPython device connected use the following command to install:

```
circup install adafruit_bus_device adafruit_hid adafruit_nunchuk adafruit_seesaw neopixel
```

Or the following command to update an existing version:

```
circup update
```
