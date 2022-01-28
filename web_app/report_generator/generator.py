import jinja2
import pdfkit
import pandas as pd
from web_app import db
from web_app.scripts.models import UserData, Protocols
import os
import importlib
from config import Config


def dynamic_import(module):
    path_module = Config.BASE_PATH + module
    return importlib.import_module(path_module)


def load_protocol_data_from_db(work_id):
    user_records = UserData.query.filter_by(id_work=work_id).all()
    protocol_data = []
    visual_parameter = []
    testing_parameter = []
    visual_result = []
    testing_result = []

    nominal_value = []
    meas_value = []
    type_pogr = []
    max_error = []
    error = []
    meas_result = []
    for user_record in user_records:
        protocol_data.append({'base_name': user_record.base_name, 'data': user_record.path})
        user_data = eval(user_record.path)
        if user_record.base_name == 'Visual':
            visual_parameter.append(user_data['content'][0])
            visual_result.append(user_data['content'][1])
        elif user_record.base_name == 'Testing':
            testing_parameter.append(user_data['content'][0])
            testing_result.append(user_data['content'][1])
        elif user_record.base_name == 'Meas':
            nominal_value.append(user_data['content'][0])
            meas_value.append(user_data['content'][1])
            type_pogr.append(user_data['content'][2])
            error.append(user_data['content'][3])
            max_error.append(user_data['content'][4])
            meas_result.append(user_data['content'][5])

    visual = pd.DataFrame({'Проверяемый параметр': visual_parameter, 'Соответсвие': visual_result})
    testing = pd.DataFrame({'Проверяемый параметр': testing_parameter, 'Соответсвие': testing_result})
    meas = pd.DataFrame({'Номинальное значение': nominal_value, 'Измеренное значение': meas_value,
                         'Тип погрешности': type_pogr, 'Погрешность': error, 'Допуск (не более)': max_error,
                         'Соответсвие': meas_result})
    pd.set_option('styler.sparse.index', True)

    return visual, testing, meas


def generate_html(visual, testing, meas, path):
    script_module = dynamic_import(path)
    script_path = os.path.dirname(script_module.__file__)
    template_path = os.path.abspath(os.path.join(script_path, '..'))
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=template_path))
    template = env.get_template('template.html')
    html = template.render(visual=visual.style.to_html(), testing=testing.style.to_html(), meas=meas.style.to_html())
    return html


def save_html_to_pdf(work_id, html, path):
    path_protokol = os.path.join(path, f'{work_id}.pdf')
    pdfkit.from_string(html, path_protokol)
    protocol = Protocols(id_work=work_id, protocol_name=f'{work_id}.pdf', path=path_protokol)
    db.session.add(protocol)
    db.session.commit()


if __name__ == '__main__':
    visual, testing, meas = load_protocol_data_from_db(2)
    html = generate_html(visual, testing, meas, 'breathalyzer.dingo_49499_12')
    save_html_to_pdf(2, html, '/home/anton/projects/protokol/')
