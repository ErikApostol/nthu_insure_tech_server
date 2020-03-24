import os

from server import db, create_app


db.create_all(app=create_app())
# export FLASK_APP=
os.system('export FLASK_APP=./server')
