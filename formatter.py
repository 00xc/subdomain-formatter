import sys
import argparse
from collections import namedtuple

__author__ = "https://github.com/00xc/"
__version__ = "0.1c"

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
	global prev

	if paragraph and prev>level: front="\n"
	else: front = ""

	print(front + "\t"*(level-b) + s)
	prev = level

def main(domains, match, level):
	toprint = list()
	for c in domains:
		if len(c.domain) == (level+1) and c.domain[-level:] == match:
			toprint.append(c)

	for c in sorted(toprint, key=lambda x: x.domain):
		tabprint(".".join(c.domain) + ("" if not c.added else " *"), level+1)
		main(domains, c.domain, level+1)

def fill_gaps(domains, base_level, level):
	if level == base_level: return domains

	fill_domains = set()

	for d in domains:
		if len(d.domain) == level:
			parent = domain_tuple(d.domain[-(level-1):], True)
			if parent.domain not in [dd.domain for dd in domains]:
				fill_domains.add(parent)

	domains.update(fill_domains)
	return fill_gaps(domains, base_level, level-1)

if __name__ == '__main__':
	
	# Read options
	info = "Subdomain formatter v{}".format(__version__)
	opts = ["i", "b", "p"]
	h = ["Input file with a list of subdomains.", "Base domain.", "Flag: switch on paragraphed style."]
	defaults = [None, "", False]
	mvar = ["input_file", "base_domain", ""]
	args = read_inputs(info, opts, h, defaults, mvar)

	domain_tuple = namedtuple("domain_tuple", ["domain", "added"])

	domains = set()
	try:
		with open(args.i, "r") as f:
			for line in f:
				line = line.rstrip().lstrip()
				if "://" in line:
					line = line = split("://", 1)[1]

				domains.add(domain_tuple(
					tuple(line.split(".")),
					False
				))
	except FileNotFoundError:
		sys.exit("[-] Input file not found")

	if len(args.b) > 0:
		args.b = args.b.split("://", 1)[1]
		args.b = tuple(args.b.split("."))
	else:
		args.b = min(domains, key=lambda e: len(e.domain)).domain[-2:]

	domains = fill_gaps(domains=domains, base_level=len(args.b), level=max(len(x.domain) for x in domains))

	# Parameters for the tabprint() function
	prev = len(args.b)
	paragraph = args.p
	b = len(args.b)

	# Print base domain and recursively print subdomains
	tabprint(".".join(args.b), len(args.b))
	main(domains, args.b, len(args.b))
