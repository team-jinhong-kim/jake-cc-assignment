from flask import redirect, render_template, request
from . import main

@main.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@main.route('/shutdown')
def server_shutdown():
    shutdown = request.environ.get('werkzeug.server.shutdown')
    shutdown()
    return 'Shutting down...'
