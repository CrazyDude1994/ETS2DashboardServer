from ctypes import *

vjoy = cdll.LoadLibrary("vJoyInterface.dll")

AcquireVJD = vjoy.AcquireVJD
GetVJDStatus = vjoy.GetVJDStatus
SetAxis = vjoy.SetAxis
SetBtn = vjoy.SetBtn

vjoy.SetAxis(1, 1, 48)

print GetVJDStatus(1)
print AcquireVJD(1)
