#!/usr/bin/python


import mido
import os
import time
import keyboard
import sys

import console
import compose

from error_code_table import error_decode as error_decode


grab_command = console.grab_command
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

current_output = ""

def user_select_output():
	global current_output

	while True:
		clear()
		print("MIDI outputs: ")
		
		i = 0
		for outport in mido.get_output_names():
			print(str(i) + ": " + outport)
			i += 1
		
		x = int(input("Please select output index: "))


		if x < 0 or x >= len(mido.get_output_names()):
			print("Invalid index!")
			continue
		
		current_output = mido.get_output_names()[x]
		return

def list_sources(args):
	for source in compose.sources.items():
		print(source[0], ":", source[1])
	return (True, None)


def list_sinks(args):
	for sink in compose.sinks.items():
		print(sink[0], ":", sink[1])
	return (True, None)

def list_msg_types(args):
	for t in compose.msg_types.items():
		print(t[0], ":", t[1])
	return (True, None)

current_message = []

def list_message(args):
	print(''.join('{:02X} '.format(a) for a in current_message))
	return (True, None)

def list_message_pretty(args):
	print(current_message)
	print(compose.MGMessage(None, current_message))
	return (True, None)

def patch(args):
	global current_message

	source = args[0]
	sink = args[1]

	if not source in compose.sources.keys():
		return (False, "E_no_such_source")

	if not sink in compose.sinks.keys():
		return (False, "E_no_such_sink")
	
	current_message = compose.MGMessage("short", source, sink, "patch", [0x44, 0x73]).compose_message()
	return (True, None)

def unpatch(args):
	global current_message
	
	source = args[0]
	sink = args[1]
	
	if not source in compose.sources.keys():
		return (False, "E_no_such_source")

	if not sink in compose.sinks.keys():
		return (False, "E_no_such_sink")


	current_message = compose.MGMessage("short", source, sink, "patch", [0x44, 0x73]).compose_message()
	return (True, None)

def vol_change(args):
	global current_message

	source = args[0]
	sink = args[1]
	
	try:
		val = int(args[2], 16)

	except:
		return (False, "E_irrepresentible_vol")
	
	if not source in compose.sources.keys():
		return (False, "E_no_such_source")

	if not sink in compose.sinks.keys():
		return (False, "E_no_such_sink")
	
	if val > 127 or val < 0:
		return (False, "E_irrepresentible_vol")


	current_message = compose.MGMessage("short", source, sink, "vol_change", [0x00, val]).compose_message()
	return (True, None)


def enter_message(args):
	global current_message

	current_message = compose.hexstring_to_list(' '.join(args))
	
	return (True, None)

def transmit(args):
	global current_message

	print("using indev:", current_input, "outdev:", current_output)
	with mido.open_input(current_input) as inport:
		with mido.open_output(current_output) as o:
			o.send(mido.Message("sysex", data=current_message))
			
			current_message = []
			
			time.sleep(0.01)

			for msg in inport.iter_pending():
				print(compose.list_to_hexstring(msg.data))
				print(compose.MGMessage(None, msg.data))
			return (True, None)


def listen(args):
	with mido.open_input(current_input) as inport:
		try:
			while True:
				if (msg := inport.poll()):
					print(compose.list_to_hexstring(msg.data))
					print(compose.MGMessage(None, msg.data))
		
		
		except:
			return (True, None)
		







function_command_dict = {
	"list_sources": list_sources,
	"list_sinks": list_sinks,
	"list_msg_types": list_msg_types,	
	"patch": patch,
	"unpatch": unpatch,
	"vol_change": vol_change,
	"list_message": list_message,
	"pretty_message": list_message_pretty,		
	"enter_message": enter_message,
	"transmit": transmit,
	"listen": listen

}

help_string = "Full command list:\nBracketed entries denote mandatory operands, square bracketed denote optional operand\n\n" + '\n'.join('\t' + command for command in function_command_dict.keys())



user_select_input()
user_select_output()

print("Which action would you like to take?")
print(help_string)

while True:
	grab_command(help_string, function_command_dict)