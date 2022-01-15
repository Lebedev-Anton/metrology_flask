from web_app.scripts import BaseFunction


class Visual(BaseFunction):
    start_method = 'preparation_device'

    def preparation_device(self):
        text_message = 'Подготовте прибор к внешнему осмотру'
        self.next_method('do_visual')
        return self.show_message(text_message)

    def do_visual(self):
        text_message = 'Внешний осмотр соответсвует?'
        response_options = 'Да;Нет'
        self.next_method('check_user_answer')
        return self.show_question(text_message, response_options)

    def check_user_answer(self):
        user_answer = eval(self.return_user_answer('do_visual'))
        result_visual = user_answer.get('choice')
        if result_visual == 'Да':
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
        text_message = 'Выполните Опробование согласно МП'
        self.next_method('do_testing')
        return self.show_message(text_message)

    def do_testing(self):
        text_message = 'Обпробование соответсвует?'
        response_options = 'Да;Нет'
        self.next_method('check_user_answer')
        return self.show_question(text_message, response_options)

    def check_user_answer(self):
        user_answer = eval(self.return_user_answer('do_testing'))
        result_visual = user_answer.get('choice')
        if result_visual == 'Да':
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
        message = 'Введите измеренное значение'
        self.next_method('check_user_answer')
        return self.show_number(message)

    def check_user_answer(self):
        user_answer = eval(self.return_user_answer('meas'))
        result_number = float(user_answer.get('number'))
        parameters = eval(self.get_checked_point_parameters())
        nominal_value = float(parameters[0])
        type_error = str(parameters[1])
        permissible_error = float(parameters[2])
        if type_error == '"abs"':
            error = result_number - nominal_value
        else:
            error = (result_number - nominal_value)/nominal_value

        if error < permissible_error:
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
        self.next_method('stop_script')
        return self.show_message(message)
