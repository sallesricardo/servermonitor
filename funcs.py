import os
import subprocess
import psutil
import socket
from datetime import datetime, timedelta

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
    last_boot = datetime.fromtimestamp(psutil.boot_time())
    return days, hours, minutes, seconds, last_boot.strftime("%d/%m/%Y %H:%M:%S")

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

def get_cpu_specs():
    cpu = {}
    cpu['model'] = None
    cpu['clock'] = psutil.cpu_freq().current
    cpu['cores'] = psutil.cpu_count()
    cpu['usage'] = psutil.cpu_percent()
    cpu['avg_load'] = psutil.getloadavg()
    cpu_times = psutil.cpu_times_percent()
    cpu['iowait'] = cpu_times.iowait
    with open('/proc/cpuinfo', 'r') as cpuinfo:
        for line in cpuinfo:
            if ('model name' in line) or ('cpu model' in line):
                print("CPU mode: {}".format(line))
                cpu['model'] = line.split(':')[1].strip()
    return cpu

def get_mem_stat():
    memory = {}
    mem = psutil.virtual_memory()
    memory['total'] = mem.total
    memory['usage'] = mem.percent
    mem = psutil.swap_memory()
    memory['sw_total'] = mem.total
    memory['sw_usage'] = mem.percent
    return memory

def get_disks_stats():
    disks = {}
    partitions = psutil.disk_partitions()
    for partition in partitions:
        part = psutil.disk_usage(partition.mountpoint)
        disks[partition.mountpoint] = {'total': part.total, 'free': part.free, 'percent': part.percent}
    return disks

def get_network_stats():
    network = {}
    interfaces = psutil.net_if_addrs()
    interfaces_stats = psutil.net_io_counters(pernic=True)
    for interface in interfaces:
        for conf in interfaces[interface]:
            if conf.family == socket.AF_INET:
                network[interface] = {'ip': conf.address, 
                                      'sent': interfaces_stats[interface].bytes_sent,
                                      'recv': interfaces_stats[interface].bytes_recv}
    
    return network

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

def get_active_users():
    return psutil.users()

def get_process_list():
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        processes.append(proc.info)

    return processes
