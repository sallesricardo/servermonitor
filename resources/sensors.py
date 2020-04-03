from flask_restful import Resource
import psutil

class Sensors(Resource):
    def get(self):
        return {"sensors": self.get_sensors()}

    @staticmethod
    def get_sensors():
        def inc_n (n):
            n += 1
            return n
        sensors = {}
        sys_fans = {}
        temperatures = psutil.sensors_temperatures()
        fans = psutil.sensors_fans()
        battery = psutil.sensors_battery()
        for sensor in temperatures:
            sensors[sensor] = {}
            n = 0
            for sen in temperatures[sensor]:
                label = sen.label if sen.label else inc_n(n)
                sensors[sensor][label] = {'current': sen.current, 'high': sen.high}
        
        for device in fans:
            for fan in fans[device]:
                sys_fans[fan.label] = fan.current
        ret = {'temperature': sensors, 'fans': sys_fans}
        if battery:
            bat = {'percent': battery.percent}
            if battery.power_plugged:
                bat['power'] = 'AC'
            elif battery.power_plugged == None:
                bat['power'] = 'Unknow'
            else:
                bat['power'] = 'battery'
                bat['secsleft'] = battery.secsleft
            ret['battery'] = bat
        return ret