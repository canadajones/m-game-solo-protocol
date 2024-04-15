#!/usr/bin/python
import mido
import os

with mido.open_input(mido.get_input_names()[1]) as inport:
	for msg in inport:
		print(''.join('{:02X} '.format(a) for a in msg.data))