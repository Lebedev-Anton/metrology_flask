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
        text_message = self.return_user_answer('do_visual')
        print(text_message)
        self.next_method('last_method')
        return self.show_message(text_message)


class Testing(BaseFunction):
    start_method = 'preparation_device'

    def preparation_device(self):
        text_message = 'Выполните тестирование'
        self.next_method('check_user_answer')
        return self.show_message(text_message)

    def check_user_answer(self):
        text_message = 'Выполните тестирование 2'
        self.last_method()
        return self.show_message(text_message)

