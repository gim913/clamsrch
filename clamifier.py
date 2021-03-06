#!/usr/bin/env python
#
# vim: tabstop=4 shiftwidth=4 noexpandtab foldmethod=indent
#

import sys
import bisect

sys.path.append('pycrc-0.7.10')

from crc_algorithms import Crc

#fp = open("temp.dat", "w")
#def debugRewrite(msg):
#	fp.write(msg)

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

	def isSimple(self):
		return not (self.isCrc or self.isLog)

	def __str__(self):
		ret = ""
		if self.isCrc: ret += "CRC:"
		if self.isAnd: ret += "AND:"
		if self.isLog: ret += "LOGIC:"
		if self.isString: ret += "STRING:"
		if self.isAscii: ret += "ASCII:"
		ret += ','.join(map(str, self.values.keys()))
		return ret

class DummyData:
	def __init__(self, values, neg):
		self.values = values
		self.neg = neg

class DataParser:
	def __init__(self, typeDesc, dataLines):
		self.values = []
		self.typeDesc = typeDesc
		self.big = 0
		self.neg = False
		for line in dataLines:
			line = line.strip()
			if not len(line):
				continue

			if self.typeDesc.isString:
				self.parseString(line)
			elif self.typeDesc.isAscii:
				self.parseAscii(line)
			else:
				self.parseNumbers(line)
		if not len(self.values):
			raise DataException('error, signature does not contain any data')

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

			self.neg = self.neg or (val < 0)
			self.big = max(self.big, abs(val))
			self.values.append(val)
	
	def strString(self):
		ret = ""
		for idx,elem in enumerate(self.values):
			if idx%32 == 0:
				ret += "\""
			if 0 == elem:
				ret += "\\0"
			elif -1 != '"\\'.find(chr(elem)):
				ret += "\\"+chr(elem)
			else:
				ret += chr(elem)
			if (idx+1)%32 == 0:
				ret += "\"\n"
		if (idx+1)%32 != 0:
			ret += "\"\n"
		return ret
	
	def strAscii(self):
		ret = ""
		for idx,elem in enumerate(self.values):
			if -1 != "'\\".find(chr(elem)):
				ret += "'\\"+chr(elem)+"',"
			else:
				ret += "'"+chr(elem)+"',"
			if (idx+1)%16 == 0:
				ret += "\n"
		if (idx+1)%16 != 0:
			ret += "\n"
		return ret

	def strNumbers(self):
		idx = bisect.bisect([0x100L, 0x10000L, 0x100000000L, 0x10000000000000000L], self.big)
		Width = [(2, 3+1), (4, 5+1),  (8, 10+1), (16, 20+1)][idx]
		ret = ""
		form = "%*d," if self.neg else "0x%0*x,"
		elWidth = Width[1] if self.neg else Width[0]

		for idx,elem in enumerate(self.values):
			ret += (form % (elWidth, elem))
			if (idx+1)%(64 / Width[0]) == 0:
				ret += "\n"
		if (idx+1)%(64 / Width[0]) != 0:
			ret += "\n"
		return ret

	def __str__(self):
		if self.typeDesc.isString:
			return self.strString()
		elif self.typeDesc.isAscii:
			return self.strAscii()
		return self.strNumbers()

def bswap(val, bits):
	if bits == 16:
		return ((val >> 8) | ((val&0xffL) << 8))
	elif bits == 32:
		temp1 = bswap(val&0xffffL, 16)
		temp2 = bswap((val>>16)&0xffffL, 16)
		return ((temp1<<16) | temp2)
	else:
		temp1 = bswap( val&0xffffffffL, 32 )
		temp2 = bswap( (val>>32)&0xffffffffL, 32 )
		return ((temp1<<32) | temp2)

Little_Endian = 0
Big_Endian = 1
class SigParser:
	def __init__(self, ndb, ldb, sig, lineNumber):
		self.sig = sig
		self.sigLineNumber = lineNumber
		self.ndb = ndb
		self.ldb = ldb

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

		#debugRewrite("TITLE:"+self.title.replace(';',':')+"\n\n")
		#debugRewrite("TYPE:"+str(self.typeDesc)+"\n")
		#debugRewrite("DATA:\n");
		#debugRewrite(str(self.data));
		#debugRewrite("\n----\n\n")

		if self.typeDesc.isSimple():
			for bitWidth in self.typeDesc.values:
				# lil endian
				b,l = self.dumpData(bitWidth, Little_Endian, self.data)
				self.generateSigName(self.ndb, bitWidth, Little_Endian, b, l)

				if bitWidth == 8:
					continue

				# big endian
				b,l = self.dumpData(bitWidth, Big_Endian, self.data)
				self.generateSigName(self.ndb, bitWidth, Big_Endian, b, l)

		# currently if "CRC:" is specified only one width is allowed
		elif self.typeDesc.isCrc:
			for Do_Reflect in [True, False]:
				bitWidth = self.typeDesc.values.keys()[0]
				crc = Crc(width = bitWidth, poly = self.data.values[0], reflect_in = Do_Reflect, xor_in = 0, reflect_out = Do_Reflect, xor_out = 0)
				dummyData = DummyData(crc.gen_table(), False)

				b,l = self.dumpData(bitWidth, Little_Endian, dummyData)
				self.generateCrcSigName(bitWidth, Little_Endian, Do_Reflect, b)
				if bitWidth != 8:
					b,l = self.dumpData(bitWidth, Big_Endian, dummyData)
					self.generateCrcSigName(bitWidth, Big_Endian, Do_Reflect, b)

		elif self.typeDesc.isLog:
			for bitWidth in self.typeDesc.values:
				if bitWidth == 8:
					print "\n [!] WARNING, generated byte-based logical signatures is a bad, BAD idea\n"
				b = self.dumpLogicalSignature(bitWidth, Little_Endian, self.data)
				self.generateSigName(self.ldb, bitWidth, Little_Endian, b, 0)

				if bitWidth != 8:
					b = self.dumpLogicalSignature(bitWidth, Big_Endian, self.data)
					self.generateSigName(self.ldb, bitWidth, Big_Endian, b, 0)

	def generateCrcSigName(self, bitWidth, mode, reflect, sig):
		if bitWidth == 8:
			self.ndb.write(self.title + (" [%d.byt.refl=%s]" % (bitWidth, reflect)) )
		else:
			self.ndb.write(self.title + (" [%d.%s.refl=%s]" % (bitWidth, ['lil','big'][mode], reflect)))
		self.ndb.write(sig)
		self.ndb.write("\n")

	#
	# Format of signame: name [width.(byt|lil|big)(.STR|.ASC).(length|AND)]
	#
	def generateSigName(self, writer, bitWidth, mode, sig, sigLen):
		sigName = self.title
		sigName += (" [%d." % bitWidth)
		if bitWidth == 8:
			sigName += "byt."
		elif mode == Little_Endian:
			sigName += "lil."
		elif mode == Big_Endian:
			sigName += "big."

		if self.typeDesc.isString:
			sigName += "STR."
		elif self.typeDesc.isAscii:
			sigName += "ASC."

		if self.typeDesc.isAnd:
			sigName += "AND]"
		elif self.typeDesc.isLog:
			sigName += "LOGIC]"
		else:
			sigName += ("%d]" % sigLen);

		writer.write(sigName)
		writer.write(sig)
		writer.write("\n")

	def dumpData(self, bitWidth, mode, dataObj):
		buff=""
		bufLen = 0
		Max_Val = (1L << bitWidth)
		for idx, elem in enumerate(dataObj.values):
			form = "%0*x"
			if dataObj.neg:
				if elem < 0:
					if -elem > Max_Val / 2:
						print " [-] warning overflow found in sig: ", self.title
						elem &= (Max_Val-1)
					elem = Max_Val + elem
					elem &= (Max_Val-1)
				# just to make them distinguishable
				form = "%0*X"

			# yes this is correct, we need to swap, when 
			# there is Little_Endian specified (cause we're just printing, the way it is)
			if (mode == Little_Endian) and (bitWidth != 8):
				elem = bswap(elem, bitWidth)
			
			tempBuf = form % (bitWidth / 4, elem)
			buff += tempBuf
			bufLen += len(tempBuf)

			# avoid adding it to last elem
			if self.typeDesc.isAnd and (idx != len(dataObj.values)-1):
				buff += "{-20}"

			if bufLen % 2:
				print " [-] warning, error occured while adding signature: ", self.title, " (isneg:",dataObj.neg,")"
				break

			if len(buff) > 1023*16:
				print " [-] warning, truncating signature: ",self.title,"to",(len(buff)/2)," bytes"
				break

		prefix = ":0:*:"
		return (prefix + buff, len(buff)/2)

	#
	# pass data as an argument just in case if I'd like
	# to make some other use of that
	#
	def dumpLogicalSignature(self, bitWidth, mode, dataObj):
		if dataObj.neg:
			raise DataException('negative values in logical clauses unsupported')

		logData = {}
		Max_Val = (1L << bitWidth)
		for el in dataObj.values:
			if el in logData:
				logData[el] += 1
			else:
				logData[el] = 1

		# the following code relies on the property, 
		# that in both of the loops, iterator will return elements
		# in the same order...
		clauses = []
		for idx,item in enumerate(logData.iteritems()):
			count = item[1]
			if count > 1:
				clauses.append( "(%d>%d)" % (idx, count) )
			else:
				clauses.append( "%d" % idx )
		logicClause = '&'.join(clauses)

		elements = []
		form = "%0*x"
		for elem,count in logData.iteritems():
			if (mode == Little_Endian) and (bitWidth != 8):
				elem = bswap(elem, bitWidth)
				
			elements.append( form % (bitWidth / 4, elem) )

		subClause = ';'.join(elements)

		prefix = ";Target:0;"
		return (prefix + logicClause + ";" + subClause)

class DbParser:
	def __init__(self, filename, ndbName, ldbName):
		self.fd = open(filename, "r")
		self.ndb = open(ndbName, "w")
		self.ldb = open(ldbName, "w")

	def __del__(self):
		self.fd.close()
		self.ndb.close()
		self.ldb.close()

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
				sp = SigParser(self.ndb, self.ldb, sig, sigLine)
				sp.parse()
				sig = []
				counter += 1
				sigLine = lineNo+1
#				print "\r",counter,
		return 0

p = DbParser("sigbase.sig", "clamsrch.ndb", "clamsrch.ldb")
p.parse()

#fp.close()

