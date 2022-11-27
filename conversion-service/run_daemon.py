from multiprocessing import Process
from app import app as current_flask_app
from project.task_daemon.daemon import run_daemon

from flask import Flask

app = Flask(__name__)

p1 = Process(target=run_daemon, args=(current_flask_app,))
p1.start()

@app.route('/')
def main():
    return {"service": "worker", "status": "ok"}, 200

if __name__ == '__main__':
    app.run(debug=True)
    p1.close()