from datetime import datetime
from termcolor import cprint, colored

import colorama
colorama.init()

def n_logging(text):
	print("{} {}".format(b_(), text))

def c_logging(value, colour):
	text = colored(value, colour)
	print("{} {}".format(b_(), text))

def c_print(value, colour):
	text = colored(value, colour)
	print(text)

def b_():
    timestamp = str("["+datetime.now().strftime("%H:%M:%S.%f")[:-3]+"]")
    return timestamp

def stamp():
	timestamp = datetime.now().strftime("%H:%M:%S")
	return timestamp