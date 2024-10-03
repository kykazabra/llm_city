class ProfilePost:
    def __init__(self, title, text):
        self.title = title
        self.text = text

    def post(self):
        # Posing to api
        print('Запрос на написание поста был отправлен на сервер!')

    def __repr__(self):
        return 'ProfilePost(' + ', '.join([f"{key}='{value}'" for key, value in self.__dict__.items()]) + ')'