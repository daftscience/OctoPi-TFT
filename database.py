from tinydb import TinyDB, where
from time import time, mktime, strftime, localtime
import datetime
from pprint import pprint

class tiny_db():
	def __init__(self):
		print "Init TinyDB"
		self.db = TinyDB('db.json')
		self.row_height = 12
		self.column_width = 6
		self.get_last_filed()
		self.rack_day = None
		self.next_location()

	def file_accn(self, accn):
		insert = {
			'accn': accn,
			'rack': self.next_rack,
			'rackDay': self.rack_day,
			'column': self.next_column,
			'row': self.next_row,
			'time': time()
		}
		# this does a few thigns:
		# 	First it inserts he item, and returns an eid
		# 	that eid is used to then get what it just inserted. 
		# 	then that dict is put into last filed
		self.last_filed = self.db.get(eid = self.db.insert(insert))
		self.next_location()

	def get_last_filed(self):
		# db.all returns a list of every tube, 
		# the [-1] will print the last item in the list,
		# which should be the last tube filed
		try:
			self.last_filed = self.db.all()[-1]
			pprint(self.last_filed)
		except:
			self.last_filed = None
			print "Last Filed is None"


	def new_day(self):
		print('creating new rack')
		today = strftime('%a', localtime(time()))
		self.next_column = 1
		self.next_rack = 1
		self.next_row = 1
		self.rack_day = today

	def next_location(self):
		today = strftime('%a', localtime(time()))
		print today
		if self.last_filed == None:
			self.new_day()
			return
		# pprint (self.last_filed)
		if self.last_filed['rackDay'] != today:
			print "creating new day"
			self.new_day()
		elif self.last_filed['column'] == self.column_width:
			if self.last_filed['row'] == self.row_height:
					self.next_column = 1
					self.next_row = 1
					self.next_rack = self.last_filed['rack'] + 1
			else:
					self.next_column = 1
					self.next_row = self.last_filed['row'] + 1
					self.next_rack = self.last_filed['rack']
		else:
			self.next_column = self.last_filed['column'] + 1
			self.next_rack = self.last_filed['rack']
			self.next_row = self.last_filed['row']
		self.rack_day = today

			# print "something is there!"
		# self.print_properties()

	def print_properties(self):
		print self.last_filed
		print self.next_column
		print self.next_row
		print self.next_rack
		print self.rack_day

	def find_accn(self, accn):
		print "looking for: "+ str(accn)
		# testTime = 1422225306.907
		twoDaysAgo = int(mktime((datetime.date.today() - datetime.timedelta(2)).timetuple()))

		# So this will check for accn and compare time
		# Returning only values that after two days ago
		result = self.db.search((where('accn') == accn) & (where('time') > twoDaysAgo))
		for item in result:  
			pprint(item)

	def list_all(self):
		for item in self.db.all():
			print "found: rack  "+str(item['rack']) + " "+str(item['column'])+" " +str(item['row'])

RACK_DB = tiny_db()


if __name__ == '__main__':

	# for x in xrange(100):
		# print x
		# RACK_DB.file_accn(x)

	# rack_db.find_accn(8)
	# rack_db.list_all()
	print RACK_DB.next_row
	print RACK_DB.next_column
	print RACK_DB.next_rack

	# rack_db.next_location()