#! /usr/bin/python

def compute_checksum_value(vals):
	return 128 - (sum(vals) % 128)

def compute_checksum(vals):
	return sum(vals) % 128


def hexstring_to_list(hexstr):
	return [int(el, 16) for el in hexstr.split(" ")]

def list_to_hexstring(l):
	return ''.join('{:02X} '.format(a) for a in l)

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
	0x02: "alternate usb",
	0x03: "sampler out",
	0x04: "main out",
	0x05: "headphones out"
}

msg_types = {
	0x00: "patch/unpatch sink to source",
	0x01: "slider/volume change",
	0x02: "button pushed"
}

def compose_message(msg_length, source, sink, msg_type, payload):
	manufacturer_id = "00 01 05" 
	product_id = "43 00"
	
	prologue = hexstring_to_list(manufacturer_id + " " + product_id)
	
	lenByte = []
	
	if (msg_length == "short"):
		lenByte.append(0x01)
	elif (msg_length == "long"):
		lenByte.append(0x02)
		raise "Long messages unsupported"
	else:
		raise "Invalid length argument"
	


	assert(source in sources.keys())

	assert(sink in sinks.keys())
	
	assert(msg_type in msg_types.keys())

	if (msg_length == "short"):
		assert(len(payload) == 2)
		padding = [0x00] * 3
		
		proto_message = prologue + lenByte + [source, sink, msg_type] + payload + padding

		return proto_message + [compute_checksum_value(proto_message)]




msg = compose_message("short", 0x04, 0x03, 0x00, [0x44, 0x73])

print(list_to_hexstring(msg))
print("checksum: ", compute_checksum(msg), "fail" if compute_checksum(msg) else "pass")


