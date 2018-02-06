from tgnLIB import *
from subprocess import call

def shutdown():
	call(['shutdown', '-h', 'now'], shell=False)

def reboot():
	call(['reboot', '-h', 'now'], shell=False)

c1 = sys.argv[1]
c2 = int(sys.argv[2])
if c2 == "shutdown":
	shutdown()
elif c1 == "reboot":
	reboot()
else:
	send(int(c1),int(c2))
