#!/usr/bin/python

#
# Representation of data in Skype
#

import dpkt

class ObjectHeader(dpkt.Packet):
	__hdr__ =	(
			('length', 'B', 0x00),
			)

	def parse(self):
		self.byte1 = 0x00
		self.byte1_present = ord(self.data[0]) & 0x30 == 0
		if self.byte1_present:
			self.byte1 = ord(self.data[0])
			self.data = self.data[1:]

		# byte2 is always present
		self.byte2 = ord(self.data[0])
		self.data = self.data[1:]

		self.byte3 = 0x00
		self.byte3_present = self.byte2 & 0x80 != 0
		if self.byte3_present:
			self.byte3 = ord(self.data[0])
			self.data = self.data[1:]

		self.id = '\x00\x00'
		self.id_present = self.byte2 & 0x02 != 0
		if self.id_present:
			self.id = self.data[:2]
			self.data = self.data[2:]

CONTENT_TYPE_CONTAINER	= 0x41
CONTENT_TYPE_DATA	= 0x42

class ObjectContent(dpkt.Packet):
	__hdr__ =	(
			('type', 'B', 0x00),
			)


if __name__ == "__main__":
	#
	# run some tests as demo
	#

	from utils import *
	from time import sleep

	def convert(p):
		return hexstr2bytestr( p.replace(' ', '') )

	testpkts = []
	testpkts.append(convert('07    7b    97be 41 01000101'))
	testpkts.append(convert('14    72    97b8 42 f622e605fa670b8506d3733d17e88329fb'))
	testpkts.append(convert('12    72    9853 42 f62308 42 31e64fad64b34b6b1e9876'))
	testpkts.append(convert('a6 03 7b    97b8 41 020500 41 02040b88030000010400000001 41 b53f5f66241b0c8a50309a4cba4cf29d654342672bbd4f989c6a98787995fba8f22eda673cff6848ce82093e37d076d4c5ccee59f9dd49723fe59036fae5fd6bdfc8a0a6b796ae90e4cdb5b0c84e80e350cb379e9a9bb36f9a7fa718d9e80ad8ee66af7676dd7ecdb8bdba2b6ce15960013446638456760b7a3f3e842ca83c644481e7c7f2c00378760d0c87254d96174da125228768eee8ff5f7c2a1596661c69f27a323bcfc9cdf890e351c93c141ebad411f8926abde35986bec356a35243e39385f88cf9ab87df7adc5388fe515ccbb09856f96f041d67722baab746140875ec4cd734ee395f2e52e9412575d50231b190d5cde15d1cc7766f980dbfd7a068b1c56df7c848068267cdd4e1e8e55f6e3d788fc6ac6b7708264cfc672a62eaacf0eff4cc226012890f6e1fc31862cc3bdad348c6022c84fb206cf22149e42413a3e59fa41bd8bd62a32d5ef664ea107f5d80f7b2dda852da8ba1495d8f39e281a542925ee8e62553ac4b348e97861216ee369fa05ee72a9294597afb834f0310646965676f2e66617272656e00000101'))
	testpkts.append(convert('07    9b 01 97b0 41 01000101'))
	testpkts.append(convert('1e    92 01 97ac 42 f622fd 40 454d31619b7f18648c31ed131bc8b7be871086ec7d4a2b'))
	testpkts.append(convert('05    d9 02      42 b517f484'))
	testpkts.append(convert('48 c1 ad 06      42 e9b11f90d226ea51e0392418b6040863c018ce14ac3955cc8829c7c9b62651c6472f5f594946a6c03926064dd87a6c0e9997348a5e4efd7e500bbb327f8376a3dd6fdce693ffff'))
	testpkts.append(convert('f2 04 eb 02 985f 41 2002115377d386110f051a4109000034000204000304000468000a6403104e4c000011030012800100210202115eaf11897c61051a410800003400020000030000043d000a630310474200001290010021030211b2750e7b5615051a41080000340002000003000004ae01000a640310424500001283010021030211506d87a5f2fe051a410800003400020000030000044c000a6403104154000012920100210302116d5b1a76a1fc051a4108000034000204000304000436000a64031044450000128c0100210302115070aae89e15051a4108000034000202000302000458000a6403104e4c00001297010021030211ad5032b55777051a410800002f000200000300000454000a63031055530000126d002103021161576eec296b051a410800003400020000030000044a000a64031055530000127800210302115280dd7a899c051a410800003400020000030000043f000a6303104649000012a0010021030211adb0ba2565e9051a41080000340002000003000004a401000a6403104341000012670021020211442b4703f888051a410800003400020000030000044d000a630310555300001275002103021150dd334ba197051a4108000034000200000300000455000a64031046490000128e010021030211b83ae2a7ef18051a4108000034000201000301000448000a64031055530000127b0021030211b83a609679f7051a410800003400020000030000044b000a6403105553000012770021030211d45558ba60e2051a4108000034000200000300000434000a6103105345000012960100210302116013ed95b17a051a410800002f000209000309000446000a64031055530000127d002103'))

	def test(testpkt):
		h = ObjectHeader(testpkt)
		h.parse()

		print '-'*80
		print str(len(testpkt))+'('+hex(len(testpkt))+') byte'
		print 'Byte 1: '+hex(h.byte1)
		print 'Byte 2: '+hex(h.byte2)
		print 'Byte 3: '+hex(h.byte3)
		print 'Object ID: '+str2hex(h.id)
		print str2hex(h.data)

	for i in range(len(testpkts)):
		test(testpkts[i])
		sleep(1)

