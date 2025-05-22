import uuid
from fastapi import APIRouter, Depends, status

from app.core.db import SessionDep
from app.models import TaskCreate, TaskUpdate, TaskPublic, TasksPublic, Message
from app.services.task_services import User, TaskService
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.get(
    "/",
    summary="List all tasks",
    status_code=status.HTTP_200_OK,
    response_model=TasksPublic,
    responses={
        200: {"description": "A list of tasks"},
    },
)
def read_tasks(
    session: SessionDep,
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> TasksPublic:
    service = TaskService(session)
    return service.get_tasks(current_user=current_user, skip=skip, limit=limit)


@router.get("/{task_id}", response_model=TaskPublic)
def read_task(
    task_id: uuid.UUID,
    session: SessionDep,
    current_user: User = Depends(get_current_user),
) -> TaskPublic:
    """
    Get task by ID.
    """
    service = TaskService(session)
    return service.get_task_by_id(task_id=task_id, current_user=current_user)


@router.post("/", response_model=TaskPublic, status_code=201)
def create_task(
    task_data: TaskCreate,
    session: SessionDep,
    current_user: User = Depends(get_current_user),
) -> TaskPublic:
    service = TaskService(session)
    return service.create_task(task_data=task_data, current_user=current_user)


@router.put("/{task_id}", response_model=TaskPublic)
def update_task(
    *,
    session: SessionDep,
    current_user: User = Depends(get_current_user),
    task_id: uuid.UUID,
    task_data: TaskUpdate,
) -> TaskPublic:
    service = TaskService(session)
    return service.update_task(
        task_id=task_id, task_data=task_data, current_user=current_user
    )


@router.delete("/{task_id}", response_model=Message)
def delete_task(
    task_id: uuid.UUID,
    session: SessionDep,
    current_user: User = Depends(get_current_user),
) -> Message:
    service = TaskService(session)
    service.delete_task(task_id=task_id, current_user=current_user)
    return Message(message="Task deleted successfully")
