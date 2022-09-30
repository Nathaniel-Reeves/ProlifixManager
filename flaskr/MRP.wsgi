import sys
import os
import logging
from logging import Formatter, FileHandler
from logging.handlers import RotatingFileHandler

#broken
#logging.basicConfig(level=logging.DEBUG, filename='/var/www/html/Material-Requirements-Planning-System/flaskr/logs/MRP.log', format='%(asctime)s %(message)s')

sys.path.insert(0, '/var/www/html/Material-Requirements-Planning-System')
sys.path.insert(0, '/var/www/html/venv/lib/python3.10/site-packages')


from flaskr.app import create_app
application = create_app()

activate_this = '/var/www/html/venv/bin/activate'
#with open(activate_this) as file_:
#	exec(file_.read(), dict(__file__=activate_this))

if not application.debug:

    logdir = '/var/www/html/Material-Requirements-Planning-System/flaskr/logs/'

    file_handler = FileHandler('/tmp/access.log')
    #file_handler = FileHandler(logdir + 'access.log')
    #file_handler = RotatingFileHandler(logdir + 'access.log', maxBytes=20000000, backupCount=10)
    file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s'))

    logging.getLogger('werkzeug').setLevel(logging.INFO)
    logging.getLogger('werkzeug').addHandler(file_handler)

    logger = logging.getLogger(__name__) 

    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

    # adding some debug
    logger.info(os.environ)
    logger.info(os.path.dirname(logdir).format())
    logger.info(os.listdir(logdir))
