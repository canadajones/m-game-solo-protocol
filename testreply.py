import mido
import os




command_string = "00 01 05 43 00 01 00 04 00 44 73 00 00 00 7b"

command = [int(x, 16) for x in command_string.split(" ")]



print("using dev ", mido.get_input_names())

with mido.open_input(mido.get_input_names()[1]) as inport:
	with mido.open_output(mido.get_output_names()[1]) as o:
		o.send(mido.Message("sysex", data=command))
		
		for msg in inport:
			print(''.join('{:02X} '.format(a) for a in msg.data))