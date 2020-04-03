from flask_restful import Resource
import psutil
import subprocess

class Users(Resource):
    def get(self):
        return {"users": self.get_active_users()}

    @staticmethod
    def get_online_users():
        who = subprocess.Popen(['who', '-q'], stdout=subprocess.PIPE)
        ret_users = who.stdout.readline().decode('utf8')
        ret_nusers = who.stdout.readline().decode('utf8')
        users = {}
        for user in ret_users.split():
            if user in users:
                users[user] += 1
            else:
                users[user] = 1
        users['total'] = int(ret_nusers.split('=')[1])

        return users

    @staticmethod
    def get_active_users():
        return psutil.users()
