from mmap import *
from struct import unpack, calcsize


class GameState:
    def __init__(self, time=None, paused=False):
        self.time = time
        self.paused = paused


class PluginInfo:
    def __init__(self, revision=0, major=0, minor=0):
        self.revision = revision
        self.major = major
        self.minor = minor


class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class GearInfo:
    def __init__(self, gear=0, gears=0, gear_ranges=0, gear_range_active=0):
        self.gear_range_active = gear_range_active
        self.gear_ranges = gear_ranges
        self.gears = gears
        self.gear = gear


class EngineInfo:
    def __init__(self, engine_rpm=0, engine_rpm_max=0):
        self.engine_rpm = engine_rpm
        self.engine_rpm_max = engine_rpm_max


class TruckInfo:
    def __init__(self, engine_enabled=False, trailer_attached=False, speed=0.0, acceleration=Vector3(0, 0, 0),
                 position=Vector3(0, 0, 0), rotation=Vector3(0, 0, 0), gear_info=GearInfo(), engine_info=EngineInfo()):
        self.engine_info = engine_info
        self.gear_info = gear_info
        self.acceleration = acceleration
        self.speed = speed
        self.position = position
        self.rotation = rotation
        self.trailer_attached = trailer_attached
        self.engine_enabled = engine_enabled


class ETSData:
    def __init__(self):
        self.truck = TruckInfo()
        self.game = GameState()
        self.plugin = PluginInfo()

    def load_from_file(self, dump_file):
        """
        Load data from file
        :param dump_file:
        :type dump_file: file
        """
        data = dump_file.read()
        self.load_from_data(data)

    def load_from_mmap(self, mmap_file):
        """
        Load data from MMAP file
        :param mmap_file: MMAP file
        :type mmap_file: mmap
        """
        data = mmap_file.read(mmap_file.size())
        self.load_from_data(data)

    def load_from_data(self, data):
        self.load_game_info(data)
        self.load_plugin_info(data)
        self.load_truck_info(data)

    def load_game_info(self, data):
        params = unpack("II", data[0:8])
        self.game = GameState(*params)

    def load_plugin_info(self, data):
        params = unpack("III", data[8:20])
        self.plugin = PluginInfo(*params)

    def load_truck_info(self, data):
        format_list = ["??xxf", "fff", "fff", "fff", "iiii", "ff"]
        offset = 20
        param_list = []
        for fmt in format_list:
            param_list.append(unpack(fmt, data[offset:offset + calcsize(fmt)]))
            print(offset, offset + calcsize(fmt))
            offset += calcsize(fmt)

        engine_enabled = param_list[0][0]
        trailer_attached = param_list[0][1]
        speed = param_list[0][2]
        self.truck = TruckInfo(engine_enabled, trailer_attached, speed, Vector3(*param_list[1]),
                               Vector3(*param_list[2]),
                               Vector3(*param_list[3]), GearInfo(*param_list[4]), EngineInfo(*param_list[5]))
