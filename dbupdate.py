import sys
import time
import MySQLdb
import re

time = time.time()
print int(time)

#ovs_lookup=re.escape(str(open(sys.argv[1]).readlines()))
#floodlight=re.escape(str(open(sys.argv[2]).readlines()))
ovs_lookup = ""
floodlight = ""
for line in open(sys.argv[2]).readlines():
    ovs_lookup = ovs_lookup + line
for line in open(sys.argv[1]).readlines():
    floodlight = floodlight + line
#floodlight=re.escape(floodlight)
floodlight=floodlight.replace('\'','')

db = MySQLdb.connect("jxtang.me","root","pl,okm123","lablog")

cursor = db.cursor()

cursor.execute("INSERT INTO LabDatas(stp,floodlight,ovs_lookup) VALUES (%d,'%s','%s')" %\
               (int(time),floodlight,ovs_lookup)
               )

db.commit()

cursor.execute("SELECT floodlight FROM `LabDatas` WHERE stp=%d" % int(time))

data = cursor.fetchone()

print "Database version : %s " % data
data = cursor.fetchone()

print "Database version : %s " % data

db.close()
