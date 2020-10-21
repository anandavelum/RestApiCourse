from app import app
from db import db

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
    try:
        user = User(3, "Nakshathra", "Nakshathra")
        user.save_to_db()
        user = User(4, "Murugan", "Murugan")
        user.save_to_db()
    except:
        print('User already present')
