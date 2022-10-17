import time
from project.conversion_tasks.model import ConversionTask
from project.conversion_engine.engine import ConversionEngine
from project import ext_celery

# @ext_celery.celery.task(id='project.task_daemon.daemon.dispatch_task')
def dispatch_task(task_id, source_file_format, source_file_path, taget_file_format, target_file_path):
    cetask = ConversionEngine(
        source_file_format = source_file_format,
        source_file_path = source_file_path,
        taget_file_format = taget_file_format,
        target_file_path = target_file_path
    )

    cetask.build()
    cetask.convert()
    ConversionTask.get_tasks_by_id(task_id).update_status_to_processed()    
    # TODO: send mail to user

def run_daemon(app):
    while True:
        print("Buscando por nuevas tareas sin procesar...")
        with app.app_context():
            tasks = ConversionTask.get_unprocessed_tasks()
            for task in tasks:
                task.update_status_to_processing()
                dispatch_task(
                    task.id,
                    task.get_file_format(),
                    task.get_file_source_path(),
                    task.get_new_format(),
                    task.get_file_converted_path()
                )
        time.sleep(1)


