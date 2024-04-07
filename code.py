# SPDX-FileCopyrightText: Copyright (c) 2023 Leon Anavi <leon@anavi.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

""" Convert Wii Nunchuk to a USB Joystick or a USB mouse with two buttons. """

import array
import math
import time
import board
import busio
import adafruit_nunchuk
import digitalio
from hid_joystick import Joystick
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.digitalio import DigitalIO
from adafruit_seesaw.pwmout import PWMOut
import usb_hid
import neopixel
import json

from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

JS_DEBUG = 0
DEADZONE = 5
X_SPEED = 3.0   # Also known as sensitivity
Y_SPEED = 3.0   # Also known as sensitivity

def handleMouse():
    
    mouse = Mouse(usb_hid.devices)
    
    # Experiment with mouse acceleration/sensitivity. For small deflections of the
    # joystick move the mouse slowly. For larger deflections, move the mouse
    # faster. The look up table is computed outside the main loop to avoid calling
    # time consuming the math function on every loop. The X and Y tables use the
    # same values but could use different values.
    X_ACCEL = array.array('B')
    Y_ACCEL = array.array('B')
    
    for x in range(128):
        if x <= DEADZONE:
            # Dead zone around center to fix drift.
            # Joysticks do not alway report (x=0,y=0) when the stick is released.
            # When this happens the cursor moves slowly when it should not be moving.
            # This is sometimes called drifting. Drifting is fixed by treating
            # joystick values between -DEADZONE to +DEADZONE as 0. If the cursor is
            # still drifting increase the value of DEADZONE.
            X_ACCEL.append(0)
            Y_ACCEL.append(0)
        else:
            X_ACCEL.append(int((math.pow(x/127.0, X_SPEED) * 127) + 0.5))
            Y_ACCEL.append(int((math.pow(x/127.0, Y_SPEED) * 127) + 0.5))
            if x > 0:
                if X_ACCEL[x] == 0:
                    X_ACCEL[x] = 1
                if Y_ACCEL[x] == 0:
                    Y_ACCEL[x] = 1
        if JS_DEBUG:
            print(x, X_ACCEL[x], Y_ACCEL[x])

    # The index into this array goes from 0 to 128 so make the last element
    # have the same value as the element 127.
    X_ACCEL.append(X_ACCEL[127])
    Y_ACCEL.append(Y_ACCEL[127])

    LAST_JS_X = 255
    LAST_JS_Y = 255

    while True:
        x, y = nc.joystick
        if JS_DEBUG:
            js_x = x
            js_y = y
        # Map the range 0 to 255 from the joystick to -127 to 128 for the mouse.
        x = x - 127
        y = -(y - 127)
        if JS_DEBUG:
            signed_x = x
            signed_y = y

        if x < 0:
            x = -X_ACCEL[abs(x)]
        else:
            x = X_ACCEL[abs(x)]

        if y < 0:
            y = -Y_ACCEL[abs(y)]
        else:
            y = Y_ACCEL[abs(y)]
        if JS_DEBUG:
            sensitivity_x = x
            sensitivity_y = y

        if JS_DEBUG and (LAST_JS_X != js_x or LAST_JS_Y != js_y):
            print(js_x, js_y, signed_x, signed_y, sensitivity_x, sensitivity_y)
            LAST_JS_X = js_x
            LAST_JS_Y = js_y
        mouse.move(x, y)

        if nc.buttons.C:
            mouse.press(Mouse.LEFT_BUTTON)
        else:
            mouse.release(Mouse.LEFT_BUTTON)
        if nc.buttons.Z:
            mouse.press(Mouse.RIGHT_BUTTON)
        else:
            mouse.release(Mouse.RIGHT_BUTTON)
        
        pixel.fill((0, 255, 0))

def handleKeyboard():

    kbd = Keyboard(usb_hid.devices)

    # Experiment with mouse acceleration/sensitivity. For small deflections of the
    # joystick move the mouse slowly. For larger deflections, move the mouse
    # faster. The look up table is computed outside the main loop to avoid calling
    # time consuming the math function on every loop. The X and Y tables use the
    # same values but could use different values.
    X_ACCEL = array.array('B')
    Y_ACCEL = array.array('B')

    for x in range(128):
        if x <= DEADZONE:
            # Dead zone around center to fix drift.
            # Joysticks do not alway report (x=0,y=0) when the stick is released.
            # When this happens the cursor moves slowly when it should not be moving.
            # This is sometimes called drifting. Drifting is fixed by treating
            # joystick values between -DEADZONE to +DEADZONE as 0. If the cursor is
            # still drifting increase the value of DEADZONE.
            X_ACCEL.append(0)
            Y_ACCEL.append(0)
        else:
            X_ACCEL.append(int((math.pow(x/127.0, X_SPEED) * 127) + 0.5))
            Y_ACCEL.append(int((math.pow(x/127.0, Y_SPEED) * 127) + 0.5))
            if x > 0:
                if X_ACCEL[x] == 0:
                    X_ACCEL[x] = 1
                if Y_ACCEL[x] == 0:
                    Y_ACCEL[x] = 1
        if JS_DEBUG:
            print(x, X_ACCEL[x], Y_ACCEL[x])

    # The index into this array goes from 0 to 128 so make the last element
    # have the same value as the element 127.
    X_ACCEL.append(X_ACCEL[127])
    Y_ACCEL.append(Y_ACCEL[127])

    last_x_key = None
    last_y_key = None

    while True:
        x, y = nc.joystick
        if JS_DEBUG:
            js_x = x
            js_y = y
        # Map the range 0 to 255 from the joystick to -127 to 128 for the mouse.
        x = x - 127
        y = -(y - 127)

        if x < 0:
            x = -X_ACCEL[abs(x)]
        else:
            x = X_ACCEL[abs(x)]

        if y < 0:
            y = -Y_ACCEL[abs(y)]
        else:
            y = Y_ACCEL[abs(y)]
        if JS_DEBUG:
            sensitivity_x = x
            sensitivity_y = y

        if 10 < x:
            last_x_key = Keycode.RIGHT_ARROW
            kbd.press(Keycode.RIGHT_ARROW)
        elif -10 > x:
            last_x_key = Keycode.LEFT_ARROW
            kbd.press(Keycode.LEFT_ARROW)
        elif None != last_x_key:
            kbd.release(last_x_key)
            last_x_key = None

        if 10 < y:
            last_y_key = Keycode.DOWN_ARROW
            kbd.press(Keycode.DOWN_ARROW)
        elif -10 > y:
            last_y_key = Keycode.UP_ARROW
            kbd.press(Keycode.UP_ARROW)
        elif None != last_y_key:
            kbd.release(last_y_key)
            last_y_key = None

        if nc.buttons.C:
            kbd.press(Keycode.A)
        else:
            kbd.release(Keycode.A)

        if nc.buttons.Z:
            kbd.send(Keycode.B)
        else:
            kbd.release(Keycode.B)

        pixel.fill((0, 255, 0))

def handleJoystick():

    js = Joystick(usb_hid.devices)

    while True:
        x, y = nc.joystick
        y = 255 - y
        js.move_joysticks(x, y)

        if nc.buttons.Z:
            js.press_buttons(1)
        else:
            js.release_buttons(1)
        if nc.buttons.C:
            js.press_buttons(2)
        else:
            js.release_buttons(2)

        pixel.fill((0, 255, 0))

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.01

while True:
    try:
            
        i2c = board.I2C()
        i2c.try_lock()
        i2c.scan()
        i2c.unlock()

        nc = adafruit_nunchuk.Nunchuk(i2c)

        with open("config.json") as f:
            data = f.read()
            config = json.loads(data)
            if "joystick" == config["type"]:
                handleJoystick()
            elif "mouse" == config["type"]:
                handleMouse()
            elif "keyboard" == config["type"]:
                handleKeyboard()

    except RuntimeError as e:
        pixel.fill((255, 0, 0))
        print("Error: ", e)
        
    except OSError as e:
        pixel.fill((0, 0, 255))
        print("Error: ", e)
