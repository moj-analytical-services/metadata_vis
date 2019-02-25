import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from app.models import Database
from app import db

if __name__ == "__main__":

    db.drop_all() #TODO probably make this optional!!
    db.create_all()

    d = Database()
    d.name = "hello3"
    d.description = "first_db"

    db.session.add(d)
    db.session.commit()