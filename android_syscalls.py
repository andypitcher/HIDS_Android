#!/usr/bin/env python
#
#Andy Pitcher <andy.pitcher@concordia.ca>
#This program trains and collects the system calls run by a given app by generating random usage
#
##############################################################################################

import subprocess
import pexpect
import sys,os
from random import randint

#Env setup
attempt=randint(0,100)
temp_strace_dir="/sdcard/Download/strace/"+str(attempt)+"/"
app="com.android.calculator2"
rand_iterations="200"

#Create training directory on Android device
os.system("adb shell mkdir "+temp_strace_dir)  

#Retrieve zygote PID to attach the future app pid
cmd_get_zygote_pid="adb shell ps | grep zygote | awk '{print $2}'"
zygote_PID=subprocess.check_output([cmd_get_zygote_pid], shell=True)

#Get all attached Zigote's child process and App PID to pull the its strace output
cmd_get_all_pid="adb shell pgrep -P"+zygote_PID
cmd_get_app_pid="adb shell ps | grep "+app+" | awk '{print $2}'"

#Start zygote's PID strace subprocess in bg which collects and copy its children process in temp_strace_dir 
cmd_get_all_strace="adb shell strace -ff -o"+temp_strace_dir+"trace -p"+str(zygote_PID)
proc_strace=subprocess.Popen([cmd_get_all_strace], shell=True)

#Print all attached Zygote's child process before lauching the app
zygote_child_PID=subprocess.check_output([cmd_get_all_pid], shell=True)
print "Number of child process\n"+zygote_child_PID

#input("Press any key to start the next? Default["+app+"]")

#Start the app and launch random unit tests: rand_iterations, throttle can be removed or increased to reduce the delay between events
os.system("adb shell monkey --throttle 50 -p "+app+" -c android.intent.category.LAUNCHER "+rand_iterations)
app_PID=subprocess.check_output([cmd_get_app_pid], shell=True)

#Stop the app
os.system("adb shell am force-stop "+app)
#Stop the Zigote strace
proc_strace.kill()

#Pull the trace.app_PID file to the computer and remove temp_strace_dir
os.system("adb pull "+temp_strace_dir+"trace."+app_PID)
os.system("adb shell rmdir -r "+temp_strace_dir)
