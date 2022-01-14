import importlib
import os
from web_app import db
from web_app.script_runner.models import CheckedPoint, CheckedPointData


def dynamic_import(module):
    return importlib.import_module(module)


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
    checked_point_in_progress = CheckedPoint.query.filter_by(id_work=work_id, status='in progress').order_by(
        CheckedPoint.id.asc()).first()
    if checked_point_in_progress:
        return run_in_progress_checked_point(checked_point_in_progress, path)

    checked_point_in_backlog = CheckedPoint.query.filter_by(id_work=work_id, status='backlog').order_by(
        CheckedPoint.id.asc()).first()
    if checked_point_in_backlog:
        return run_backlog_checked_point(checked_point_in_backlog, path)

    return stop_script()


def run_in_progress_checked_point(checked_point, path):
    checked_point_id = checked_point.id
    checked_point_name = checked_point.checked_point_name

    path_of_functions_for_checked_point = path + '.functions'
    functions_for_checked_point = dynamic_import(path_of_functions_for_checked_point)

    current_function = getattr(functions_for_checked_point, checked_point_name)
    next_method = db.session.query(CheckedPointData.next_method).filter(
        CheckedPointData.id_checked_point == checked_point_id).order_by(CheckedPointData.id.desc()).first()[0]
    print(next_method)
    checked_point_data = CheckedPointData(current_method=next_method, id_checked_point=checked_point_id)
    db.session.add(checked_point_data)
    db.session.commit()
    point_in_progress = CheckedPoint.query.filter_by(id=checked_point_id).first()
    point_in_progress.status = 'in progress'
    db.session.commit()
    return getattr(current_function(checked_point_id, path), next_method)()


def run_backlog_checked_point(checked_point, path):
    checked_point_id = checked_point.id
    checked_point_name = checked_point.checked_point_name

    path_of_functions_for_checked_point = path + '.functions'
    functions_for_checked_point = dynamic_import(path_of_functions_for_checked_point)

    start_function = getattr(functions_for_checked_point, checked_point_name)
    current_method = start_function(checked_point_id, path).start_method
    checked_point_data = CheckedPointData(current_method=current_method, id_checked_point=checked_point_id)
    db.session.add(checked_point_data)
    db.session.commit()

    point_in_progress = CheckedPoint.query.filter_by(id=checked_point_id).first()
    point_in_progress.status = 'in progress'
    db.session.commit()
    return getattr(start_function(checked_point_id, path), current_method)()


def stop_script():
    print('СКРИПТ ВЫПОЛНЕН!!!!!!!!!!!!!')


if __name__ == '__main__':
    path = 'web_app.scripts.breathalyzer.dingo_49499_12'
    # pars_tree(path, work_id=14)
    run_checked_point(1, 14, path)
