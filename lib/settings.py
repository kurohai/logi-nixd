import json
import os
import sys
from pprint import pprint
from dicto import dicto
import binascii


config_file = './config.json'
config_stream = open(config_file, 'rb')
config = dicto(json.load(config_stream))
g510 = dicto(config.g510)

# json can't handle hex
# this converts the vendor and device id from str to hex
g510.vendor_id = hex(int(g510.vendor_id))
g510.device_id = hex(int(g510.device_id))
