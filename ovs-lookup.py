import time
import os
import sys
import subprocess

bridge = sys.argv[1]
home = subprocess.check_output("pwd",shell=True)
home = '/'+home[1:home.__len__()-1]
filename = time.time()

try:
    os.mkdir(str(home) + '/ovs-lookup/tmp')
except:
    print 'dir always exist'

try:
    print str(home) + '/ovs-lookup/tmp/' + str(filename)
    os.mknod(str(home) + '/ovs-lookup/tmp/' + str(filename))
except:
    print 'file always exist'

file = os.open(home + '/ovs-lookup/tmp/' + str(filename),os.O_WRONLY)

begin = int(time.time())

print "delay time:"+str(int(sys.argv[2]))
print "delay period:"+str(int(sys.argv[3]))
sys.stdout.write("time(s): ")
len=1

while (int(time.time()) - begin) < int(sys.argv[3]):
    res = subprocess.check_output("sudo ovs-ofctl -O OpenFlow13 dump-flows " + str(bridge),shell=True)
    for i in range(len):
        sys.stdout.write("\b")
    sys.stdout.write(str(int(time.time()) - begin))
    sys.stdout.flush()
    len=str(int(time.time()) - begin).__len__()
    os.write(file,'snapshot at '+str(int(time.time()))+'\r\n')
    os.write(file,str(res))
    time.sleep(int(sys.argv[2]))


os.close(file)
os.system('sudo vim '+ home + '/ovs-lookup/tmp/' + str(filename))