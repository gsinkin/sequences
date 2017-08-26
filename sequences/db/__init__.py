import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URI = os.environ["DATABASE_URI"]
ENGINE = None


def get_engine():
    global ENGINE
    if ENGINE:
        return ENGINE
    ENGINE = create_engine(DATABASE_URI)
    return ENGINE


def get_session():
    return sessionmaker(bind=ENGINE)()


class Transaction(object):

    def __init__(self):
        self.engine = get_engine()
        self.session = get_session()

    def begin(self):
        return self.session

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()

    def __enter__(self):
        return self.begin()

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type:
            self.rollback()
        else:
            self.commit()
