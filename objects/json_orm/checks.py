from objects.json_orm.errors import *


class CheckClass(object):
    database: 'Database'
    only_startup: bool = True

    @classmethod
    def get_all_checks(cls):
        return cls.__subclasses__()

    def __init__(self, database: 'Database'):
        self.database = database

    def check(self):
        pass


class FieldsCheck(CheckClass):

    fix_database = {
        "ru_captcha_key": "",
        "delete_all_notify": False,
        "role_play_commands": [],
        "ignored_members": [],
        "ignored_global_members": [],
        "auto_exit_from_chat": False,
        "auto_exit_from_chat_delete_chat": False,
        "auto_exit_from_chat_add_to_black_list": False,
        "sloumo": []
    }

    def check(self):
        for key in self.database.__all_fields__:
            if key not in self.database:
                if key in self.fix_database:
                    self.database.update({key: self.fix_database[key]})
                    self.database.save()
                else:
                    raise DatabaseError(
                        name='Нет поля',
                        description=f'В базе данных не хватает поля "{key}"'
                    )


class TokensCountCheck(CheckClass):

    def check(self):
        if len(self.database.tokens) < 1:
            raise DatabaseError(
                name='Нет токенов',
                description='Укажите токены в файле конфигурации'
            )

        if len(self.database.tokens) < 3:
            raise DatabaseWarning(
                name='Малое количество токенов',
                description='Слишком мало токенов, рекомендуемое количество 3 и более.'
            )


class SecretCodeCheck(CheckClass):

    def check(self):
        if not self.database.secret_code:
            raise DatabaseError(
                name='Нет секретного кода',
                description='Укажите секретный код в файле конфигурации'
            )
