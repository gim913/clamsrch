#!/usr/bin/env python
#
# vim: tabstop=4 shiftwidth=4 noexpandtab 
#

class TypeDesc:
	def __init__(self, desc):
		self.desc = desc

	def parse(self):
		print self.desc

class SigParser:
	def __init__(self, sig):
		self.sig = sig

	def parse(self):
		for s in self.sig:
			if s[0:6] == "TITLE:":
				self.title = s[6:].replace(':', ';')
				continue
			if s[0:5] == "TYPE:":
				self.typeDesc = TypeDesc(s[5:])
				self.typeDesc.parse()
				continue

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
				sp.parse()
				sig = []
				counter += 1
#				print "\r",counter,
		return 0

p = DbParser("sigbase.sig")
p.parse()

