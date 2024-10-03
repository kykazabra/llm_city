from .models import AgentProfile
from sqlalchemy.exc import SQLAlchemyError
import functools
from sqlalchemy.orm.session import Session
from sqlalchemy import create_engine
import os


def get_session():
    return Session(create_engine(os.environ.get('DB_CONNECTION_STRING')))


def with_session(fn):
    """Decorator for handling sessions."""

    @functools.wraps(fn)
    def func(*args, **kwargs):
        session = None

        if not kwargs.get("session"):
            session = get_session()
            kwargs["session"] = session

        if session is not None:
            try:
                return fn(*args, **kwargs)
            except SQLAlchemyError as e:
                session.rollback()
                raise e
            finally:
                session.close()
        else:
            return fn(*args, **kwargs)

    return func


@with_session
def load_agent_profile(id: int, session=None) -> AgentProfile:
    return session.query(AgentProfile).get(id)
