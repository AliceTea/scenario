sudo python ./cbr002.py ./cbrconf001&
sleep 3
sudo ovs-vsctl set bridge s1 protocols=OpenFlow13
sudo python ./ovs-lookup.py s1 1 120 
