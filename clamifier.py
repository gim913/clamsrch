#!/usr/bin/env python
#
# vim: tabstop=4 shiftwidth=4 noexpandtab 
#

class SigParser:
	def __init__(self, sig):
		pass

class DbParser:
	def __init__(self, filename):
		self.fd = open(filename, "r")

	def parse(self):
		sig = []
		counter = 0
		while True:
			line = self.fd.readline()
			if not line:
				break
			line = line.strip()
			if line != "----":
				sig.append(line)
			else:
				sp = SigParser(sig)
				sig = []
				counter += 1
				print "\r",counter,
		return 0

p = DbParser("sigbase.sig")
p.parse()

