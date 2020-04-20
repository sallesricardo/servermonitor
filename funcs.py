import os
import subprocess
import psutil
import socket
from datetime import datetime, timedelta

def get_datetime():
    today = datetime.now()
    # return today.strftime("%d/%m/%Y %H:%M:%S")
    return today.isoformat()

def get_system_uptime():
    with open('/proc/uptime', 'r') as uptime:
        total_seconds = int(uptime.readline().split('.')[0])
    seconds = total_seconds % 60
    total_minutes = int(total_seconds / 60)
    minutes = total_minutes % 60
    total_hours = int(total_minutes / 60)
    hours = total_hours % 24
    days = int(total_hours / 24)
    last_boot = datetime.fromtimestamp(psutil.boot_time())
    return days, hours, minutes, seconds, last_boot.strftime("%d/%m/%Y %H:%M:%S")

