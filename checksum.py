#!/usr/bin/python
import linecache
import compose

message = input("Please input message to checksum: ")

message.split(" ")

message_bytes = [int(e,16) for e in message.split(" ")]


print("{:02X}".format(compose.compute_checksum(message_bytes)))
    
