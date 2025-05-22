from typing import Any
import uuid
from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_active_superuser, get_current_user
from app.core.db import SessionDep
from app.models import (
    UpdatePassword,
    User,
    UserCreate,
    UserRegister,
    UserUpdate,
    UserUpdateMe,
    UserPublic,
    UsersPublic,
    Message,
)
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
    dependencies=[Depends(get_current_active_superuser)],
    responses={
        200: {"description": "A list of users"},
    },
)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> UsersPublic:
    service = UserService(session)
    return service.get_users(skip=skip, limit=limit)


@router.get(
    "/me",
    response_model=UserPublic,
    summary="Get current user info",
    status_code=status.HTTP_200_OK,
)
def get_my_info(current_user: User = Depends(get_current_user)) -> UserPublic:
    return current_user


@router.patch("/me", response_model=UserPublic)
def update_user_me(
    *,
    session: SessionDep,
    user_data: UserUpdateMe,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update own user.
    """
    service = UserService(session)
    return service.update_current_user(current_user, user_data)


@router.patch("/me/password", response_model=Message)
def update_password_me(
    *,
    session: SessionDep,
    body: UpdatePassword,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update own password.
    """
    service = UserService(session)
    return service.update_current_user_password(current_user, body)


@router.delete("/me", response_model=Message)
def delete_user_me(
    session: SessionDep, current_user: User = Depends(get_current_user)
) -> Any:
    service = UserService(session)
    return service.delete_current_user(current_user)


@router.post("/signup", response_model=UserPublic)
def register_user(session: SessionDep, user_data: UserRegister) -> Any:
    service = UserService(session)
    return service.register_user(user_data)


@router.get(
    "/{user_id}",
    response_model=UserPublic,
    summary="Get user details",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "User details retrieved successfully"},
        404: {"description": "User not found"},
    },
)
def get_user(session: SessionDep, user_id: uuid.UUID) -> UserPublic:
    service = UserService(session)
    return service.get_user_by_id(user_id=user_id)


@router.patch(
    "/{user_id}",
    response_model=UserPublic,
    dependencies=[Depends(get_current_active_superuser)],
)
def update_user(
    *,
    session: SessionDep,
    user_id: uuid.UUID,
    user_data: UserUpdate,
) -> Any:
    service = UserService(session)
    return service.update_user_by_id(user_id, user_data)


@router.post(
    "/",
    summary="Create a new user",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_active_superuser)],
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Bad Request"},
        409: {"description": "Email already registered"},
    },
)
def create_user(session: SessionDep, user_data: UserCreate) -> UserPublic:
    service = UserService(session)
    return service.create_user(user_data=user_data)


@router.delete(
    "/{user_id}",
    summary="Delete a user",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_active_superuser)],
    responses={
        200: {"description": "User deleted successfully"},
        404: {"description": "User not found"},
    },
)
def delete_user(session: SessionDep, user_id: int) -> dict:
    service = UserService(session)
    return service.delete_user(user_id=user_id)
