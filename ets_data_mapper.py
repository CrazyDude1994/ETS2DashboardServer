from struct import unpack, calcsize
import json


class TruckEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        return json.JSONEncoder.default(self, obj)


class GameState:
    def __init__(self, time=None, paused=False, time_absolute=0):
        self.time_absolute = time_absolute
        self.time = time
        self.paused = paused

    def __json__(self):
        return vars(self)


class PluginInfo:
    def __init__(self, revision=0, major=0, minor=0):
        self.revision = revision
        self.major = major
        self.minor = minor

    def __json__(self):
        return vars(self)


class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __json__(self):
        return vars(self)


class GearInfo:
    def __init__(self, gear=0, gears=0, gear_ranges=0, gear_range_active=0):
        self.gear_range_active = gear_range_active
        self.gear_ranges = gear_ranges
        self.gears = gears
        self.gear = gear

    def __json__(self):
        return vars(self)


class FuelInfo:
    def __init__(self, fuel=0, fuel_capacity=0, fuel_rate=0, fuel_avg_consumption=0):
        self.fuel_capacity = fuel_capacity
        self.fuel_rate = fuel_rate
        self.fuel_avg_consumption = fuel_avg_consumption
        self.fuel = fuel

    def __json__(self):
        return vars(self)


class EngineInfo:
    def __init__(self, engine_rpm=0, engine_rpm_max=0):
        self.engine_rpm = engine_rpm
        self.engine_rpm_max = engine_rpm_max

    def __json__(self):
        return vars(self)


class InputInfo:
    def __init__(self, user_steer=0, user_throttle=0, user_brake=0, user_clutch=0, game_steer=0, game_throttle=0,
                 game_brake=0, game_clutch=0):
        self.game_throttle = game_throttle
        self.game_steer = game_steer
        self.game_brake = game_brake
        self.game_clutch = game_clutch
        self.user_steer = user_steer
        self.user_throttle = user_throttle
        self.user_brake = user_brake
        self.user_clutch = user_clutch

    def __json__(self):
        return vars(self)


class TrailerInfo:
    def __init__(self, trailer_weight=0, trailer_offset=0, trailer_length=0, trailer_id="", trailer_name=""):
        self.trailer_id = trailer_id.strip("\0")
        self.trailer_name = trailer_name.strip("\0")
        self.trailer_length = trailer_length
        self.trailer_offset = trailer_offset
        self.trailer_weight = trailer_weight

    def __json__(self):
        return vars(self)


class TruckInfo:
    def __init__(self, engine_enabled=False, trailer_attached=False, speed=0.0, acceleration=Vector3(0, 0, 0),
                 position=Vector3(0, 0, 0), rotation=Vector3(0, 0, 0), gear_info=GearInfo(), engine_info=EngineInfo(),
                 fuel_info=FuelInfo(), truck_weight=0, model_offset=0, model_length=0):
        self.truck_weight = truck_weight
        self.model_offset = model_offset
        self.model_length = model_length
        self.fuel_info = fuel_info
        self.engine_info = engine_info
        self.gear_info = gear_info
        self.acceleration = acceleration
        self.speed = speed
        self.position = position
        self.rotation = rotation
        self.trailer_attached = trailer_attached
        self.engine_enabled = engine_enabled

    def __json__(self):
        return vars(self)


class ETSData:
    def __init__(self):
        self.truck = TruckInfo()
        self.game = GameState()
        self.plugin = PluginInfo()
        self.trailer = TrailerInfo()
        self.input = InputInfo()

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
        format_list = ["??xxf", "3f", "3f", "3f", "4i", "2f", "4f", "8f", "2f4i", "2i", "f64s64s"]
        offset = 20  # truck info byte position offset
        param_list = []
        for fmt in format_list:
            param_list.append(unpack(fmt, data[offset:offset + calcsize(fmt)]))
            offset += calcsize(fmt)

        engine_enabled, trailer_attached, speed = param_list[0][:3]
        truck_weight, model_offset, model_length = param_list[8][0], param_list[8][2], param_list[8][3]
        trailer_weight, trailer_offset, trailer_length = param_list[8][1], param_list[8][4], param_list[8][5]
        time_absolute, gears_reverse = param_list[9]
        trailer_mass, trailer_id, trailer_name = param_list[10]
        self.input = InputInfo(*param_list[7])
        self.trailer = TrailerInfo(trailer_weight, trailer_offset, trailer_length, trailer_id, trailer_name)
        self.truck = TruckInfo(engine_enabled, trailer_attached, speed, Vector3(*param_list[1]),
                               Vector3(*param_list[2]),
                               Vector3(*param_list[3]), GearInfo(*param_list[4]), EngineInfo(*param_list[5]),
                               FuelInfo(*param_list[6]), truck_weight, model_offset, model_length)

    def __json__(self):
        return vars(self)
