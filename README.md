# thorlabs_lcc2415

Basic python script for communicating with a Thorlabs LCC2415-VIS Multi-Wave Variable Retarder with Integrated Controller.


**Installation**

The package is based on the .dll's provided by Thorlabs (uart_library_ftdi32.dll and uart_library_ftdi64.dll), so it only works on Windows. So far no alternative known for Linux or Mac.
It should be possible to replace the .dll's with newer ones provided by Thorlabs.
Installation of the Thorlabs software package (see reference) should not be required.

Connect a Thorlabs LCC2415 to your computer. 

Run test_LCC.py directly in the folder. This will perform several functions of the control_LCC.py script, such as automatically connecting to the LCC2415, set wavelength, get retardance, set retardance, etc.


**Information on Usage**

Two different LCC2415 were used without any issues. control_LCC.py includes the most important functions, adapted from the C++ code (see LCC2415_Api.h) provided by Thorlabs (see reference). More functions can be included. To my knowledge the script is not directly compatible to other LC retarders.


**Known Issue**

Depending on the python version (if >3.8), the dll can not be loaded from a specific folder. Has to be implemented in the future. 


**References**

- [Thorlabs LCC2415 software](https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=LCC2415)
