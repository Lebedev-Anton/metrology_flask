import importlib
import os
from web_app import db
from web_app.script_runner.models import CheckedPoint, CheckedPointData
from flask import redirect, url_for
from web_app.script_runner.enums import Status
from config import Config


def dynamic_import(module):
    path_module = Config.BASE_PATH + module
    return importlib.import_module(path_module)


def isLoad(id):
    return CheckedPoint.query.filter_by(id_work=id).all()


def load_checked_point_in_db(path, work_id):
    if not isLoad(work_id):
        CheckedPoint.query.filter_by(id_work=work_id).all()
        script_module = dynamic_import(path)
        script_path = os.path.dirname(script_module.__file__)
        tree_path = os.path.join(script_path, 'tree.uts')
        with open(tree_path, 'r', encoding='utf-8') as file:
            tree_lines = file.readlines()

        for line in tree_lines:
            if not ('#' in line):
                line_data = line.split()
                checked_point_name = line_data[0]
                checked_point_parameters = str(line_data[1:])
                checked_point = CheckedPoint(checked_point_name=checked_point_name,
                                             checked_point_parameters=checked_point_parameters, id_work=work_id)
                db.session.add(checked_point)
                db.session.commit()


def run_checked_point(user_id, work_id, path):
    checked_point_in_progress = CheckedPoint.query.filter_by(id_work=work_id, status=Status.in_progress.value).order_by(
        CheckedPoint.id.asc()).first()
    if checked_point_in_progress:
        return selection_checked_point(checked_point_in_progress, path, Status.in_progress.value)

    checked_point_in_backlog = CheckedPoint.query.filter_by(id_work=work_id, status=Status.backlog.value).order_by(
        CheckedPoint.id.asc()).first()
    if checked_point_in_backlog:
        return selection_checked_point(checked_point_in_backlog, path, Status.backlog.value)

    return stop_script()


def get_script_functions(path):
    path_of_script_functions = path + '.functions'
    return dynamic_import(path_of_script_functions)


def isLastMethodInProgress(checked_point_id):
    return CheckedPointData.query.filter_by(status=Status.in_progress.value, id_checked_point=checked_point_id).all()


def selection_checked_point(checked_point, path, type_selection):
    checked_point_id = checked_point.id
    checked_point_name = checked_point.checked_point_name

    script_functions = get_script_functions(path)

    current_function = getattr(script_functions, checked_point_name)
    if type_selection == Status.backlog.value:
        next_method = current_function(checked_point_id, path).start_method
    else:
        if isLastMethodInProgress(checked_point_id):
            in_progress_method = CheckedPointData.query.filter_by(
                status=Status.in_progress.value, id_checked_point=checked_point_id).order_by(
                CheckedPointData.id.desc()).first()
            next_method = in_progress_method.current_method
            db.session.delete(in_progress_method)
        else:
            next_method = db.session.query(CheckedPointData.next_method).filter(
                CheckedPointData.id_checked_point == checked_point_id).order_by(CheckedPointData.id.desc()).first()[0]

    checked_point_data = CheckedPointData(current_method=next_method,
                                          id_checked_point=checked_point_id, status=Status.in_progress.value)
    db.session.add(checked_point_data)

    point_in_progress = CheckedPoint.query.filter_by(id=checked_point_id).first()
    point_in_progress.status = Status.in_progress.value
    db.session.commit()
    return getattr(current_function(checked_point_id, path), next_method)()


def stop_script():
    return redirect(url_for('index'))
