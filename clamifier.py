#!/usr/bin/env python
#
# vim: tabstop=4 shiftwidth=4 noexpandtab 
#

class DataException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
	
class TypeDesc:
	def __init__(self, desc):
		self.isAnd = False
		self.isCrc = False
		self.isLog = False
		self.isString = False
		self.isAscii = False 
		self.values = {}

		for elem in desc.split(':'):
			elem = elem.strip()
			if elem == 'AND':
				self.isAnd = True
			elif elem == 'CRC':
				self.isCrc = True
			elif elem == 'LOGIC':
				self.isLog = True
			elif elem == 'STRING':
				self.isString = True
			elif elem == 'ASCII':
				self.isAscii = True
			else:
				for val in elem.split(','):
					self.values[int(val)] = 1
		print self.values, desc

class DataParser:
	def __init__(self, dataLines):
		self.data = dataLines
		for line in dataLines:
			line = line.strip()
			if not len(line):
				continue

			if line[0] == '"':
				parseString(line)
			elif line[0] == "'":
				parseAscii(line)
			else:
				parseNumbers(line)
		raise DataException('dummy')

	def parseString(self, line):
		pass

	def parseAscii(self, line):
		pass

	def parseNumbers(self, line):
		pass

class SigParser:
	def __init__(self, sig, lineNumber):
		self.sig = sig
		self.sigLineNumber = lineNumber

	def parse(self):
		data = None
		self.title = '[empty]'
		for idx,s in enumerate(self.sig):
			if s[0:6] == "TITLE:":
				self.title = s[6:].replace(':', ';')
				continue
			if s[0:5] == "TYPE:":
				self.typeDesc = TypeDesc(s[5:])
				continue
			if s[0:5] == "DATA:":
				data = self.sig[idx+1:]
				continue
		if not data:
			raise DataException('error in data of signature at line ' + str(self.sigLineNumber) + ' named: ' + self.title)
		self.data = DataParser(data)

class DbParser:
	def __init__(self, filename):
		self.fd = open(filename, "r")

	def parse(self):
		sig = []
		counter = 0
		lineNo  = 0
		sigLine = 1
		while True:
			line = self.fd.readline()
			if not line:
				break
			line = line.strip()
			lineNo += 1
			if line != "----":
				sig.append(line)
			else:
				sp = SigParser(sig, sigLine)
				sp.parse()
				sig = []
				counter += 1
				sigLine = lineNo+1
#				print "\r",counter,
		return 0

p = DbParser("sigbase.sig")
p.parse()

