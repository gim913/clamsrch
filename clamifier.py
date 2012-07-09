#!/usr/bin/env python
#
# vim: tabstop=4 shiftwidth=4 noexpandtab 
#

fp = open("temp.dat", "w")
def debugRewrite(msg):
	fp.write(msg)

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

	def __str__(self):
		ret = ""
		if self.isCrc: ret += "CRC:"
		if self.isAnd: ret += "AND:"
		if self.isLog: ret += "LOGIC:"
		if self.isString: ret += "STRING:"
		if self.isAscii: ret += "ASCII:"
		ret += ','.join(map(str, self.values.keys()))
		return ret

class DataParser:
	def __init__(self, typeDesc, dataLines):
		self.values = []
		for line in dataLines:
			line = line.strip()
			if not len(line):
				continue

			if typeDesc.isString:
				self.parseString(line)
			elif typeDesc.isAscii:
				self.parseAscii(line)
			else:
				self.parseNumbers(line)
		if not len(self.values):
			raise DataException('dummy')

	def parseString(self, line):
		idx = 1

		# if idx overflow it doesn't really matter, cause it means
		# string wasn't properly terminated, exception will be
		# raised, and I'm happy with that :P
		#
		while line[idx] != '"':
			if line[idx] == '\\':
				idx += 1
				if line[idx] == '0':
					self.values.append( long(0) )
				elif line[idx] == '\\':
					self.values.append( long(ord(line[idx])) )
				else:
					raise DataException('unsupported escaped character [\\%c] in string: %s' % (line[idx], line))
			else:
				self.values.append( long(ord(line[idx])) )
			idx += 1

	def parseAscii(self, line):
		idx = 0
		Opening,Want_Data,Closing,Skip_Separator = 0,1,2,3
		state = Opening
		# and yes, I know I could do that with few lines using re.
		# but I want to have some more-or-less sensible errors
		while idx < len(line):
			if state == Opening:
				if line[idx] != "'":
					raise DataException('was waiting for opening apostrophe')
				state = Want_Data
			elif state == Want_Data:
				if line[idx] == '\\':
					idx += 1
					if -1 != "'\\".find(line[idx]):
						self.values.append( long(ord(line[idx])) )
					else:
						raise DataException('not handled yet ['+line[idx]+']')
				else:
					self.values.append( long(ord(line[idx])) )
				state = Closing
			elif state == Closing:
				if line[idx] != "'":
					raise DataException('was waiting for closing apostrophe')
				state = Skip_Separator
			elif state == Skip_Separator:
				if -1 != " ,".find(line[idx]):
					pass
				elif line[idx] == "'":
					state = Opening
					continue # !!!
				else:
					raise DataException('unexpected data ['+line+']')
			idx += 1

	def parseNumbers(self, line):
		for number in line.split(','):
			cleanNumber = number.strip()
			if not len(cleanNumber):
				continue

			if cleanNumber[0:2] == "0x":
				val = long(cleanNumber, 16)
			else:
				val = long(cleanNumber, 10)
			self.values.append(val)
	
	def __str__(self):
		return ""

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
		try:
			self.data = DataParser(self.typeDesc, data)
		except DataException as de:
			raise DataException('error in data of signature at line ' + str(self.sigLineNumber) + ' named: ' + self.title + ' child info:' + de.value)

		debugRewrite("TITLE:"+self.title.replace(';',':')+"\n\n")
		debugRewrite("TYPE:"+str(self.typeDesc)+"\n")
		debugRewrite("DATA:\n");
		debugRewrite(str(self.data));
		debugRewrite("\n----\n\n")


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

fp.close()
