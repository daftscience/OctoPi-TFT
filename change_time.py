import sys
import datetime
from pprint import pprint
import os
# from subprocess import call, Popen
import subprocess


class change_time():

    def __init__(self):
        pass

    def set(self, time_tuple):
        if sys.platform == 'linux2':
            # self.system = "linux"
            self._linux_set_time(time_tuple)
        elif sys.platform == 'win32':
            # self.system = "windows"
            self._win_set_time(time_tuple)
        else:
            print sys.platform

    def _win_set_time(self, time_tuple):
        # import pywin32
        # http://timgolden.me.uk/pywin32-docs/win32api__SetSystemTime_meth.html
        # pywin32.SetSystemTime(year, month , dayOfWeek , day , hour , minute , second , millseconds )
        # dayOfWeek = datetime.datetime(time_tuple).isocalendar()[2]
        # pywin32.SetSystemTime(time_tuple[:2] + (dayOfWeek,) + time_tuple[2:])
        print(time_tuple)

    def _linux_set_time(self, time_tuple):
        import ctypes
        import ctypes.util
        import time

        # /usr/include/linux/time.h:
        #
        # define CLOCK_REALTIME
        CLOCK_REALTIME = 0

        class timespec(ctypes.Structure):
            _fields_ = [("tv_sec", ctypes.c_long),
                        ("tv_nsec", ctypes.c_long)]

        librt = ctypes.CDLL(ctypes.util.find_library("rt"))

        ts = timespec()
        ts.tv_sec = int(
            time.mktime(
                datetime.datetime(
                    *
                    time_tuple[
                        :6]).timetuple()))
        ts.tv_nsec = time_tuple[6] * 1000  # Millisecond to nanosecond

        # http://linux.die.net/man/3/clock_settime
        librt.clock_settime(CLOCK_REALTIME, ctypes.byref(ts))

    def change(self, unit, value):
        delta = {unit: value}
        # pprint(delta)
        current_time = datetime.datetime.now()
        # pprint(current_time)
        new_time = current_time + datetime.timedelta(**delta)
        new_time = new_time.timetuple()
        self.set(new_time)
        # '/bin/sh', '-c',
        # Popen('/bin/sh', '-c', "hwclock -r")
        # Popen('/bin/sh', '-c', "hwclock -r")
        # Popen('/bin/sh', '-c', "hwclock -r")
        # os.system("hwclock -r")
        # os.system("hwclock -w")
        # os.system("hwclock -r")
        # os.popen("hwclock -w", 'r', 1)
        # subprocess.call(["hwclock", "-w"], shell=True)
        # call(["hwclock", "-r"])
        # call(["hwclock", "-w"])
        # call(["hwclock", "-r"])
        # pprint(datetime.datetime.now().timetuple())


if __name__ == "__main__":

    from time import time, localtime
    from pprint import pprint
    # local_time = datetime.datetime.now()
    # time_tuple = datetime.date.timetuple(local_time)
    # time_tuple = localtime()

    # datetime.datetime(2010, 12, 26, 2, 25)
    # pprint(d)

    # pprint(time_tuple)
    test = change_time()
    test.change("hours", -1)
    test.change('minutes', -1)


# if sys.platform == 'linux2':
#     _linux_set_time(time_tuple)

# elif sys.platform == 'win32':
#     _win_set_time(time_tuple)
