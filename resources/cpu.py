from flask_restful import Resource
import psutil

class CPU(Resource):
    def get(self):
        return {"cpu": self.get_cpu_specs(),
           "memory": self.get_mem_stat()}

    @staticmethod
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

    @staticmethod
    def get_mem_stat():
        memory = {}
        mem = psutil.virtual_memory()
        memory['total'] = mem.total
        memory['usage'] = mem.percent
        mem = psutil.swap_memory()
        memory['sw_total'] = mem.total
        memory['sw_usage'] = mem.percent
        return memory
