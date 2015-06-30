from ets_data_mapper import ETSData


dump_file = open("C:\\unpaused.txt", "r")
data = ETSData()
data.load_from_file(dump_file)
print data.truck.gear_info.gear