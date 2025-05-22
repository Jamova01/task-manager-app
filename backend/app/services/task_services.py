import uuid
from fastapi import HTTPException, status
from sqlmodel import Session, select, func

from app.models import User, Task, TaskCreate, TaskUpdate, TasksPublic

MAX_LIMIT = 100


class TaskService:
    def __init__(self, session: Session):
        self.session = session

    def get_tasks(
        self, current_user: User, skip: int = 0, limit: int = 100
    ) -> TasksPublic:
        if skip < 0 or limit <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Skip and limit must be positive numbers.",
            )

        limit = min(limit, MAX_LIMIT)

        if current_user.is_superuser:
            count_statement = select(func.count()).select_from(Task)
            total = self.session.exec(count_statement).one()

            statement = select(Task).offset(skip).limit(limit)
            tasks = self.session.exec(statement).all()
        else:
            count_statement = (
                select(func.count())
                .select_from(Task)
                .where(Task.owner_id == current_user.id)
            )
            total = self.session.exec(count_statement).one()

            statement = (
                select(Task)
                .where(Task.owner_id == current_user.id)
                .offset(skip)
                .limit(limit)
            )
            tasks = self.session.exec(statement).all()

        return TasksPublic(data=tasks, count=total)

    def get_task_by_id(self, task_id: uuid.UUID, current_user: User) -> Task:
        task = self.session.get(Task, task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )

        if not current_user.is_superuser and task.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
            )

        return task

    def create_task(self, task_data: TaskCreate, current_user: User) -> Task:
        new_task = Task.model_validate(task_data, update={"owner_id": current_user.id})
        self.session.add(new_task)
        self.session.commit()
        self.session.refresh(new_task)
        return new_task

    def update_task(
        self, task_id: uuid.UUID, task_data: TaskUpdate, current_user: User
    ) -> Task:
        task = self.session.get(Task, task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        if not current_user.is_superuser and task.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")

        update_data = task_data.model_dump(exclude_unset=True)
        task.sqlmodel_update(update_data)

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete_task(self, task_id: uuid.UUID, current_user: User) -> None:
        task = self.session.get(Task, task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        if not current_user.is_superuser and task.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")

        self.session.delete(task)
