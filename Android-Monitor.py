# Python3
# Android Monitor
import os
import cv2
import sys
import numpy as np
import pyautogui
import PIL.ImageGrab as ImageGrab
import imutils
import time
import psutil
from subprocess import run

box = (174,31,509,736) #Android screen coordinates
def work_site():                #cause script to execute in directory containing script and adb
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))  #move to dir that holds this script and ADB (need to change for exe)
    global pwd
    pwd = os.path.dirname(os.path.abspath(__file__))
	
work_site()

def checkIfProcessRunning(processName):
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def convert_time(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)

def tap_once(x,y):
	try:
	# os.chdir(adb_dir)
		tap_coordinates = 'adb shell input tap '+str(x)+' '+str(y)
		os.system(tap_coordinates) #x,y
		os.chdir(pwd)
	except Exception as e:
		print(e)
		cv2.destroyAllWindows()
	
#Excluding from running two mirrors of android screen
if checkIfProcessRunning('scrcpy-noconsole.exe'):
	print('>> Android screen already mirrored')
else:
	# print('>> Mirroring android screen')
	os.system("start ./AM_Deps/scrcpy-noconsole.exe")

run_status = 1
st = time.time()
adb_dir = os.path.join(pwd, "scrcpy-win64")
fps = int(60)

try:
	while cv2.getWindowProperty(screen,cv2.WND_PROP_VISIBLE) > 1:	
		
		screen = ImageGrab.grab(box)
		screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
		screen = imutils.resize(screen, height=600)
		
		et = time.time()
		elapsed_time = et-st
		elapsed_time = round(elapsed_time)
		try:
			if elapsed_time < 30:
				fps = run_status/elapsed_time
				fps = round(fps)
		except Exception as e:
			print(e)
			fps = 0

		if run_status == 5:
			x,y = (360,360) #coordinate according to your android phone screen
			tap_once(x,y)

		#Program End Handling Block
		run_status +=1
		key = cv2.waitKey(1)
		try:
			if cv2.getWindowProperty(screen,cv2.WND_PROP_VISIBLE) < 1:
				run(['adb.exe kill-server'])
				break
		except SystemError:
			print("minor system error occurred - no biggie")

except NameError:
	#no biggie
	pass
cv2.destroyAllWindows()





