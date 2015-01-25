
from tinydb import TinyDB, where
from time import time
from pprint import pprint

class database():
	def __init__(self):
		self.db = TinyDB('db.json')
		self.last_filed = None

	def file_accn(self, accn):
		insert = {
			'accn': accn,
			'rack': '1',
			'column': '4',
			'row': '1',
			'time': time()
		}
		# pprint(insert)
		self.last_filed = self.db.insert(insert)

	def find_accn(self, accn):
		print "looking for: "+ str(accn)

		result = self.db.search(where('accn') == accn)
		for item in result:
			pprint(item['time'])
	def list_all(self):
		for result in self.db.all():
			pprint(result['time'])



if __name__ == '__main__':
	rack_db = database()

	# for x in xrange(1000):
		# print x
		# rack_db.file_accn(x)

	rack_db.find_accn(10)
	rack_db.list_all()
