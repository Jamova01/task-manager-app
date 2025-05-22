from typing import Annotated
from datetime import timedelta
from fastapi import HTTPException, status

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.db import SessionDep
from app.core.config import settings
from app.models import Token
from app.services.user_services import UserService
from app.auth.security import create_access_token

router = APIRouter(tags=["login"])


@router.post("/login/access-token")
def login_acess_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user_service = UserService(session)
    user = user_service.authenticate_user_service(
        email=form_data.username,
        password=form_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token)
