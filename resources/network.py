from flask_restful import Resource
import psutil
import socket

class Network(Resource):
    def get(self):
        return {"network": self.get_network_stats()}

    @staticmethod
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
