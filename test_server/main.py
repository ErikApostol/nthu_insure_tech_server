from __init__ import app, db
from init_db.user.model import User

@app.route('/')
def index():

    return 'ok'


if __name__ == "__main__":
    db.create_all()
    app.run()