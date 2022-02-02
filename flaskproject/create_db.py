#run from parent dir with 
# python3 flaskproject/create_db.py
from models import Base
from db import engine

Base.metadata.create_all(bind=engine)