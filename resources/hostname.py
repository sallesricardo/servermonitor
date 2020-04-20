from flask_restful import Resource
import os
import funcs

class hostname(Resource):
    def get(self):
        return {"hostname": os.uname().nodename,
           "timedate": funcs.get_datetime()}
