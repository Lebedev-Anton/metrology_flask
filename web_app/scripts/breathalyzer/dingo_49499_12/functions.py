from web_app.scripts import BaseFunction


class Visual(BaseFunction):
    start_method = 'preparation_device'

    def preparation_device(self):
        choice_field_1 = {'type': 'choise', 'name': 'choise_1', 'value': ['Соотв.', 'Не соотв.']}
        choice_field_2 = {'type': 'choise', 'name': 'choise_2', 'value': ['Соотв.', 'Не соотв.']}
        headings = ['Проверяемый пункт', 'Соответсвие']
        num_rows = 2
        rows_data = {0: ['Царапины и повреждения на корпусе отсутвуют', choice_field_1],
                     1: ['Внешний вид соответвует требованиям ОТ и МП', choice_field_2]}
        table_config = {'headings': headings, 'num_rows': num_rows, 'rows_data': rows_data}
        self.next_method('check_user_answer')
        return self.show_table(table_config)

    def check_user_answer(self):
        user_answer = eval(self.return_user_answer('preparation_device'))
        result_visual_1 = user_answer.get('choise_1')
        result_visual_2 = user_answer.get('choise_2')
        if result_visual_1 == 'Соотв.' and result_visual_2 == 'Соотв.':
            return self.last_method()
        else:
            self.next_method('repeat')
            text_message = 'Визуальный осмотр не пройден. Повторить?'
            response_options = 'Да;Нет'
            return self.show_question(text_message, response_options)

    def repeat(self):
        user_answer = eval(self.return_user_answer('check_user_answer'))
        result_visual = user_answer.get('choice')
        if result_visual == 'Да':
            self.next_method('preparation_device')
        else:
            self.next_method('last_method')
        return self.redirect_in_next_method()


class Testing(BaseFunction):
    start_method = 'preparation_device'

    def preparation_device(self):
        choice_field_1 = {'type': 'choise', 'name': 'choise_1', 'value': ['Соотв.', 'Не соотв.']}
        choice_field_2 = {'type': 'choise', 'name': 'choise_2', 'value': ['Соотв.', 'Не соотв.']}
        headings = ['Проверяемый пункт', 'Соответсвие']
        num_rows = 2
        rows_data = {0: ['Прибор включается, на экране проявляется информация о приборе', choice_field_1],
                     1: ['Автоматически происходит забор пробы воздуха', choice_field_2]}
        table_config = {'headings': headings, 'num_rows': num_rows, 'rows_data': rows_data}
        self.next_method('check_user_answer')
        return self.show_table(table_config)

    def check_user_answer(self):
        user_answer = eval(self.return_user_answer('preparation_device'))
        result_visual_1 = user_answer.get('choise_1')
        result_visual_2 = user_answer.get('choise_2')
        if result_visual_1 == 'Соотв.' and result_visual_2 == 'Соотв.':
            return self.last_method()
        else:
            self.next_method('repeat')
            text_message = 'Опробование не пройдено. Повторить?'
            response_options = 'Да;Нет'
            return self.show_question(text_message, response_options)

    def repeat(self):
        user_answer = eval(self.return_user_answer('check_user_answer'))
        result_visual = user_answer.get('choice')
        if result_visual == 'Да':
            self.next_method('preparation_device')
        else:
            self.next_method('last_method')
        return self.redirect_in_next_method()


class Meas(BaseFunction):
    start_method = 'connect_device'

    def connect_device(self):
        parameters = eval(self.get_checked_point_parameters())
        message = f'Подайте на прибор значение {parameters[0]}'
        self.next_method('meas')
        return self.show_message(message)

    def meas(self):
        parameters = eval(self.get_checked_point_parameters())
        message = f'Проведите три измерения на поверяемой точке {parameters[0]}'
        input_field_1 = {'type': 'input', 'name': 'input_1'}
        input_field_2 = {'type': 'input', 'name': 'input_2'}
        input_field_3 = {'type': 'input', 'name': 'input_3'}

        headings = ['Номинальное значение', 'Измеренное значение', 'Тип погрешности', 'Погрешность']
        num_rows = 3
        rows_data = {0: [parameters[0], input_field_1, parameters[1], parameters[2]],
                     1: [parameters[0], input_field_2, parameters[1], parameters[2]],
                     2: [parameters[0], input_field_3, parameters[1], parameters[2]],
                     }
        table_config = {'headings': headings, 'num_rows': num_rows, 'rows_data': rows_data}
        self.next_method('check_user_answer')
        return self.show_table(table_config, message)

    def check_user_answer(self):
        user_answer = eval(self.return_user_answer('meas'))
        input_1 = float(user_answer.get('input_1'))
        input_2 = float(user_answer.get('input_2'))
        input_3 = float(user_answer.get('input_3'))
        parameters = eval(self.get_checked_point_parameters())
        nominal_value = float(parameters[0])
        type_error = str(parameters[1])
        permissible_error = float(parameters[2])
        if type_error == '"abs"':
            error = (input_1 + input_2 + input_3)/3 - nominal_value
        else:
            error = ((input_1 + input_2 + input_3)/3 - nominal_value)*100/nominal_value
        if abs(error) < permissible_error:
            return self.last_method()
        else:
            self.next_method('repeat')
            text_message = 'Измеренное значение не в допуске. Повторить?'
            response_options = 'Да;Нет'
            return self.show_question(text_message, response_options)

    def repeat(self):
        user_answer = eval(self.return_user_answer('check_user_answer'))
        result_visual = user_answer.get('choice')
        if result_visual == 'Да':
            self.next_method('meas')
        else:
            self.next_method('last_method')
        return self.redirect_in_next_method()


class Result(BaseFunction):
    start_method = 'end_check'

    def end_check(self):
        message = 'Поверка завершена'
        self.next_method('last_method')
        return self.show_message(message)
