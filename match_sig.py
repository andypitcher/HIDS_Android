#!/usr/bin/env python

import glob

def check_sig(session):
	path=("reports/"+str(session)+"/trace.*")
	traces = glob.glob(path)
	# iterate over the list getting each file 
	for trace in traces:
		for line in open(trace):
			if "Meterpreter" in line:
				status=1
				details=trace+"\n"+line
				return status,details
			elif "172.16.16.5" in line:
				status=2
				details=trace+"\n"+line
				return status,details
			else:
				status=0
				continue

statusa,detailsa=check_sig(1)
print str(statusa)+detailsa

