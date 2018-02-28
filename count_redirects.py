#!/usr/bin/python2

from collections import defaultdict
from sys import argv


last_urls = {}  # ip: last_url 
url_counter = defaultdict(int)


with open(argv[1]) as f:
    for line in f:
        ip, _, url = line.strip().partition(' ') 
        url, _, _ = url[1:-1].partition('?')
        url = url.strip('/')
        last_url = last_urls.get(ip)
        last_urls[ip] = url
        if last_url is None:
            url_counter[url] = url_counter.get(url, 0)
            continue
        url_counter[last_url] += 1


sorted_urls = sorted(url_counter.iteritems(), key=lambda o: o[1])


for url, count in sorted_urls:
    print count, url
