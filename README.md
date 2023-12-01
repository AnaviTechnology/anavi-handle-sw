# ANAVI Handle

[CircuitPython](https://circuitpython.org/) firmware for the open source hardware development board [ANAVI Handle](https://anavi.technology/) which converts Nintendo Wii Nunchuk compatible controllers to USB HID devices such as mouse.

# Dependencies

## Installing to a Connected ANAVI Handle with Circup

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

```
pip3 install circup
```

With circup` installed and your CircuitPython device connected use the following command to install:

```
circup install adafruit_bus_device adafruit_hid adafruit_nunchuk adafruit_seesaw neopixel
```

Or the following command to update an existing version:

```
circup update
```
