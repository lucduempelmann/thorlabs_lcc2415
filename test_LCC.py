"""
Example code to control a Thorlabs LCC2415 Phase Retarder, 
by performing some commands defined in control_LCC.py.

@author: Luc Dümpelmann
"""

import control_LCC
import os, time
from ctypes import *

LCC=control_LCC.LCCRetard()                     # connect to the device with serial number set

# Example how to run the python script
ret=LCC.fnLCC2415_SetWavelength(LCC.hdl,500)   	# set wavelength to 500nm
assert ret==0
c=create_string_buffer(255)	                	# buffer string, could be implemented in definitions separately in the future
ret=LCC.fnLCC2415_GetRetardance(LCC.hdl,c)      # get retardance
assert ret==0
ret=LCC.fnLCC2415_SetRetardance(LCC.hdl,50)     # set retardance to 50nm
assert ret==0
ret=LCC.fnLCC2415_GetRetardance(LCC.hdl,c)      # get retardance
assert ret==0
ret=LCC.fnLCC2415_GetID(LCC.hdl,c)              # get ID
assert ret==0
ret=LCC.LCC_MoveRelative(LCC.hdl,100)           # move relative 100
ret=LCC.fnLCC2415_SetRetardance(LCC.hdl,100)    # set retardance to 100
assert ret==0
ret=LCC.fnLCC2415_GetRetardance(LCC.hdl,c)      # get retardance
assert ret==0
ret=LCC.fnLCC2415_Close(LCC.hdl)                # disconnect device

    # Example of looping through a range of wavelength retardance
   	# for i in range(0,20):                         # automatically changes retardance every 0.5sec
   	# 	time.sleep(0.5)
   	# 	ret = LCC.fnLCC2415_GetRetardance(hdl,c)
   	# 	assert ret==0
   	# 	ret = LCC.LCC2415_SetRetardance(hdl,i*50)
   	# 	assert ret==0
   
   	#LCC.fnLCC2415_GetID(hdl,c)
   	#hdl=LCC.fnLCC2415_Open(hdl)