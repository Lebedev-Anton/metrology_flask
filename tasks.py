from celery import Celery
from web_app.script_runner.runner import load_checked_point_in_db
celery_app = Celery('tasks', broker='redis://localhost:6379/0')


@celery_app.task
def load_checked_point_in_celery(script_path_for_import, work_id):
    load_checked_point_in_db(script_path_for_import, work_id)

