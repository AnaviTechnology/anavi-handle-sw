import json
import usb_hid

# Extended descriptor to include accelerometer axes
JOYSTICK_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,  # Usage Page (Generic Desktop Ctrls)
    0x09, 0x04,  # Usage (Joystick)
    0xA1, 0x01,  # Collection (Application)
    
    # Buttons (same as before)
    0x15, 0x00,  # Logical Minimum (0)
    0x25, 0x01,  # Logical Maximum (1)
    0x35, 0x00,  # Physical Minimum (0)
    0x45, 0x01,  # Physical Maximum (1)
    0x75, 0x01,  # Report Size (1)
    0x95, 0x08,  # Report Count (8)
    0x05, 0x09,  # Usage Page (Button)
    0x19, 0x01,  # Usage Minimum (Button 1)
    0x29, 0x08,  # Usage Maximum (Button 8)
    0x81, 0x02,  # Input (Data,Var,Abs,No Wrap,Linear)
    
    # Joystick X/Y axes (same as before)
    0x05, 0x01,  # Usage Page (Generic Desktop Ctrls)
    0x26, 0xFF, 0x00,  # Logical Maximum (255)
    0x46, 0xFF, 0x00,  # Physical Maximum (255)
    0x09, 0x30,  # Usage (X)
    0x09, 0x31,  # Usage (Y)
    0x75, 0x08,  # Report Size (8)
    0x95, 0x02,  # Report Count (2)
    0x81, 0x02,  # Input (Data,Var,Abs,No Wrap,Linear)
    
    # Accelerometer axes (X, Y, Z)
    0x09, 0x33,  # Usage (Rx) - Using Rx/Ry/Rz for accel
    0x09, 0x34,  # Usage (Ry)
    0x09, 0x35,  # Usage (Rz)
    0x75, 0x08,  # Report Size (8)
    0x95, 0x03,  # Report Count (3)
    0x81, 0x02,  # Input (Data,Var,Abs,No Wrap,Linear)
    
    0xC0,        # End Collection
))

joystick = usb_hid.Device(
    report_descriptor=JOYSTICK_REPORT_DESCRIPTOR,
    usage_page=0x01,           # Generic Desktop Control
    usage=0x04,                # Joystick
    report_ids=(0,),           # Descriptor uses report ID 0
    in_report_lengths=(6,),    # Now we send 6 bytes (buttons + joy + accel)
    out_report_lengths=(0,),   # No output reports
)