import asyncio
import logging
import json
from typing import Any, List
from jose import jwt
from sqlalchemy.orm import Session

from fastapi import APIRouter, Request, Query, HTTPException, status, Depends, Security
from fastapi.encoders import jsonable_encoder
from sse_starlette.sse import EventSourceResponse
from pydantic import ValidationError

from app.core import security, settings
from app import schemas, crud, models
from api.deps import get_db, get_current_active_user

STREAM_DELAY = 5  # second
RETRY_TIMEOUT = 15000  # milisecond


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("", response_model=List[schemas.NotificationInDB])
def read_notifications(
    db: Session = Depends(get_db), 
    current_user: models.User = Security(
        get_current_active_user,
        scopes=['super_admin', 'admin', 'chief', 'doctor']
    ),    
    skip: int = 0, 
    limit: int = 100) -> Any:
    """
    Retrieve all notifications.
    """
    notifications = crud.notification.get_by_user(db, user=current_user ,skip=skip, limit=limit)
    return notifications

@router.post("/create")
async def create_notifications(
    db: Session = Depends(get_db),
    current_user: models.User = Security(
        get_current_active_user,
        scopes=['super_admin', 'admin', 'chief', 'doctor']
    ),
    notify_in: schemas.NotificationCreate = None
) -> Any:
    """
    Создание уведомления
    """
    notification = crud.notification.create_notify(db, obj_in=notify_in)
    return notification


@router.get("/sse", response_model=List[schemas.NotificationInDB])
async def notifications_stream(request: Request, token: str = Query(None), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    def new_notofications():
        # Add logic here to check for new messages
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
            )
            if payload.get("id") is None:
                raise credentials_exception        
            token_data = schemas.TokenPayload(**payload)
        except (jwt.JWTError, ValidationError):
            logger.error("Error Decoding Token", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                )     
        user = crud.user.get(db, model_id=token_data.id)
        if not user:
            raise credentials_exception
        notifications = crud.notification.get_by_user(db, user, skip=0, limit=100)
        return notifications
    async def event_generator():
        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break

            # Checks for new messages and return them to client if any
            notifications = new_notofications()
            if notifications:
                yield {
                        "event": "notify",
                        # "id": "message_id",
                        # "retry": RETRY_TIMEOUT,
                        "data": jsonable_encoder(notifications)
                }

            await asyncio.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())