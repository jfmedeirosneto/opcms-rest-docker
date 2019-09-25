# -*- coding: utf-8 -*-
import os
from tinydb import TinyDB

# Base dir
base_dir = os.path.abspath(os.path.dirname(__file__))

# App data dir
app_data_dir = os.path.join(base_dir, 'app-data')
if not os.path.exists(app_data_dir):
    os.makedirs(app_data_dir)

# Data base
db = TinyDB(os.path.join(app_data_dir, 'db.json'))

# JWT
JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 600
