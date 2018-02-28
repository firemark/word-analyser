#!/usr/bin/python2

from collections import defaultdict
from sys import argv


IPS_COUNTER = defaultdict(int)  # ip: counter


with open(argv[1]) as f:
    for line in f:
        ip, _, url = line.partition(' ') 
        IPS_COUNTER[ip] += 1


ips = (ip for ip, counter in IPS_COUNTER.iteritems() if counter <= 1)
for ip in ips:
    print ip

