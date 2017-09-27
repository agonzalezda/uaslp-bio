#!/usr/bin/env python
# ------------------------ Force plate ATM wrapper  --------------------------------
# Description: ATM function definitions
# --------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of ay kind.
# Autor: Luis Enrique Coronado Zuniga

## TODO the wrapper can be improved adding more functions (see AMTIUSBDeviceDefinitions.h)
from ctypes import*
from nep import*

atmdll = cdll.LoadLibrary("AMTIUSBDevice.dll")
fmDLLInit = atmdll['fmDLLInit']
fmDLLInit.restype = c_void_p

DeviceInitComplete = atmdll['fmDLLIsDeviceInitComplete']
DeviceInitComplete.restype = c_int

fmBroadcastAcquisitionRate = atmdll['fmBroadcastAcquisitionRate']
fmBroadcastAcquisitionRate.restype = c_void_p

fmBroadcastZero = atmdll['fmBroadcastZero']
fmBroadcastZero.restype = c_void_p

fmDLLPostDataReadyMessages = atmdll['fmDLLPostDataReadyMessages']
fmDLLPostDataReadyMessages.restype = c_void_p

fmBroadcastRunMode = atmdll['fmBroadcastRunMode']
fmBroadcastRunMode.restype = c_void_p

fmDLLSetDataFormat = atmdll['fmDLLSetDataFormat']
fmDLLSetDataFormat.restype = c_void_p

fmBroadcastResetSoftware = atmdll['fmBroadcastResetSoftware']
fmBroadcastResetSoftware.restype = c_void_p

fmBroadcastStart = atmdll['fmBroadcastStart']
fmBroadcastStart.restype = c_void_p

fmBroadcastStop = atmdll['fmBroadcastStop']
fmBroadcastStop.restype = c_void_p

fmDLLTransferFloatData = atmdll['fmDLLTransferFloatData']
fmDLLTransferFloatData.restype =  c_int
fmDLLTransferFloatData.argtypes = [POINTER((POINTER(c_float)))]

fmDLLGetTheFloatDataLBVStyle = atmdll['fmDLLGetTheFloatDataLBVStyle']
fmDLLGetTheFloatDataLBVStyle.restype =  c_int
fmDLLGetTheFloatDataLBVStyle.argtypes = [POINTER(c_float), c_int]




