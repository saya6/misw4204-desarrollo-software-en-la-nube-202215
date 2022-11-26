from multiprocessing import Process
from ..project.app import app as flask_app_context
from ..project.task_daemon.daemon import run_daemon
from flask import Flask

application = Flask(__name__)

@application.route('/', methods=['GET'])
def index():
    return 'OK', 200

if __name__ == '__main__':
    p1 = Process(target=run_daemon, args=(flask_app_context,))
    p1.start()
    application.run(host='0.0.0.0', port=80)