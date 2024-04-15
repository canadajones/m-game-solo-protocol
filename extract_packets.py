#!/usr/bin/python

import json

def my_obj_pairs_hook(lst):
    result={}
    count={}
    for key,val in lst:
        if key in count:count[key]=1+count[key]
        else:count[key]=1
        if key in result:
            if count[key] > 2:
                result[key].append(val)
            else:
                result[key]=[result[key], val]
        else:
            result[key]=val
    return result
capture = json.load(open(input("Enter name of file to load: ")), object_pairs_hook=my_obj_pairs_hook)


def test(capture):
    for element in capture:
        for ua in element["_source"]["layers"]["usbaudio"]:
            if "usbaudio.sysex.fragments" in ua:
    	        if not ua == "usbaudio.sysex.fragments" and "usbaudio.sysex.reassembled.data" in ua["usbaudio.sysex.fragments"]:
    	    	    print(ua["usbaudio.sysex.fragments"]["usbaudio.sysex.reassembled.data"])



test(capture)
