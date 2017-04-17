from .config import db

session = db.session


def init_db():
    # ModelBase.metadata.create_all(engine)
    db.create_all()


def drop_all():
    # ModelBase.metadata.drop_all(engine)
    db.drop_all()

# def list_tests(engine):
#
