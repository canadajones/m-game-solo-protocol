#!/usr/bin/python

import mido
import compose
import console

clear = console.clear

current_input = ""



def user_select_input():
	global current_input
	
	while True:
		clear()
		print("MIDI inputs: ")

		i = 0
		for inport in mido.get_input_names():
			print(str(i) + ": " + inport)
			i += 1
		
		x = int(input("Please select input index: "))

		if x < 0 or x >= len(mido.get_input_names()):
			print("Invalid index!")
			continue
		

		current_input = mido.get_input_names()[x]
		return

user_select_input()

with mido.open_input(current_input) as inport:
    for msg in inport:
        print(compose.list_to_hexstring(msg.data))
        print(compose.MGMessage(None, msg.data))
