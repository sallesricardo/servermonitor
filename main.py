import os
from datetime import timedelta, datetime
import ujson as json
from flask import Flask, redirect, url_for, render_template, session
from flask_restful import Api
from flask_cors import CORS

from conf import Conf

from resources.hostname import hostname
from resources.system import System
from resources.cpu import CPU
from resources.disks import Disks
from resources.network import Network
from resources.sensors import Sensors
from resources.users import Users
from resources.process import Process

conf = Conf()

app = Flask(__name__)
CORS(app)
app.secret_key = bytes(conf.secret_key, 'utf-8')
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)


@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html', conf=conf)

api.add_resource(hostname, '/hostname')
api.add_resource(System, '/system')
api.add_resource(CPU, '/cpu')
api.add_resource(Disks, '/disks')
api.add_resource(Network, '/network')
api.add_resource(Sensors, '/sensors')
api.add_resource(Users, '/users')
api.add_resource(Process, '/process', '/process/<string:name>', '/process/<int:pid>')

@app.route('/hello', methods=['GET'])
def hello():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('hello.html')


if __name__ == '__main__':
    debug = os.path.exists('DEBUG')
    app.run(debug=debug, host='0.0.0.0', port=(5000 if debug else 80))
