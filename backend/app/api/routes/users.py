from fastapi import APIRouter, status

from app.core.db import SessionDep
from app.models import UserCreate, UserPublic, UsersPublic
from app.services.user_services import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get(
    "/",
    summary="List all users",
    response_model=UsersPublic,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "A list of users"},
    },
)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> UsersPublic:
    service = UserService(session)
    return service.get_users(skip=skip, limit=limit)


@router.post(
    "/",
    summary="Create a new user",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Bad Request"},
        409: {"description": "Email already registered"},
    },
)
def create_user(session: SessionDep, user_data: UserCreate) -> UserPublic:
    service = UserService(session)
    return service.create_user(user_data=user_data)
