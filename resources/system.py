from flask_restful import Resource
import os
import funcs
from resources.users import Users

def get_system_data():
    hostname = os.uname().nodename
    release = os.uname().release
    machine = os.uname().machine
    return hostname, release, machine

class System(Resource):
    def get(self):
        hostname, release, machine = get_system_data()
        days, hours, minutes, seconds, last_boot = funcs.get_system_uptime()
        users = Users.get_online_users()
        return {"system": {"hostname": hostname,
                        "release": release,
                        "machine": machine},
            "datetime": funcs.get_datetime(),
            "uptime": {"days": days,
                        "hour": hours,
                        "minutes": minutes,
                        "seconds": seconds,
                        "lastboot": last_boot},
                "users": users}

    @staticmethod
    def get_system_data():
        hostname = os.uname().nodename
        release = os.uname().release
        machine = os.uname().machine
        return hostname, release, machine

