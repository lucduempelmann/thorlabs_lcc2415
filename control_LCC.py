"""
Script to control a Thorlabs LCC2415 Phase Retarder, by using the .dll files 
uart_library_ftdi32.dll or uart_library_ftdi64.dll (depending on operation system)
provided by Thorlabs (https://www.thorlabs.com/software_pages/viewsoftwarepage.cfm?code=LCC2415).
The most important functions are included in the code, but the list is not exhaustive. 

@author: Luc Dümpelmann
"""

DEBUG = False
import os, time, sys
from ctypes import *
if DEBUG: print((os.getcwd()))

class LCCRetard():
	def __init__(self, SerialNum = None):    
		# # =========================================================
		#Load dll file (select 32 or 64 bit version)
		self.dll_handle = windll.LoadLibrary('uart_library_ftdi64.dll')
		# =========================================================
		self.openP=self.dll_handle.fnUART_LIBRARY_open
		self.isOpen=self.dll_handle.fnUART_LIBRARY_isOpen
		self.listP=self.dll_handle.fnUART_LIBRARY_list
		self.close=self.dll_handle.fnUART_LIBRARY_close
		self.write=self.dll_handle.fnUART_LIBRARY_write
		self.read=self.dll_handle.fnUART_LIBRARY_read
		self.Set=self.dll_handle.fnUART_LIBRARY_Set
		self.Get=self.dll_handle.fnUART_LIBRARY_Get
		self.Req=self.dll_handle.fnUART_LIBRARY_Req
		self.timeout=self.dll_handle.fnUART_LIBRARY_timeout
		self.Purge=self.dll_handle.fnUART_LIBRARY_Purge
		# =========================================================
		self.Connected = False
		# =========================================================
		if SerialNum==None:
			c=create_string_buffer(255)
			ret=self.listP(c,255)
			N_ThlabsDevices = c.value.decode().count(str("LCC"))
			if N_ThlabsDevices == 0:
				print('No Thorlabs controller detected')
				self.hdl=-1
			elif N_ThlabsDevices > 1:
				print('More than 1 Thorlabs LCC controller detected')
				sn=self.fnLCC2415_List_Manual(c)
				self.hdl=self.fnLCC2415_Open(sn)
			else:
				print('1 Thorlabs LCC controller detected')
				sn=self.fnLCC2415_List_Auto(c)
				self.hdl=self.fnLCC2415_Open(sn)
		else:
			self.hdl=self.fnLCC2415_Open(SerialNum)
		
		if self.hdl < 0:
			print("COM port failed to open - is a device connected?")
			sys.exit()
		else:
			self.Connected = True
			print('LCC connected')

	def getNumberOfHardwareUnits(self):
		# Returns the number of HW units connected that are available to be interfaced
		numUnits = c_long()
		self.dll_handle.GetNumHWUnitsEx(self.HWType, pointer(numUnits))
		return numUnits.value

	def fnLCC2415_List_Manual(self,c):
		print("Connected LCC devices:")
		print(c.value)
		print("Please input serial number:"); 
		sn=create_string_buffer(bytes(input(),"utf-8"),256)
		return sn

	def fnLCC2415_List_Auto(self,c):
		ret=self.listP(c,255)
		text=c.value.decode()
		for i in range(text.find("LCC")):
			if text[text.find("LCC")-i]==",":
				ret=text[text.find("LCC")-i-8:text.find("LCC")-i]
				sn=create_string_buffer(bytes(ret,"utf-8"),256)
				break
		return sn
	
	def fnLCC2415_Open(self,sn):
		hdl = self.openP(sn, c_int(115200), c_int(3))
		if hdl<0:
			return hdl
		b=c_char_p(b"\05\0")
		ret = self.Set(hdl,b,0)
		return hdl

	def fnLCC2415_GetRetardance(self,hdl,c):
		ret=0
		b=c_char_p(b"RE?\r")
		ret = self.Get(hdl,b,c)
		return ret

	def fnLCC2415_GetID(self,hdl,c):
		ret=0
		b=c_char_p(b"*idn?\r")
		ret = self.Get(hdl,b,c)
		print("LCC ID is: " + str(c.value))
		return ret

	def fnLCC2415_SetRetardance(self,hdl,n):
		ret=0
		b=c_char_p(b"RE=%d\r" %(n))
		c=create_string_buffer(255)
		ret = self.Set(hdl,b,c)
		print('LCC set Retardance to '+str(n)+'nm')
		return ret

	def fnLCC2415_SetWavelength(self,hdl,n):
		ret=0
		b=c_char_p(b"WL=%d\r" %(n))
		ret = self.Set(hdl,b,0)
		print('LCC set Wavelength to '+str(n)+'nm')
		return ret

	def fnLCC2415_Close(self,hdl):
		ret=0
		self.close(hdl)
		print('LCC disconnected')
		return ret

	def LCC_MoveRelative(self,hdl,moveRel):
		c=create_string_buffer(255)	
		ret=self.fnLCC2415_GetRetardance(self.hdl,c)
		code_string,code_value=self.decode_ReturnString(c)
		ret=self.fnLCC2415_SetRetardance(self.hdl,moveRel+code_value)
		return ret

	def decode_ReturnString(self,c):
		# decodes a return string c, e.g. b'RE=50\r>' into a:
		# code_string = RE=50 and code_value = 50
		code_string=c.value.decode().split('\r>')[0]
		code_value=int(code_string.split('=')[1])
		return code_string, code_value