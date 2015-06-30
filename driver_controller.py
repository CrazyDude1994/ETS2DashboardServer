from driver_interface import *

HID_USAGE_X = 0x30
HID_USAGE_Y = 0x31
HID_USAGE_Z = 0x32
HID_USAGE_RX = 0x33
HID_USAGE_RY = 0x34
HID_USAGE_RZ = 0x35
HID_USAGE_SL0 = 0x36
HID_USAGE_SL1 = 0x37
HID_USAGE_WHL = 0x38
HID_USAGE_POV = 0x39


class VJoyException(Exception):
    pass


class Joystick:
    def __init__(self, id):
        self._id = id
        code = VJoy.AcquireVJD(id)
        if not code:
            raise VJoyException("Failed to aquaire device")

    def set_button_pressed(self, id, state):
        VJoy.SetBtn(state, self._id, id)

    def set_slider_position(self, id, position):
        VJoy.SetAxis(position, self._id, id)
