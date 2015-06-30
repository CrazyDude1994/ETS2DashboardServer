from ctypes import *

vjoy = cdll.LoadLibrary("vJoyInterface.dll")


class VJoy:
    AcquireVJD = vjoy.AcquireVJD
    GetVJDStatus = vjoy.GetVJDStatus
    SetAxis = vjoy.SetAxis
    SetBtn = vjoy.SetBtn
