from web_app import celery_app, app
from web_app.script_runner.runner import load_checked_point_in_db, run_checked_point


@celery_app.task
def start_script_in_celery(work_id, script_path_for_import):
    with app.app_context(), app.test_request_context():
        load_checked_point_in_db(script_path_for_import, work_id)
        return run_checked_point(work_id, script_path_for_import)


@celery_app.task
def run_script_in_celery(work_id, script_path_for_import):
    with app.app_context(), app.test_request_context():
        return run_checked_point(work_id, script_path_for_import)