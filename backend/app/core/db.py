from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine, select

# ⚠️ Comentamos imports que requieren modelos aún no definidos
# from app import crud
# from app.models import User, UserCreate

from app.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel
    # SQLModel.metadata.create_all(engine)

    # ⚠️ Desactiva la lógica de superusuario hasta que tengas el modelo User
    pass

    # user = session.exec(
    #     select(User).where(User.email == settings.FIRST_SUPERUSER)
    # ).first()
    # if not user:
    #     user_in = UserCreate(
    #         email=settings.FIRST_SUPERUSER,
    #         password=settings.FIRST_SUPERUSER_PASSWORD,
    #         is_superuser=True,
    #     )
    #     user = crud.create_user(session=session, user_create=user_in)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
