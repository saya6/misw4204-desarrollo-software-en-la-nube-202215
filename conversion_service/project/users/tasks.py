from celery import shared_task

# Just for testing purposes :D
@shared_task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y