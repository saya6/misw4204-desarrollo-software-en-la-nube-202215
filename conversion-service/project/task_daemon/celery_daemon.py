from project.conversion_engine.engine import ConversionEngine
from project.mail_dispatcher.mailer import MailDispatcher
from project.conversion_tasks.model import ConversionTask

from project import celery

@celery.task
def excecuteTask(id_task):
    task = ConversionTask.get_tasks_by_id(id_task)
    task.update_status_to_processing()

    cetask = ConversionEngine(
        source_file_format = task.get_file_format(),
        source_file_path = task.get_file_source_path(),
        taget_file_format = task.get_new_format(),
        target_file_path = task.get_file_converted_path()
    )

    cetask.build()
    cetask.convert()
    task.update_status_to_processed()
    email = MailDispatcher(
        receiver= task.user.email,
        title= "Tu solicitud de conversion ha sido procesada",
        body= """Hola!
         Tu solicitud de conversion del archivo archivo a formato '{}'
         ha finalizado con exito!""".format(task.get_new_format())
    )    
    email.send_mail()
    return ""