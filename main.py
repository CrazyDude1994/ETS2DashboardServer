from ctypes import *

vjoy = cdll.LoadLibrary("vJoyInterface.dll")

AcquireVJD = vjoy.AcquireVJD
GetVJDStatus = vjoy.GetVJDStatus
SetAxis = vjoy.SetAxis
SetBtn = vjoy.SetBtn

print GetVJDStatus(1)
print AcquireVJD(1)