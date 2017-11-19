#!/usr/bin/env python
#
#Andy Pitcher <andy.pitcher@concordia.ca>
#

import subprocess
import pexpect
import sys,os

#adb="/usr/share/platform-tools/adb"

temp_strace_dir="/sdcard/Download/strace/"
app="com.android.calculator2"

cmd_get_zygote_pid="adb shell ps | grep zygote | awk '{print $2}'"
zygote_PID=subprocess.check_output([cmd_get_zygote_pid], shell=True)
cmd_get_all_pid="adb shell pgrep -P"+zygote_PID
cmd_get_all_strace="adb shell strace -ff -o"+temp_strace_dir+"output.txt -p"+str(zygote_PID)
cmd_get_app_pid="adb shell ps | grep "+app+" | awk '{print $2}'"
subprocess.Popen([cmd_get_all_strace], shell=True)
zygote_child_PID=subprocess.check_output([cmd_get_all_pid], shell=True)

print "Number of child process\n"+zygote_child_PID

raw_input("Press any key to start the next? Default["+app+"]")
os.system("adb shell monkey -p "+app+" -c android.intent.category.LAUNCHER 1")







#command="adb shell strace -o "+ temp_strace_dir+" -ff -p"+str(i)
#for i in zygote_PID:
#	os.system("adb shell strace -o "+ temp_strace_dir+"-ff -p"+str(i)+" &")
#subprocess.Popen(command,shell=True)
#adb_android.shell("monkey -p com.android.calculator2 -c android.intent.category.LAUNCHER 1")



#syscalls = set(ln.split('(', 1)[0] for ln in strace_output)
#for i in syscalls:
#	print i
#child = pexpect.spawn(adb + " shell")
#child.logfile_send = sys.stdout
#child.sendline("ls")
#child.expect(pexpect.EOF)
#print child.read()
