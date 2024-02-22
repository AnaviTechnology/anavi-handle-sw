# ANAVI Handle

[CircuitPython](https://circuitpython.org/) firmware for the open source hardware development board [ANAVI Handle](https://anavi.technology/) which converts Nintendo Wii Nunchuk compatible controllers to USB HID devices such as mouse.

ANAVI Handle lets you easily connect Nintendo Wii Nunchuk-compatible controller to any USB-equipped personal computer (PC). It is equipped with [Seeed Studio’s XIAO RP2040 module](https://www.seeedstudio.com/XIAO-RP2040-v1-0-p-5026.html?utm_source=github&utm_medium=ANAVI&utm_campaign=Handle) that provides a USB-C connector and a Raspberry Pi RP2040 microcontroller.

[Stay tuned for the upcoming crowdfunding campaign of ANAVI Handle on Crowd Supply. Subscribe now to receive notifications about news and stock updates.](https://www.crowdsupply.com/anavi-technology/anavi-handle). For more details please visit https://anavi.technology/

# Hardware

ANAVI Handle is an open source hardware project designed with [KiCad](https://www.kicad.org/). ou can access [all hardware schematics on GitHub](https://github.com/AnaviTechnology/anavi-handle).

# Dependencies

## Installing to a Connected ANAVI Handle with Circup

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

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
