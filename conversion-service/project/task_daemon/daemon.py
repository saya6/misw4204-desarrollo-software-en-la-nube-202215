import time

from project.file_store.file_store import FileStorage
from project.mail_dispatcher.mailer import MailDispatcher
from project.conversion_tasks.model import ConversionTask
from project.conversion_engine.engine import ConversionEngine
from google.cloud import pubsub_v1

def retry(func):
    def wrapper_retry(*args, **kwargs):
        for wait_time in range(5):
            try:
                func(*args, **kwargs)
                break
            except Exception as e:
                print("fallo #{} registrado: {}".format(wait_time, e))
                time.sleep(0.2)
    return wrapper_retry

@retry
def dispatch_task(task_id, source_file_format, source_file_path, taget_file_format, target_file_path):
    file_store = FileStorage("miso_bfac_bucket")
    source_binary_file = file_store.get_file(source_file_path)
    cetask = ConversionEngine(
        source_file_format = source_file_format,
        source_file_path = source_file_path,
        taget_file_format = taget_file_format,
        target_file_path = target_file_path
    )
    cetask.build()
    cetask.set_source_file_bytes(source_binary_file)
    cetask.convert()
    current_task = ConversionTask.get_tasks_by_id(task_id)
    file_store.save_file_from_file(target_file_path, cetask.get_target_file_bytes())
    current_task.update_status_to_processed()
    email = MailDispatcher(
        receiver= current_task.user.email,
        title= "Tu solicitud de conversion ha sido procesada",
        body= """Hola!
         Tu solicitud de conversion del archivo archivo a formato '{}'
         ha finalizado con exito!""".format(taget_file_format)
    )    
    email.send_mail()
    print("Tarea id ({}) completada con exito".format(task_id))


def callback_with_app(app):
    def callback(message):
        # process the message
        task_id = int(message.data)
        message.ack()
        print("Procesando tarea con id ({})".format(task_id))

        # get the task fron the database
        with app.app_context():
            task = ConversionTask.get_tasks_by_id(task_id)
            if task != None:
                task.update_status_to_processing()
                dispatch_task(
                    task.id,
                    task.get_file_format(),
                    task.get_file_source_path(),
                    task.get_new_format(),
                    task.get_file_converted_path()
                )

    return callback

def run_daemon(app):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = "projects/bfac-366702/subscriptions/conversion_tasks-sub"
    flow_control = pubsub_v1.types.FlowControl(max_messages=1)
    streaming_pull_future =subscriber.subscribe(subscription_path, callback = callback_with_app(app), flow_control= flow_control)
    with subscriber:
        try:
            print("Buscando por nuevas tareas sin procesar...")
            streaming_pull_future.result()
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()



