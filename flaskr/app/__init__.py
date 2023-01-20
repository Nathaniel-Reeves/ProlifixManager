from flask import Flask

from app import auth
from app import blog
from app import hello
from app import home
from app import organizations
from app import people

from db import db_conf as db

app = Flask(__name__)


app.register_blueprint(auth.bp)
app.register_blueprint(blog.bp)
app.register_blueprint(home.bp)
app.register_blueprint(hello.bp)
app.register_blueprint(organizations.bp)
app.register_blueprint(people.bp)


app.config['UPLOAD_FOLDER'] = db.UPLOAD_FOLDER
app.config['SECRET_KEY'] = '7f8408c53127a46b97cb365e09d9f103ce055cfee2ee35f4625986653d2eb732'
