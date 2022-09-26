import sys
import logging

logging.basicConfig(level=logging.DEBUG, filename='/var/www/html/Material-Requirements-Planning-System/flaskr/logs/MRP.log', format='%(asctime)s %(message)s')
sys.path.insert(0, '/var/www/html/Material-Requirements-Planning-System')
sys.path.insert(0, '/var/www/html/venv/lib/python3.10/site-packages')


from flaskr.app import create_app
application = create_app()

activate_this = '/var/www/html/venv/bin/activate'
#with open(activate_this) as file_:
#	exec(file_.read(), dict(__file__=activate_this))
