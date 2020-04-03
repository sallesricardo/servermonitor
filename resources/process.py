from flask_restful import Resource
import psutil
import subprocess

class Process(Resource):
    def get(self, name=None, pid=None):
        if name:
            return {"process": self.get_process_list(name)}
        if pid:
            return {"PID": self.get_process(pid)}
        return {"processes": self.get_process_list()}

    @staticmethod
    def get_process_list(name=None, pid=None):
        processes = []
        for proc in psutil.process_iter():
            pInfoDict = proc.as_dict(attrs=['pid', 
                                            'memory_percent', 
                                            'cpu_percent', 
                                            'name'])
            if not name or name in pInfoDict['name']:
                processes.append(pInfoDict)                
        return processes

    @staticmethod
    def get_process(pid):
        return psutil.Process(pid).as_dict(attrs=[
                                            'cmdline', 
                                            'connections', 
                                            'cpu_num', 
                                            'cpu_percent', 
                                            'create_time', 
                                            'cwd', 
                                            'exe', 
                                            'gids', 
                                            'ionice', 
                                            'memory_percent', 
                                            'name', 
                                            'nice', 
                                            'num_fds', 
                                            'num_threads', 
                                            'open_files', 
                                            'pid', 
                                            'ppid', 
                                            'status', 
                                            'terminal', 
                                            'threads', 
                                            'uids', 
                                            'username'])

