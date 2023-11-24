# SPDX-FileCopyrightText: Copyright (c) 2022 esp32beans@gmail.com
#
# SPDX-License-Identifier: MIT

""" Convert Wii Nunchuk to USB mouse with two buttons. """

import array
import math
import board
import adafruit_nunchuk
import usb_hid
import neopixel

from adafruit_hid.mouse import Mouse

JS_DEBUG = 0
DEADZONE = 5
X_SPEED = 3.0   # Also known as sensitivity
Y_SPEED = 3.0   # Also known as sensitivity



def handle():
    
    mouse = Mouse(usb_hid.devices)
    
    nc = adafruit_nunchuk.Nunchuk(i2c)

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


pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.01

while True:
    try:
            
        i2c = board.I2C()
        i2c.try_lock()
        i2c.scan()
        i2c.unlock()
                
        handle()
        
    except RuntimeError as e:
        pixel.fill((255, 0, 0))
        print("Error: ", e)
        
    except OSError as e:
        pixel.fill((0, 0, 255))
        print("Error: ", e)
