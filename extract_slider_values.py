#!/usr/bin/python
import linecache

filename = input()

i = 1
while linecache.getline(filename,i):

    x = linecache.getline(filename,i)
    if (not x):
        continue
    a = x.split(" ")
    a.pop(-1)

    b = [int(el, 16) for el in a]

    
    if (b[7] == 0 and b[9] != 0):
        print(b[10])

    i += 1