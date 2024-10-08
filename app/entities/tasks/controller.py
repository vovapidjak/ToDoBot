from sqlalchemy.exc import SQLAlchemyError

from . import models
from ..tasks.models import TaskTable
from ...database import SessionLocal


class Task:
    model = models.TaskTable
    db = SessionLocal()

    def __init__(self, task: model, user_id, description):
        self.db_entity: models.TaskTable = task


    @classmethod
    def add_task(cls, user_id, description):
        """Добавляет задачу в базу данных."""
        new_task = cls.model(user_id=user_id, description=description)

        try:
            cls.db.add(new_task)
            cls.db.commit()
            return True, f"Задача '{description}' добавлена!"
        except SQLAlchemyError as e:
            cls.db.rollback()
            return False, "Произошла ошибка при добавлении задачи."
        finally:
            cls.db.close()


    @classmethod
    def get_tasks(cls, user_id):
        """Получает список задач пользователя."""
        try:
            tasks = cls.db.query(cls.model).filter_by(user_id=user_id).all()
            return tasks
        finally:
            cls.db.close()


    @classmethod
    def delete_task(cls, user_id, task_index):
        """Удаляет задачу по индексу для указанного пользователя."""
        tasks = cls.db.query(cls.model).filter_by(user_id=user_id).all()

        if not tasks or task_index >= len(tasks):
            return False, "Некорректный номер задачи."

        task_to_delete = tasks[task_index]

        try:
            cls.db.delete(task_to_delete)
            cls.db.commit()
            return True, f"Задача '{task_to_delete.description}' удалена."
        except SQLAlchemyError as e:
            cls.db.rollback()
            return False, "Произошла ошибка при удалении задачи."
        finally:
            cls.db.close()


    @classmethod
    def clear_tasks(cls):
        # TODO: добавить проверку не пустой ли список с задачами
        cls.db.query(cls.model).delete()  # Удаляем все задачи
        cls.db.commit()
        cls.db.close()