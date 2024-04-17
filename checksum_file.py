#!/usr/bin/python
import linecache
import compose

filename = input("Please input filename to checksum all messages in: ")

i = 0

while linecache.getline(filename, i):

    x = linecache.getline(filename,i)
    a = [int(e,16) for e in x.split(" ")]
    a.pop(-1)

    print(compose.compute_checksum(a))
    
    i += 1