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

JS_DEBUG = 1
DEADZONE = 10
X_SPEED = 2.0
Y_SPEED = 2.0

def handleMouse():
    mouse = Mouse(usb_hid.devices)
    
    # Take initial readings to establish baseline
    print("Calibrating - hold nunchuk still...")
    baseline_ax = 0
    baseline_ay = 0
    baseline_az = 0
    samples = 0
    
    # Average 10 readings for baseline
    while samples < 10:
        try:
            ax, ay, az = nc.acceleration
            baseline_ax += ax
            baseline_ay += ay
            baseline_az += az
            samples += 1
            time.sleep(0.1)
        except:
            continue
    
    baseline_ax //= 10
    baseline_ay //= 10
    baseline_az //= 10
    
    print(f"Calibrated - Baseline: ({baseline_ax}, {baseline_ay}, {baseline_az})")
    
    # Movement parameters
    ACCEL_THRESHOLD = 60
    ACCEL_SCALE = 0.2
    SCROLL_SCALE = 0.05
    MIN_SCALE = 0.05
    MAX_SCALE = 0.4
    
    # Smoothing parameters
    last_x = 0
    last_y = 0
    smooth_factor = 0.75
    
    # Mode control variables
    scroll_enabled = True  # Start with scroll enabled
    sens_adjust_mode = False
    both_buttons_start = 0
    LONG_PRESS_TIME = 0.5  # Time in seconds to hold both buttons
    
    while True:
        try:
            x, y = nc.joystick
            ax, ay, az = nc.acceleration
            
            # Calculate relative movement from baseline
            delta_ax = ax - baseline_ax
            delta_ay = ay - baseline_ay
            
            # Handle dual button press
            both_pressed = nc.buttons.C and nc.buttons.Z
            if both_pressed:
                if both_buttons_start == 0:  # Just pressed
                    both_buttons_start = time.monotonic()
                elif time.monotonic() - both_buttons_start > LONG_PRESS_TIME:
                    sens_adjust_mode = True
            else:
                if both_buttons_start > 0:  # Just released
                    if time.monotonic() - both_buttons_start <= LONG_PRESS_TIME:
                        scroll_enabled = not scroll_enabled
                        print(f"Scroll {'enabled' if scroll_enabled else 'disabled'}")
                    sens_adjust_mode = False
                both_buttons_start = 0
            
            # Adjust sensitivity if in sens_adjust_mode
            if sens_adjust_mode:
                if abs(delta_ax) > ACCEL_THRESHOLD:
                    adjustment = (delta_ax - (ACCEL_THRESHOLD if delta_ax > 0 else -ACCEL_THRESHOLD)) * 0.0001
                    ACCEL_SCALE = max(MIN_SCALE, min(MAX_SCALE, ACCEL_SCALE + adjustment))
                    print(f"Sensitivity: {ACCEL_SCALE:.3f}")
                pixel.fill((255, 255, 0))  # Yellow for sensitivity adjustment mode
                continue  # Skip other processing while adjusting sensitivity
            
            # Use joystick for mouse movement
            mouse_x = 0
            mouse_y = 0
            
            if abs(x - 128) > DEADZONE:
                mouse_x = int((x - 128) * ACCEL_SCALE)
                mouse_x = int(mouse_x * (1 - smooth_factor) + last_x * smooth_factor)
            else:
                mouse_x = 0
                last_x = 0  # Force reset when returning to center

            if abs(y - 128) > DEADZONE:
                mouse_y = int(-(y - 128) * ACCEL_SCALE)
                mouse_y = int(mouse_y * (1 - smooth_factor) + last_y * smooth_factor)
            else:
                mouse_y = 0
                last_y = 0  # Force reset when returning to center

            last_x = mouse_x if abs(mouse_x) > 0 else 0
            last_y = mouse_y if abs(mouse_y) > 0 else 0
                
            # Use accelerometer for scrolling if enabled
            scroll_y = 0
            if scroll_enabled and abs(delta_ay) > ACCEL_THRESHOLD:
                scroll_y = int(-(delta_ay - (ACCEL_THRESHOLD if delta_ay > 0 else -ACCEL_THRESHOLD)) * SCROLL_SCALE)
            
            if JS_DEBUG:
                print(f"Mouse - Joy: ({x}, {y}) Move: ({mouse_x}, {mouse_y}) Scroll: {scroll_y}")
            
            # Apply movements
            if mouse_x != 0 or mouse_y != 0:
                mouse.move(mouse_x, mouse_y)
            if scroll_y != 0:
                mouse.move(0, 0, scroll_y)
            
            # Handle buttons (only if not both pressed)
            if not both_pressed:
                if nc.buttons.C:
                    mouse.press(Mouse.LEFT_BUTTON)
                else:
                    mouse.release(Mouse.LEFT_BUTTON)
                if nc.buttons.Z:
                    mouse.press(Mouse.RIGHT_BUTTON)
                else:
                    mouse.release(Mouse.RIGHT_BUTTON)
            
            # Update LED color based on mode
            if scroll_enabled:
                pixel.fill((0, 255, 0))  # Green for normal mode with scroll
            else:
                pixel.fill((0, 0, 255))  # Blue for normal mode without scroll
            
        except Exception as e:
            print(f"Error in mouse handling: {e}")
            pixel.fill((255, 0, 0))
            time.sleep(0.1)

def handleJoystick():
    js = Joystick(usb_hid.devices)
    
    while True:
        x, y = nc.joystick
        y = 255 - y
        print(f"X: {x}, Y: {y}")
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

def handleKeyboard():
    kbd = Keyboard(usb_hid.devices)

    last_x_key = None
    last_y_key = None

    while True:
        x, y = nc.joystick
        x = x - 127
        y = -(y - 127)

        if 15 < x:
            last_x_key = Keycode.RIGHT_ARROW
            kbd.press(Keycode.RIGHT_ARROW)
        elif -15 > x:
            last_x_key = Keycode.LEFT_ARROW
            kbd.press(Keycode.LEFT_ARROW)
        elif None != last_x_key:
            kbd.release(last_x_key)
            last_x_key = None

        if 15 < y:
            last_y_key = Keycode.DOWN_ARROW
            kbd.press(Keycode.DOWN_ARROW)
        elif -15 > y:
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
            kbd.press(Keycode.B)
        else:
            kbd.release(Keycode.B)

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
        print("Nunchuk initialized")

        with open("config.json") as f:
            data = f.read()
            config = json.loads(data)
            print(f"Mode: {config['type']}")
            
            if "joystick" == config["type"]:
                handleJoystick()
            elif "mouse" == config["type"]:
                handleMouse()
            elif "keyboard" == config["type"]:
                handleKeyboard()

    except RuntimeError as e:
        pixel.fill((255, 0, 0))
        print("Error: ", e)
        time.sleep(1)
        
    except OSError as e:
        pixel.fill((0, 0, 255))
        print("Error: ", e)
        time.sleep(1)