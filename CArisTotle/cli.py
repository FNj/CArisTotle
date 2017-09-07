from .config import app
from .datamodel.procedures import init_db, drop_all


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
    from .dev.test_data import test_data
    test_data()
    print("Test data inserted into the database.")
