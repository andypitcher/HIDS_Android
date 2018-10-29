# HIDS_Android: Host-Based Intrusion detection system for Android

## Implementation:

The	main	idea	behind	this	implementation	is	a	proof	of	concept	that	takes	two	same	applications,	
one	legit	and	the other repackaged with a malicious payload (msfvenom). Then,	apply	signature	detection,	basde on	system	calls	to	match	certain	type	
of	pattern.	
Enventually,	this	allows	to	detect	or	prevent	some	attack,	in	our	case,	the	execution	of	
meterpreter	commands	through	a	reverse_tcp	shell.	

## Defense environment:

This PoC	relies	on	three	hosts	all	connected	to	the	same	network	172.16.16.0/24:	

- Kali	linux	VM : Acts	as	a	remote	attack	machine,	which	the	reverse	tcp	shell,	
waiting	for	the	malicious	application	to	be	launched.
- Android	x86	VM (Kitkat	4.4):	Acts	as	the	victim	phone/tablet
- Centos	host:	acts	as	the	HIDS	and	connects	remotely	to	the	Androidx86	through	ADB	
(Android	 debug	 bridge)	 to	 launch	 both	 applications	 (legit	 and	 malicious)	 with	 Monkey	 while	
collecting	the	strace (Zigote)	results	to	be	parsed	and	compared	to	the	signatures.

## Running the program:

- On the Legit App:


