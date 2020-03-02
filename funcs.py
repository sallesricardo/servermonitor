import os
import subprocess
from datetime import datetime

def get_datetime():
    today = datetime.now()
    return today.strftime("%d/%m/%Y %H:%M:%S")

def get_system_data():
    hostname = os.uname().nodename
    release = os.uname().release
    machine = os.uname().machine
    return hostname, release, machine

def get_system_uptime():
    with open('/proc/uptime', 'r') as uptime:
        total_seconds = int(uptime.readline().split('.')[0])
    seconds = total_seconds % 60
    total_minutes = int(total_seconds / 60)
    minutes = total_minutes % 60
    total_hours = int(total_minutes / 60)
    hours = total_hours % 24
    days = int(total_hours / 24)
    return days, hours, minutes, seconds

def get_online_users():
    who = subprocess.Popen(['who', '-q'], stdout=subprocess.PIPE)
    ret_users = who.stdout.readline().decode('ascii')
    ret_nusers = who.stdout.readline().decode('ascii')
    users = {}
    for user in ret_users.split():
        if user in users:
            users[user] += 1
        else:
            users[user] = 1
    users['total'] = int(ret_nusers.split('=')[1])
    
    return users

