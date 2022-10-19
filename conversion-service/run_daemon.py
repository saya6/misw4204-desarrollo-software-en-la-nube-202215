from multiprocessing import Process
from app import app
#from project import ext_celery
from project.task_daemon.daemon import run_daemon

#celery = ext_celery.celery

p1 = Process(target=run_daemon, args=(app,))
p1.start()
p1.join()
