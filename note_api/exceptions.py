from rest_framework.exceptions import APIException

class MismatchNoteAuthor(Exception):
    def __init__(self, id_from_instance, user_id):
        self.text = f"Id пользователя в поле author, экземпляра Note, должен совпадать с id " \
                    f"пользователя редактирующего! В модели автор id - {id_from_instance} != {user_id}"
