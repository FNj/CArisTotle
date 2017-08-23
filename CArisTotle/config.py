from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy

from .forms import ExtendedRegisterForm

app = Flask('CArisTotle')

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config["lang"] = 'cs'
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.jinja_env.globals.update(zip=zip, len=len)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.sqlite'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECURITY_PASSWORD_SALT'] = 'iangawegkaowengoaweggawe51g6a1ga6r1g6a5d'
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_CHANGEABLE'] = True

app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_SEND_PASSWORD_CHANGE_EMAIL'] = False
app.config['SECURITY_SEND_PASSWORD_RESET_EMAIL'] = False
app.config['SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL'] = False

app.config['CARISTOTLE_TIME_LIMIT_GRACE_SECONDS'] = 30

db = SQLAlchemy(app)

from .datamodel.model import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=ExtendedRegisterForm,
                    confirm_register_form=ExtendedRegisterForm)
