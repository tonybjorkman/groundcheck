from sqlalchemy import create_engine

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///db.sqlite',connect_args={'check_same_thread': False},echo=True)

Session = scoped_session(sessionmaker(bind=engine))
session = Session()