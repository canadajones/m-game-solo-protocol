#! /usr/bin/python

import json

def compute_checksum_value(vals):
	return 128 - (sum(vals) % 128)

def compute_checksum(vals):
	return sum(vals) % 128


def hexstring_to_list(hexstr):
	return [int(el, 16) for el in hexstr.split(" ")]

def list_to_hexstring(l):
	return ''.join('{:02X} '.format(a) for a in l)


lengths = {
	0x01: "short",
	0x02: "long"
}

sources = {
	0x00: "microphone",
	0x02: "game",
	0x04: "chat",
	0x06: "auxiliary",
	0x08: "sampler",
	0x0A: "system"
}

sinks = {
	0x00: "stream",
	0x01: "chat",
	0x02: "alternate_usb",
	0x03: "sampler_out",
	0x04: "main_out",
	0x05: "headphones_out"
}

msg_types = {
	0x00: "patch",
	0x01: "vol_change",
	0x02: "button"
}

lengths = {
    "short":      0x01,
    "long":       0x02
}
sources = {
    "microphone": 0x00,
    "game":       0x02,
    "chat":       0x04,
    "auxiliary":  0x06,
    "sampler":    0x08,
    "system":     0x0A
}
sinks = {
    "stream":     0x00,
    "chat":       0x01,
    "alt_usb":    0x02,
    "sampler":    0x03,
    "main_out":   0x04,
    "phones_out": 0x05
}
msg_types = {
    "patch":      0x00,
    "vol_change": 0x01,
    "button":     0x02
}


def lookup_value(dictionary, needle):
	for key, value in dictionary.items():
		if (value == needle):
			return key


class MGMessage:         
	manufacturer_id = "00 01 05" 
	product_id = "43 00"

	def __init__(self, length, source, sink = "", msg_type ="", payload = []):
		if (length == None):
			self.initialise(source)
			return

		assert length in lengths.keys()
		assert source in sources.keys()
		assert sink in sinks.keys()
		assert msg_type in msg_types.keys()
		
		if (length == "short"):
			assert(len(payload) == 2)


		if (length == "long"):
			raise "Long messages unsupported"

		self.length = length
		self.source = source
		self.sink = sink
		self.msg_type = msg_type
		self.payload = payload


	def __str__(self):
		return "MGMessage of length {}. Action {} ({} | {}). Payload {}.".format(self.length, self.msg_type, self.source, self.sink, ' '.join("{:02X}".format(pad) for pad in self.payload))

	def __eq__(self, other):
		assert isinstance(other, MGMessage)
		
		

		return self.length   == other.length   and\
			   self.source   == other.source   and\
			   self.sink     == other.sink     and\
			   self.msg_type == other.msg_type and\
			   self.payload  == other.payload


	def compose_message(self):
		prologue = hexstring_to_list(self.manufacturer_id + " " + self.product_id)
		
		length_byte = lengths[self.length]
		source_byte = sources[self.source]
		sink_byte = sinks[self.sink]
		msg_type_byte = msg_types[self.msg_type]

		if (self.length == "short"):
			
			padding = [0x00] * 3
			
			proto_message = prologue + [length_byte, source_byte, sink_byte, msg_type_byte] + self.payload + padding

			return proto_message + [compute_checksum_value(proto_message)]

	def initialise(self, rmsg):
		msg = list(rmsg)
		assert msg[:3] == hexstring_to_list(self.manufacturer_id), "({} / {})".format(msg[:3], hexstring_to_list(self.manufacturer_id))
		assert msg[3:5] == hexstring_to_list(self.product_id), "({} / {})".format(msg[3:5], hexstring_to_list(self.product_id))
		assert compute_checksum(msg) == 0, compute_checksum(msg)

		contents = msg[5:]

		if (contents[0] == 0x01):
			self.length = "short"
			assert(len(contents) == 10)

			source_byte   = contents[1]
			sink_byte     = contents[2]
			msg_type_byte = contents[3]
			payload 	  = contents[4:6]
			padding		  = contents[6:9]
			checksum_val  = contents[9]

			assert source_byte in sources.values()
			assert sink_byte in sinks.values()
			assert msg_type_byte in msg_types.values()
			assert padding == [0x00, 0x00, 0x00], ("Padding contains values: " + ' '.join("{:02X}".format(pad) for pad in padding))

			self.source = lookup_value(sources, source_byte)
			self.sink = lookup_value(sinks, sink_byte)
			self.msg_type = lookup_value(msg_types, msg_type_byte)


			self.payload = payload
			

		elif (contents[0] == 0x02):
			self.length = "long"
			assert(len(contents) == 14)


		else:
			raise "Unsupported length value: 0x{:02X}".format(contents[0])



_testVal = MGMessage("short", "microphone", "main_out", "patch", [0x44, 0x73])

assert _testVal.compose_message() == hexstring_to_list("00 01 05 43 00 01 00 04 00 44 73 00 00 00 7b"), "{} / {}".format(_testVal, "00 01 05 43 00 01 00 04 00 44 73 00 00 00 7b")
assert MGMessage(None, _testVal.compose_message()) == _testVal, "{} / {}".format(MGMessage(None, _testVal.compose_message()), _testVal)