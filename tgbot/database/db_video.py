import sqlite3 as sq

from pydantic import BaseModel

from tgbot.data.config import PATH_DATABASE
from tgbot.utils.const_functions import get_unix, ded
from tgbot.database.db_helper import update_format_where, dict_factory


# Модель таблицы
class UserModel(BaseModel):
    increment: int
    video_id: int
    video_name: str
    video_size: int
    video_duration: int


class Videox():
    storage_name = 'storage_video'

    # Добавление user'а
    @staticmethod
    def add(video_id: int, video_name: str, video_size: int, video_duration: int):
        with sq.connect(PATH_DATABASE) as con:
            con.execute(
                ded(f"""
                                INSERT INTO {Videox.storage_name} (
                                    video_id,
                                    video_name,
                                    video_size,
                                    video_duration
                                    
                                ) VALUES (?, ?, ?, ?)
                            """),
                [
                    video_id,
                    video_name,
                    video_size,
                    video_duration,
                ],
            )

    # Проверка на уникальное видео
    @staticmethod
    def video_unic(video_name, video_size, video_duration):
        with sq.connect(PATH_DATABASE) as con:
            result = con.execute(
                f'SELECT * FROM {Videox.storage_name} WHERE video_name = ? AND video_size = ? AND video_duration = ?',
                (video_name, video_size, video_duration)).fetchall()

            return not bool(len(result))
