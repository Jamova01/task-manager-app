from fastapi import APIRouter, status

from app.core.db import SessionDep
from app.models import UsersPublic
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
    # dependencies=[Depends(get_current_user_with_roles(["admin"]))],
)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> UsersPublic:
    service = UserService(session)
    return service.get_users(skip=skip, limit=limit)
