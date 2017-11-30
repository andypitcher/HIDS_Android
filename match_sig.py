#!/usr/bin/env python

import glob

def check_sig(session):
path=("reports/*/trace.*")
traces = glob.glob(path)
# iterate over the list getting each file 
for trace in traces:
	for line in open(trace):
		if "Meterpreter" in line:
			status=1
			details=trace+"\n"+line
			return details
		elif "connect" in line:
			status=2
			details=trace+"\n"+line
			return details
		else:
			status=0
			return status

