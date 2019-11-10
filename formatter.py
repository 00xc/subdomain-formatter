import sys
import argparse

__author__ = "https://github.com/00xc/"
__version__ = "0.1a"

def read_inputs(info, opts, h, defaults, mvar):
	parser = argparse.ArgumentParser(description=info)
	for default, o, htext, mtext in zip(defaults, opts, h, mvar):
		if isinstance(default, bool):
			if default == True: action = "store_false"
			else: action = "store_true"
			parser.add_argument("-"+o, help=htext, default=default, action=action)
		else:
			if default==None: req = True
			else: req = False
			parser.add_argument("-"+o, help=htext, default=default, required=req, metavar=mtext)
	args = parser.parse_args()
	return args

def tabprint(s, level):
	global prev, paragraph, b

	if paragraph and prev>level: front="\n"
	else: front = ""

	print(front + "\t"*(level-b) + s)
	prev = level

def main(domains, match, level):
	toprint = list()
	for c in domains:
		if len(c) == (level+1) and c[-level:] == match:
			toprint.append(c)

	toprint.sort()
	for c in toprint:
		tabprint(".".join(c), level+1)
		main(domains, c, level+1)

def fill_gaps(domains, base_level, max_level, level):
	if level > max_level: return domains

	for d in domains:
		if len(d) == level:
			parent = d[-(level-1):]
			if parent not in domains:
				domains.append(parent)

	domains = fill_gaps(domains, base_level, max_level, level+1)
	return domains

if __name__ == '__main__':
	
	# Read options
	info = "Subdomain formatter v{}".format(__version__)
	opts = ["i", "b", "p"]
	h = ["Input file with a list of subdomains.", "Base domain.", "Flag: switch on paragraphed style."]
	defaults = [None, "", False]
	mvar = ["input_file", "base_domain", ""]
	args = read_inputs(info, opts, h, defaults, mvar)

	# Read input file
	domains = set()
	try:
		with open(args.i, "r") as f:
			for line in f:
				line = line.rstrip()
				if line.count("://")>0:
					line = line.split("://", 1)[1]
				line = tuple(line.split("."))
				domains.add(line)
		domains = list(domains)
	except FileNotFoundError:
		sys.exit("[-] Input file not found")

	# Base domain
	if args.b != "":
		args.b = args.b.split("://")[-1]
		args.b = tuple(args.b.split("."))
	else:
		args.b = tuple(min(domains, key=len))[-2:]

	# Add intermediate subdomains
	domains = fill_gaps(domains, len(args.b), max([len(x) for x in domains]), len(args.b)+1)

	# Parameters for the tabprint() function
	global prev, paragraph, b
	prev = len(args.b)
	paragraph = args.p
	b = len(args.b)

	# Print base domain and recursively print subdomains
	tabprint(".".join(args.b), len(args.b))
	main(domains, args.b, len(args.b))
