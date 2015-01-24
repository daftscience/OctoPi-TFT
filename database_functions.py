import sys
import os
import datetime
import sqlite3
import configobj
from pprint import pprint
from global_variables import *
from time import time, mktime
sys.dont_write_bytecode = True


class sqlite_database:

    def __init__(self):
        # read the settings.ini file for config information
        self.config_file = os.path.join("config", "settings.ini")
        try:
            self.config = configobj.ConfigObj(self.config_file)
        except:
            print "Error reading config/settings.ini"

        self.db_file = self.config['storage_settings']['database']
        self.column_width = self.config['storage_settings']['columns']
        self.row_height = self.config['storage_settings']['rows']

        self.db = sqlite3.connect(self.db_file)
        self.db.execute("""
                        CREATE TABLE IF NOT EXISTS tube_data (
                        id          INTEGER    PRIMARY    KEY,
                        accn        TEXT,
                        rackNum     TEXT,
                        rackDate    INT,
                        col         TEXT,
                        row         TEXT,
                        debug       TEXT,
                        timeFiled   INT)
                      """)
        self.cursor = self.db.execute('SELECT max(id) FROM tube_data')
        self.max_id = self.cursor.fetchone()[0]
        self.days_stored = 4

        self.last_stored = 'Not Available'
        self.next_row = None
        self.next_rack = None
        self.next_column = None
        self.rack_date = int(time())
        self.locate_next()

    def locate_next(self):
        self.cursor = self.db.execute('SELECT max(id) FROM tube_data')
        self.max_id = self.cursor.fetchone()[0]
        print self.cursor.rowcount
        if self.max_id is None:
            self.max_id = 0
            self.next_row = 1
            self.next_column = 1
            self.next_rack = 1
            return
        self.cursor = self.db.execute(
            'SELECT rackNum, col, row FROM tube_data where id is ' + str(self.max_id))
        last_entry = self.cursor.fetchone()
        rack = int(last_entry[0])
        column = int(last_entry[1])
        row = int(last_entry[2])
        if column == self.column_width:
            if row == self.row_height:
                column = 1
                row = 1
                rack += 1
            else:
                column = 1
                row += 1
        else:
            column += 1

        nextSpot = [str(rack), str(column), str(row)]
        self.next_row = row
        self.next_rack = rack
        self.next_column = column
        return nextSpot

    def find_accn(self, accn):
        self.cursor = self.db.cursor()
        rows = []

        # this gets a datetime of midnight a few days ago.
        earliest_date = datetime.datetime.combine(
            datetime.date.today() - datetime.timedelta(self.days_stored), datetime.time())
        earliest_date_epoch = earliest_date.strftime('%s')
        print earliest_date_epoch + "earliest epoch"

        print earliest_date
        try:
            self.cursor.execute("""
        SELECT id, accn, rackNum, col, row, timeFiled, rackDate, debug FROM tube_data WHERE accn == ? AND 
        rackDate >= ? ORDER BY id DESC""", (accn, earliest_date_epoch,))
        except sqlite3.Error as e:
            print "SQLite Error:", e.args[0]
        for thing in self.cursor:
            rows.append(thing)
        return rows

    def find_all(self):
        self.cursor = self.db.cursor()
        today = int(mktime(datetime.date.today().timetuple()))
        yesterday = int(
            mktime((datetime.date.today() - datetime.timedelta(1)).timetuple()))
        twoDaysAgo = int(
            mktime((datetime.date.today() - datetime.timedelta(2)).timetuple()))
        print "Today", today
        dates = [twoDaysAgo, yesterday, today]
        rows = []
        setRows = orderedset.OrderedSet()
        for date in dates:
            try:
                self.cursor.execute("SELECT id, accn FROM tube_data WHERE timeFiled >= datetime(" + str(
                    date) + ", 'unixepoch', 'localtime') AND timeFiled <= datetime(" + str(date + 86399) + ", 'unixepoch', 'localtime')s ORDER BY id ASC")
            except sqlite3.Error as e:
                print "SQLite Error:", e.args[0]
            else:
                for item in self.cursor:
                    print item
                    setRows.add(item[1])
        for x in setRows:
            print x
        print "----"
        while setRows:
            rows.append(setRows.pop())
        return rows

    def file_accn(self, accn):
        self.locate_next()
        time_filed = int(time())
        print time_filed
        self.db.execute("INSERT INTO tube_data (accn, rackNum, rackDate, timeFiled, col, row) VALUES(?,?,?,?,?,?)",
                        (accn, self.next_rack, self.rack_date, time_filed, self.next_column, self.next_row))
        self.db.commit()
        self.last_stored = accn
        self.locate_next()


RACK_DB = sqlite_database()


# this function is to remove an item from a tuple, not really a database
# function


# def tuple_without(original_tuple, element_to_remove):
#     new_tuple = []
#     for s in list(original_tuple):
#         if not s == element_to_remove:
#             new_tuple.append(s)
#     return tuple(new_tuple)


if __name__ == '__main__':
    def testDB(dbclass):
        test = 0
        accn = "012546308014"
        while test < 10:
            dbclass.file_accn(accn)
            print "file loop"
            test += 1
        pprint(dbclass.find_accn(accn))

    rack_dimensions = {'columns': 6, 'rows': 12}
    test = sqlite_database('racks.db', rack_dimensions)
    print "file_accn function"
    test.file_accn("98765")
    print "find accn"
    test.find_accn("98765")
    # test.find_all()
    test.db.close()
