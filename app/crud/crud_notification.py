from typing import List
import uuid
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.notification import Notification
from app import schemas, models


class CrudNotification(CRUDBase[Notification, schemas.NotificationCreate, schemas.NotificationUpdate]):
    def create_notify(self, db: Session, obj_in: schemas.NotificationCreate):
        """
        Создать уведомление
        """
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['user_id'] = uuid.UUID(obj_in_data['user_id'])
        db_obj = models.Notification(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_user(self, db: Session, user: schemas.User, skip: int = 0, limit: int = 100) -> List[Notification]:
        """
        Получить уведомления пользователя
        """   
        return db.query(self.model).filter(Notification.user_id == user.id)\
            .filter(Notification.read == False).offset(skip).limit(limit).all()

notification = CrudNotification(Notification)