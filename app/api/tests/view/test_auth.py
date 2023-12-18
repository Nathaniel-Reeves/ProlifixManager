import json
import pytest

from main.wsgi import create_app
from main.view.response import CustomResponse
from view import auth as auth

