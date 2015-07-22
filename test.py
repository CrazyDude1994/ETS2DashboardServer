import time
from mmap import *
from ets_data_mapper import ETSData
import sys

def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))

data = ETSData()
map_file = mmap(-1, 16 * 1024, "Local\SimTelemetryETS2", ACCESS_READ)
while 1:
    map_file.seek(0)
    data.load_from_mmap(map_file)
    sys.stdout.write("\rSpeed: {0} Gear: {1} Trailer name: {2}".format(data.truck.speed, data.truck.gear_info.gear,
                                                                     data.trailer.trailer_id))
    progress(data.truck.fuel_info.fuel, data.truck.fuel_info.fuel_capacity, "Fuel")
    sys.stdout.flush()
    time.sleep(0.1)
