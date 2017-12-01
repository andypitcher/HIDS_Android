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
			elif "Connection refused" in line:
				status=2
				details=trace+"\n"+line
				return status,details
			else:
				status=0
				details="Ok"
				continue
	return status,details


