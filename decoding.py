#!/usr/bin/python

import mido
import os

def compute_checksum(id, sv):
	ov = 0x35 - id

	return (ov - sv)



def handle_slider(data):
	ret = "ID: {:x}, ".format(data[1])

	if (data[4] == 0x00):

		ret += "begin, "
	elif data[4] == 0x44:
		#return ""
		ret += "seq: {:x}, ".format(data[2])
	else:
		return "error! invalid continuation byte! " + str(data)
	
	ret += "SV: {:x}".format(data[5] - data[4] if data[5] != 0 else data[5])

	return ret

def log_slider(data):
	ret = ""

	if (data[4] == 0x00):
		computed_sv = -(data[9] - (53 - data[1]))
		ret += str((data[5], computed_sv if computed_sv >= 0 else computed_sv + 128 ))

	return ret


def decode_sysex(data):
	if (data[3]) == 0x01:
		return handle_slider(data)
	
	return str(data)

with mido.open_input(mido.get_input_names()[1]) as inport:
	for msg in inport:
		print(''.join('{:02X} '.format(a) for a in msg.data))
		#val = decode_sysex(msg.data[5:])
		val = log_slider(msg.data[5:])

		if (val):
			#print(val)
			pass