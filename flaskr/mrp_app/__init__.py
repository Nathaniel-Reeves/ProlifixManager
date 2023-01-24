from flask import Flask
from werkzeug.utils import import_string


"""
Config Settings for Flask App
"""
app = Flask(__name__, instance_relative_config=True)


cfg = import_string('configmodule.Work_Laptop_Config')()
# cfg = import_string('configmodule.Home_PC_Config')()
# cfg = import_string('configmodule.Home_PC_To_Pi_Config')()
# cfg = import_string('configmodule.School_Laptop_Config')()
# cfg = import_string('configmodule.Pi_Server_Config')()

app.config.from_object(cfg)
print(app.config["MESSAGE"])
print('~~~ DATABASE CONFIG ~~~')
print('    Host:         ', app.config["DB_CREDENTIALS"]['host'])
print('    Port:         ', app.config["DB_CREDENTIALS"]['port'])
print('    SQL User:     ', app.config["DB_CREDENTIALS"]['user'])
print('    SQL Password: ', app.config["DB_CREDENTIALS"]['password'])
print()
print('~~~ SERVER START ~~~')
print()

"""
Import Views
"""

from mrp_app.views import home
app.register_blueprint(home.bp)

from mrp_app.views import auth
app.register_blueprint(auth.bp)

from mrp_app.views import organizations
app.register_blueprint(organizations.bp)
