import sqlite3 as sq

from pydantic import BaseModel

from tgbot.data.config import PATH_DATABASE
from tgbot.utils.const_functions import get_unix, ded
from tgbot.database.db_helper import update_format_where, dict_factory


# Модель таблицы
class UserModel(BaseModel):
    increment: int
    user_id: int
    user_balance: int
    user_referral: int
    user_unix: int
    user_ban: int


# Работа с юзером
class Userx():
    storage_name = 'storage_users'

    # Добавление user'а
    @staticmethod
    def add(user_id: int):
        user_balance = 0
        user_referral = 0
        user_unix = get_unix()
        user_ban = 0

        with sq.connect(PATH_DATABASE) as con:
            con.execute(
                ded(f"""
                                INSERT INTO {Userx.storage_name} (
                                    user_id,
                                    user_balance,
                                    user_referral,
                                    user_unix,
                                    user_ban
                                ) VALUES (?, ?, ?, ?, ?)
                            """),
                [
                    user_id,
                    user_balance,
                    user_referral,
                    user_unix,
                    user_ban,
                ],
            )

    # Получение записи
    @staticmethod
    def get(**kwargs) -> UserModel:
        with sq.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Userx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchone()

            if response is not None:
                response = UserModel(**response)

            return response

    # Получение id всех записей
    @staticmethod
    def get_all_id():
        with sq.connect(PATH_DATABASE) as con:
            total_id = con.execute(f'SELECT user_id FROM {Userx.storage_name}').fetchall()

            return total_id

    @staticmethod
    def user_ban_unban(user_id):
        with sq.connect(PATH_DATABASE) as con:
            user = Userx.get(user_id=user_id)
            if user.user_ban == 0:
                con.execute(f'UPDATE {Userx.storage_name} SET user_ban = ?', (1,))
                return True
            else:
                con.execute(f'UPDATE {Userx.storage_name} SET user_ban = ?', (0,))
                return False

    # Получение количества всех записей
    @staticmethod
    def get_all_count():
        with sq.connect(PATH_DATABASE) as con:
            total_count = con.execute(f'SELECT * FROM {Userx.storage_name}').fetchall()

            return len(total_count)

    # Проверка на запись пользователя в бд
    @staticmethod
    def user_exist(user_id):
        with sq.connect(PATH_DATABASE) as con:
            result = con.execute(f'SELECT * FROM {Userx.storage_name} WHERE user_id = ?', (user_id,)).fetchone()

            return bool(len(result))

    # Проверка на правдивость реферальной ссылки
    @staticmethod
    def user_check_ref(referral_id):
        with sq.connect(PATH_DATABASE) as con:
            result = con.execute(f'SELECT * FROM {Userx.storage_name} WHERE user_id = ?', (referral_id,)).fetchone()
            return bool(len(result))

    # Изменение реферального кода, для пользователей без реферала
    @staticmethod
    def user_without_ref(user_id):
        with sq.connect(PATH_DATABASE) as con:
            if Userx.get(user_id=user_id).user_referral < 1:
                con.execute(f'UPDATE {Userx.storage_name} SET user_referral = ?', (1,))

    # Добавление id реферала в нового юзера
    @staticmethod
    def user_add_ref(user_id, referral_id):
        with sq.connect(PATH_DATABASE) as con:
            con.execute(f'UPDATE {Userx.storage_name} SET user_referral = ? WHERE user_id = ?',
                        (referral_id, user_id,))

    # + ко времени пользователю
    @staticmethod
    def user_uptime(user_id, minutes):
        user = Userx.get(user_id=user_id)
        current_time = get_unix()

        with sq.connect(PATH_DATABASE) as con:
            if user.user_unix < current_time:
                con.execute(f'UPDATE {Userx.storage_name} SET user_unix = ? WHERE user_id = ?',
                            ((current_time + 60 * minutes), user_id,))
            else:
                con.execute(f'UPDATE {Userx.storage_name} SET user_unix = ? WHERE user_id = ?',
                            ((user.user_unix + 60 * minutes), user_id,))
