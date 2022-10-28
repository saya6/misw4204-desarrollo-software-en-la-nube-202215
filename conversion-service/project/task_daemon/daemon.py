import time

from project.mail_dispatcher.mailer import MailDispatcher
from project.conversion_tasks.model import ConversionTask
from project.conversion_engine.engine import ConversionEngine
from project import ext_celery

def retry(func):
    def wrapper_retry(*args, **kwargs):
        for wait_time in range(5):
            try:
                func(*args, **kwargs)
                break
            except Exception as e:
                print("fallo #{}registrado: {}".format(wait_time, e))
                time.sleep(0.2)
    return wrapper_retry

@retry
def dispatch_task(task_id, source_file_format, source_file_path, taget_file_format, target_file_path):
    cetask = ConversionEngine(
        source_file_format = source_file_format,
        source_file_path = source_file_path,
        taget_file_format = taget_file_format,
        target_file_path = target_file_path
    )

    cetask.build()
    cetask.convert()
    current_task = ConversionTask.get_tasks_by_id(task_id)
    current_task.update_status_to_processed()
    email = MailDispatcher(
        receiver= current_task.user.email,
        title= "Tu solicitud de conversion ha sido procesada",
        body= """Hola!
         Tu solicitud de conversion del archivo archivo a formato '{}'
         ha finalizado con exito!""".format(taget_file_format)
    )    
    email.send_mail()
    print("Tarea id={} completada con exito".format(task_id))

def run_daemon(app):
    while True:
        print("Buscando por nuevas tareas sin procesar...")
        with app.app_context():
            tasks = ConversionTask.get_unprocessed_tasks()
            if tasks.count() > 0 :
                print("Procesando ({}) tareas...".format(tasks.count()))
                for task in tasks:
                    dispatch_task(
                        task.id,
                        task.get_file_format(),
                        task.get_file_source_path(),
                        task.get_new_format(),
                        task.get_file_converted_path()
                    )
                    task.update_status_to_processing()
        time.sleep(1)


