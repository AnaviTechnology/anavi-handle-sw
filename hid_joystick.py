# SPDX-FileCopyrightText: Copyright (c) 2023 Leon Anavi <leon@anavi.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
HID Joystick

This code is based on the Adafruit hid_gamepad.py example. See boot.py for
the joystick HID report descriptor.
"""

import struct
import time

from adafruit_hid import find_device


class Joystick:
    """Emulate a generic joystick controller with 8 buttons,
    numbered 1-8, and two joysticks, one controlling
    ``x` and ``y`` values

    The joystick values could be interpreted
    differently by the receiving program: those are just the names used here.
    The joystick values are in the range -127 to 127."""

    def __init__(self, devices):
        """Create a Joystick object that will send USB joystick HID reports.

        Devices can be a list of devices that includes a joystick device or a joystick device
        itself. A device is any object that implements ``send_report()``, ``usage_page`` and
        ``usage``.
        """
        self._joystick_device = find_device(devices, usage_page=0x1, usage=0x04)

        # Reuse this bytearray to send joystick reports.
        # Typically controllers start numbering buttons at 1 rather than 0.
        # report[0] buttons 1-8 (LSB is button 1)
        # report[1] joystick x: -127 to 127
        # report[2] joystick y: -127 to 127
        self._report = bytearray(3)

        # Remember the last report as well, so we can avoid sending
        # duplicate reports.
        self._last_report = bytearray(3)

        # Store settings separately before putting into report. Saves code
        # especially for buttons.
        self._buttons_state = 0
        self._joy_x = 0
        self._joy_y = 0

        # Send an initial report to test if HID device is ready.
        # If not, wait a bit and try once more.
        try:
            self.reset_all()
        except OSError:
            time.sleep(1)
            self.reset_all()

    def press_buttons(self, *buttons):
        """Press and hold the given buttons."""
        for button in buttons:
            self._buttons_state |= 1 << self._validate_button_number(button) - 1
        self._send()

    def release_buttons(self, *buttons):
        """Release the given buttons."""
        for button in buttons:
            self._buttons_state &= ~(1 << self._validate_button_number(button) - 1)
        self._send()

    def release_all_buttons(self):
        """Release all the buttons."""

        self._buttons_state = 0
        self._send()

    def click_buttons(self, *buttons):
        """Press and release the given buttons."""
        self.press_buttons(*buttons)
        self.release_buttons(*buttons)

    def move_joysticks(self, x=None, y=None):
        """Set and send the given joystick values.
        The joysticks will remain set with the given values until changed

        One joystick provides ``x`` and ``y`` values,
        Any values left as ``None`` will not be changed.

        All values must be in the range -127 to 127 inclusive.

        Examples::

            # Change x and y values only.
            gp.move_joysticks(x=100, y=-50)

            # Reset all joystick values to center position.
            gp.move_joysticks(0, 0)
        """
        if x is not None:
            self._joy_x = self._validate_joystick_value(x)
        if y is not None:
            self._joy_y = self._validate_joystick_value(y)
        self._send()

    def reset_all(self):
        """Release all buttons and set joysticks to center."""
        self._buttons_state = 0
        self._joy_x = 0
        self._joy_y = 0
        self._send(always=True)

    def _send(self, always=False):
        """Send a report with all the existing settings.
        If ``always`` is ``False`` (the default), send only if there have been changes.
        """
        struct.pack_into('BBB', self._report, 0,
                self._buttons_state,
                self._joy_x,
                self._joy_y
        )

        if always or self._last_report != self._report:
            self._joystick_device.send_report(self._report)
            # Remember what we sent, without allocating new storage.
            self._last_report[:] = self._report

    @staticmethod
    def _validate_button_number(button):
        if not 1 <= button <= 8:
            raise ValueError("Button number must in range 1 to 8")
        return button

    @staticmethod
    def _validate_joystick_value(value):
        if not 0 <= value <= 255:
            raise ValueError("Joystick value must be in range 0 to 255")
        return value
