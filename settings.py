# -*- coding: utf-8 -*-
from tinydb import TinyDB
import os

# Data base
db = TinyDB('db.json')

# Directories data
base_dir = os.path.abspath(os.path.dirname(__file__))

# JWT
JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 600
