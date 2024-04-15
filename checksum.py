#!/usr/bin/python
import linecache

filename = input()


for i in range(127):

    x = linecache.getline(filename,123)
    a = x.split(" ")
    a.pop(-1)

    b = [int(el, 16) for el in a]

    print(sum(b) % 128)