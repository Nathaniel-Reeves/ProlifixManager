from flask import Flask
from werkzeug.utils import import_string


"""
Config Settings for Flask App
"""
app = Flask(__name__)


cfg = import_string('configmodule.Work_Laptop_Config')()
# cfg = import_string('configmodule.Home_PC_Config')()
# cfg = import_string('configmodule.School_Laptop_Config')()
# cfg = import_string('configmodule.Pi_Server_Config')()

app.config.from_object(cfg)
print(app.config["DB_CREDENTIALS"])
print(app.config["MESSAGE"])


"""
Import Views
"""

from mrp_app.views import home
app.register_blueprint(home.bp)

from mrp_app.views import auth
app.register_blueprint(auth.bp)

from mrp_app.views import blog
app.register_blueprint(blog.bp)

from mrp_app.views import organizations
app.register_blueprint(organizations.bp)

from mrp_app.views import people
app.register_blueprint(people.bp)
