from datetime import datetime
from typing import Optional
from pydantic import BaseModel, UUID4


class NotificationBase(BaseModel):
    user_id: Optional[UUID4]
    text: Optional[str]
    link: Optional[str]
    read: Optional[bool] = False


class NotificationCreate(NotificationBase):
    user_id: UUID4
    text: str
    link: str
    read: bool = False  

class NotificationUpdate(NotificationBase):
    id: Optional[UUID4]
    user_id: Optional[UUID4]
    text: Optional[str]
    link: Optional[str]
    read: Optional[bool] = False


class NotificationInDB(NotificationBase):
    id: UUID4
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True