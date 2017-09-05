from .config import app, db
from .datamodel.procedures import init_db, drop_all, session
from .dev.test_data import entities
from .routing import *


@app.cli.command('initdb')
def initdb():
    init_db()
    print('Database initialized.')


@app.cli.command('dropall')
def dropall():
    really = input('Are you sure you want to delete all data in the database? [y/n] \n')
    if really in ('y', 'Y'):
        drop_all()
        print('Database purged.')
    else:
        print("Nothing was done.")


@app.cli.command('testdata')
def testdata():
    session.add_all(entities)
    session.commit()
    print("Test data inserted into the database.")
