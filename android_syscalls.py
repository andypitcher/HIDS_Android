#!/usr/bin/env python
#
#Author: andypitcher <andy.pitcher@mail.concordia.ca>
#This program trains and collects the system calls run by a given app by generating random usage
#It calls match_sig.py afterwhile to match the straces PID and PID children to the signatures 
#
##############################################################################################
from match_sig import check_sig
import subprocess
import pexpect
import sys,os
from random import randint

#Env setup
attempt=randint(0,100)
temp_strace_dir="/system/xbin/strace_dir/"+str(attempt)+"/"
app=sys.argv[1]
rand_iterations="50"

#Cleaning strace dir
os.system("adb shell 'rm -rf /system/xbin/strace_dir/*'")

#Create training directory on Android device
os.system("adb shell mkdir "+temp_strace_dir)  

#Retrieve zygote PID to attach the future app pid
cmd_get_zygote_pid="adb shell ps | grep zygote | awk '{print $2}'"
zygote_PID=subprocess.check_output([cmd_get_zygote_pid], shell=True)

#Get all attached Zigote's child process and App PID to pull the its strace output
cmd_get_all_pid="adb shell pgrep -P"+zygote_PID
cmd_get_app_pid="adb shell ps | grep "+app+" | awk '{print $2}'"

#Start zygote's PID strace subprocess in bg which collects and copy its children process in temp_strace_dir 
#cmd_get_all_strace="adb shell strace -e"+trace_filter+" -ff -o"+temp_strace_dir+"trace -p"+str(zygote_PID)
cmd_get_all_strace="adb shell strace -ff -o"+temp_strace_dir+"trace -p"+str(zygote_PID)
proc_strace=subprocess.Popen([cmd_get_all_strace], shell=True)

#Print all attached Zygote's child process before lauching the app
zygote_child_PID=subprocess.check_output([cmd_get_all_pid], shell=True)
print "Number of child process\n"+zygote_child_PID

#input("Press any key to start the next? Default["+app+"]")

#Start the app and launch random unit tests: rand_iterations, throttle can be removed or increased to reduce the delay between events
os.system("adb shell monkey --throttle 50 -p "+app+" -c android.intent.category.LAUNCHER "+rand_iterations)
app_PID=subprocess.check_output([cmd_get_app_pid], shell=True)

#Stop the Zigote strace
proc_strace.kill()

print "REPORT:\n\n\n\n"
#Pull the trace.app_PID file to the computer and remove temp_strace_dir
os.system("adb pull "+temp_strace_dir+" reports/")

#Checking signatures matchs and either raise an alert or kill the application
status,details=check_sig(attempt)


if status == 1:
	print('\x1b[6;30;41m' +"Logging: Reverse tcp shell detected!!!Killing the app..."+app+ '\x1b[0m')
        print details
        #Stop the app
        os.system("adb shell am force-stop "+app)
elif status == 2:
	print('\x1b[6;30;43m'+"Logging: Attempt of external connection"+'\x1b[0m')
        print details
else:
	print('\x1b[6;30;42m' + "Logging: OK" + '\x1b[0m')
        
#Flushing the the remote directory 
os.system("adb shell rm -rf "+temp_strace_dir)
