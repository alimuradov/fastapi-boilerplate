from sqlalchemy.orm import Session
from datetime import datetime
from app import crud, schemas
from app.core.config import settings

def init_db(db: Session) -> None:

    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            role="super_admin",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841