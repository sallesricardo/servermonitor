import os
from datetime import timedelta, datetime
from flask import Flask, render_template, request, session, redirect, url_for, escape, json
import funcs

app = Flask(__name__)
app.secret_key = b'996caf70-f4df-4db7-a64d-76ca1e8e9ac6'
   
@app.after_request
def add_header(request):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    request.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    request.headers["Pragma"] = "no-cache"
    request.headers["Expires"] = "0"
    request.headers['Cache-Control'] = 'public, max-age=0'
    return request

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)
    session.modified = True


@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clock', methods=['GET'])
def clock():
    return funcs.get_datetime()

@app.route('/hello', methods=['GET'])
def hello():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('hello.html')

@app.route('/system')
def get_system_info():
    hostname, release, machine = funcs.get_system_data()
    days, hours, minutes, seconds = funcs.get_system_uptime()
    users = funcs.get_online_users()
    ret = {"system": {"hostname": hostname,
                      "release": release,
                      "machine": machine},
           "datetime": funcs.get_datetime(),
           "uptime": {"days": days,
                      "hour": hours,
                      "minutes": minutes,
                      "seconds": seconds},
            "users": users}
    return app.response_class(
        response=json.dumps(ret),
        mimetype='application/json'
    )

if __name__ == '__main__':
    debug = os.path.exists('DEBUG')
    app.run(debug=debug, host='0.0.0.0', port=(5000 if debug else 80))
