from flask_restful import Resource
import psutil
import subprocess

class Process(Resource):
    def get(self):
        return {"processes": self.get_process_list()}

    @staticmethod
    def get_process_list():
        processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            processes.append(proc.info)

        return processes

    @staticmethod
    def get_process(pid):
        process = {}
        return process