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
	"tiny":       0x00,
    "short":      0x01,
    "long":       0x02,
	"longer":     0x04,
	"bigger":     0x06,
	"huge":		  0x0B
}
sources = {
    "microphone": 0x00,
    "game":       0x02, # from PC
    "chat":       0x04, # from PC
    "auxiliary":  0x06,
    "sampler":    0x08, # from PC
    "system":     0x0A, # from PC
	
	"voicefx":	  0x0E,
	"muteaux":    0x0C,
	"banking":	  0x10,
	"button1":    0x14,
	"button2":    0x16,
	"button3":	  0x18,
	"button4":	  0x1A,
	"button5":    0x1C,
	"button6":    0x1E
}
sinks = {
    "stream":     0x00, # to PC
    "chat":       0x01, # to pc
    "alt_usb":    0x02, # to PC
    "sampler":    0x03, # to PC

    "main_out":   0x04,
    "phones_out": 0x05
}
msg_types = {
    "patch":      0x00,
    "vol_change": 0x01,
    "button":     0x02,
	"voicefx":	  0x04,
	"voicefx2":   0x07,
	"voicefx3":	  0x08
}


def lookup_value(dictionary, needle):
	for key, value in dictionary.items():
		if (value == needle):
			return key


class MGMessage:         
	manufacturer_id = "00 01 05" 
	product_id = "43"

	def __init__(self, length, source, sink = "", msg_type ="", payload = [], success=0x00):
		if (length == None):
			self.initialise(source)
			return

		assert length in lengths.keys()
		assert source in sources.keys()
		assert sink in sinks.keys()
		assert msg_type in msg_types.keys()
		
		if (length == "tiny"):
			assert len(payload) == 2

		if (length == "short"):
			assert len(payload) == 5
	
		if (length == "long"):
			assert len(payload) == 7
		
		if (length == "bigger"):
			assert len(payload) == 27

		if (length == "huge"):
			assert len(payload) == 45
		


		self.success_byte = success
		self.length = length
		self.source = source
		self.sink = sink
		self.msg_type = msg_type
		self.payload = payload
		

	def __str__(self):
		return "MGMessage of length {}. Status {}. Action {} ({} | {}). Payload {}.".format(self.length, "{:02X}".format(self.success_byte), self.msg_type, self.source, self.sink, ' '.join("{:02X}".format(pad) for pad in self.payload))

	def __eq__(self, other):
		assert isinstance(other, MGMessage)
		
		

		return self.success_byte  == other.success_byte and\
			   self.length        == other.length       and\
			   self.source        == other.source       and\
			   self.sink          == other.sink         and\
			   self.msg_type      == other.msg_type     and\
			   self.payload       == other.payload


	def compose_message(self):
		prologue = hexstring_to_list(self.manufacturer_id + " " + self.product_id)
		
		length_byte = lengths[self.length]
		source_byte = sources[self.source]
		sink_byte = sinks[self.sink]
		msg_type_byte = msg_types[self.msg_type]

		if (self.length == "short"):
			
			
			proto_message = prologue + [self.success_byte, length_byte, source_byte, sink_byte, msg_type_byte] + self.payload

			return proto_message + [compute_checksum_value(proto_message)]

	def initialise(self, rmsg):
		msg = list(rmsg)
		assert msg[:3] == hexstring_to_list(self.manufacturer_id), "({} / {})".format(msg[:3], hexstring_to_list(self.manufacturer_id))
		assert [msg[3]] == hexstring_to_list(self.product_id), "({} / {})".format([msg[3]], hexstring_to_list(self.product_id))
		assert compute_checksum(msg) == 0, compute_checksum(msg)

		self.success_byte = msg[4]

		contents = msg[5:]
		
		assert contents[0] in lengths.values(), contents[0]
		

		if (contents[0] == 0x00):
			self.length = "tiny"
			assert len(contents) == 6 

			source_byte   = contents[1]
			sink_byte     = contents[2]
			msg_type_byte = contents[3]
			payload       = contents[4]
			checksum_val  = contents[5]

			assert source_byte in sources.values()
			assert sink_byte in sinks.values()
			assert msg_type_byte in msg_types.values()

			self.source = lookup_value(sources, source_byte)
			self.sink = lookup_value(sinks, sink_byte)
			self.msg_type = lookup_value(msg_types, msg_type_byte)
			

			self.payload = [payload]


		if (contents[0] == 0x01):
			self.length = "short"
			assert len(contents) == 10

			source_byte   = contents[1]
			sink_byte     = contents[2]
			msg_type_byte = contents[3]
			payload 	  = contents[4:9]
			#padding       = contents[7:9]
			checksum_val  = contents[9]

			assert source_byte in sources.values()
			assert sink_byte in sinks.values()
			assert msg_type_byte in msg_types.values()
			#assert padding == [0x00, 0x00], ("Padding contains values: " + ' '.join("{:02X}".format(pad) for pad in padding))

			self.source = lookup_value(sources, source_byte)
			self.sink = lookup_value(sinks, sink_byte)
			self.msg_type = lookup_value(msg_types, msg_type_byte)


			self.payload = payload
			

		elif (contents[0] == 0x02):
			self.length = "long"
			assert(len(contents) == 14)

			source_byte   = contents[1]
			sink_byte     = contents[2]
			msg_type_byte = contents[3]
			payload 	  = contents[4:11]
			padding		  = contents[11:13]
			checksum_val  = contents[13]

			assert source_byte in sources.values()
			assert sink_byte in sinks.values()
			assert msg_type_byte in msg_types.values()
			assert padding == [0x00] * 2, ("Padding contains values: " + ' '.join("{:02X}".format(pad) for pad in padding))

			self.source = lookup_value(sources, source_byte)
			self.sink = lookup_value(sinks, sink_byte)
			self.msg_type = lookup_value(msg_types, msg_type_byte)


			self.payload = payload
		
		elif (contents[0] == 0x06):
			self.length = "bigger"
			assert(len(contents) == 30)

			source_byte   = contents[1]
			sink_byte     = contents[2]
			msg_type_byte = contents[3]
			payload 	  = contents[4:29]
			#padding		  = contents[11:13]
			checksum_val  = contents[29]

			assert source_byte in sources.values()
			assert sink_byte in sinks.values()
			assert msg_type_byte in msg_types.values()
			#assert padding == [0x00] * 2, ("Padding contains values: " + ' '.join("{:02X}".format(pad) for pad in padding))

			self.source = lookup_value(sources, source_byte)
			self.sink = lookup_value(sinks, sink_byte)
			self.msg_type = lookup_value(msg_types, msg_type_byte)


			self.payload = payload

		elif (contents[0] == 0x04):
			self.length = "longer"
			assert(len(contents) == 22)

			source_byte   = contents[1]
			sink_byte     = contents[2]
			msg_type_byte = contents[3]
			payload 	  = contents[4:21]
			#padding		  = contents[11:13]
			checksum_val  = contents[21]

			assert source_byte in sources.values()
			assert sink_byte in sinks.values()
			assert msg_type_byte in msg_types.values()
			#assert padding == [0x00] * 2, ("Padding contains values: " + ' '.join("{:02X}".format(pad) for pad in padding))

			self.source = lookup_value(sources, source_byte)
			self.sink = lookup_value(sinks, sink_byte)
			self.msg_type = lookup_value(msg_types, msg_type_byte)


			self.payload = payload


		elif (contents[0] == 0x0B):
			self.length = "huge"
			assert(len(contents) == 50)

			source_byte   = contents[1]
			sink_byte     = contents[2]
			msg_type_byte = contents[3]
			payload 	  = contents[4:49]
			#padding		  = contents[11:13]
			checksum_val  = contents[49]

			assert source_byte in sources.values()
			assert sink_byte in sinks.values()
			assert msg_type_byte in msg_types.values()
			#assert padding == [0x00] * 2, ("Padding contains values: " + ' '.join("{:02X}".format(pad) for pad in padding))

			self.source = lookup_value(sources, source_byte)
			self.sink = lookup_value(sinks, sink_byte)
			self.msg_type = lookup_value(msg_types, msg_type_byte)


			self.payload = payload


_testVal = MGMessage("short", "microphone", "main_out", "patch", [0x44, 0x73, 0x00, 0x00, 0x00])

assert _testVal.compose_message() == hexstring_to_list("00 01 05 43 00 01 00 04 00 44 73 00 00 00 7b"), "{} / {}".format(list_to_hexstring(_testVal.compose_message()), "00 01 05 43 00 01 00 04 00 44 73 00 00 00 7b")
assert MGMessage(None, _testVal.compose_message()) == _testVal, "{} / {}".format(MGMessage(None, _testVal.compose_message()), _testVal)