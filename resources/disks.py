from flask_restful import Resource
import psutil

class Disks(Resource):
    def get(self):
        return {"disks": self.get_disks_stats()}

    @staticmethod
    def get_disks_stats():
        disks = {}
        partitions = psutil.disk_partitions()
        for partition in partitions:
            if '/snap' not in partition.mountpoint:
                part = psutil.disk_usage(partition.mountpoint)
                disks[partition.mountpoint] = {'total': part.total, 
                                            'free': part.free, 
                                            'percent': part.percent}
        return disks
