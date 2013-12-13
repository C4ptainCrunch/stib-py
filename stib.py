import requests
from xml.etree import ElementTree
import time

class Stop(object):
	def __init__(self, id, name, present, gps):
		self.id = id
		self.name = name
		self.present = present
		self.gps = gps

	@classmethod
	def from_xml(klass, node):
		present = False
		gps = {}
		for tag in node:
			if tag.tag == 'name':
				name = tag.text.capitalize()
			elif tag.tag == 'id':
				id = tag.text
			elif tag.tag == 'present':
				present = True
			elif tag.tag == 'latitude':
				gps['latitude'] = tag.text
			elif tag.tag == 'longitude':
				gps['longitude'] = tag.text
		return Stop(id, name, present, gps)

	def __repr__(self):
		vehicule = 'X' if self.present else '-'
		return "<[{}] Stop {} ({})>".format(vehicule, self.name, self.id)


class Traject(object):
	
	def __init__(self, id, way):
		'''Init of a traject, params :
		id (int) : number of the stib line
		way (int) : 1 or 2, way of the line (see stib website)'''
		self.id = id
		self.way = way
		self.stops = []
		self.last_update = time.time()
		r = requests.get('http://m.stib.be/api/getitinerary.php?line={}&iti={}'.format(id, way))
		stops = ElementTree.fromstring(r.text)

		for stop in stops:
			self.stops.append(Stop.from_xml(stop))

	def update(self, force=True, wait=False):
		'''Update the traject infos. Set force=False to prevent querying the api if last update if newer than 20 sec
		Set force=False and wait=True to block untill the 20 sec are done.'''
		if not force:
			diff = time.time() - self.last_update
			if diff < 20:
				if wait:
					time.sleep(20 - diff)
				else:
					return None
		self.__init__(self.id, self.way)


	@property
	def terminus(self):
		'''Return the last stop'''
		return self.stops[-1]

	@property
	def start(self):
		'''Return the first stop'''
		return self.stops[0]

	def __len__(self):
		'''Number of vehicles on the traject'''
		l = 0
		for stop in self.stops:
			if stop.present:
				l += 1
		return l

	def __repr__(self):
		return "<Traject {}: direction {}, {} stops, {} vehicules>".format(self.id, self.terminus.name, len(self.stops), len(self))

if __name__ == '__main__':
	bus95 = Traject(95,1) # Bus 95, direction Heiligenborre
	print "Line 95, direction Heiligenborre"
	print repr(bus95)
	print '--------------------'
	print "The 10th stop"
	print repr(bus95.stops[10])
	print 'GSP coords'
	print repr(bus95.stops[10].gps)
	print '--------------------'
	print 'All stops :'
	for stop in bus95.stops:
		print repr(stop)

