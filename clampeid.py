#!/usr/bin/env python
#
# vim: tabstop=4 shiftwidth=4 noexpandtab foldmethod=indent
#

class DataException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class SigParser:
	def __init__(self, ndb, lineNumber):
		self.sigLineNumber = lineNumber
		self.ndb = ndb
		self.title = None
		self.signature = None
		self.ep = None

	def parse(self, line):
		if len(line) < 5:
			return

		if line[0] == '[':
			self.title = line[1:-1].replace(':', ';')
		elif line[0:9] == 'signature':
			if line [0:12] == 'signature = ':
				self.signature = line[12:]
			else:
				raise DataException("incorrect data")
		elif line[0:9] == "ep_only =":
			if line == "ep_only = true":
				self.ep = True
			elif line == "ep_only = false":
				self.ep = False
			else:
				raise DataException("ep_only has bad format")

	def flush(self):
		self.ndb.write(self.title)
		if self.ep == True:
			self.ndb.write(':1:EP+0:')
		else:
			self.ndb.write(':1:*:')
		self.ndb.write(self.signature.replace(' ', ''))
		self.ndb.write('\n')

class DbParser:
	def __init__(self, filename, ndbName):
		self.fd = open(filename, "r")
		self.ndb = open(ndbName, "w")

	def __del__(self):
		self.fd.close()
		self.ndb.close()

	def parse(self):
		lineNo  = 0
		sigLine = 1
		sp = None
		while True:
			line = self.fd.readline()
			if not line:
				break
			line = line.strip()
			lineNo += 1
			if len(line) and line[0] == '[':
				if sp:
					sp.flush()

				sp = SigParser(self.ndb, lineNo)
			if sp:
				sp.parse(line)
		if sp:
			sp.flush()

p = DbParser("userdb.txt", "clampeid.ndb")
p.parse()

