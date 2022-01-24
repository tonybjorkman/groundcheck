from sqlalchemy.orm import sessionmaker
from models import *

class Database:

    def create_session():
        """
        Create a session object to work with the database
        """
        engine = create_engine('sqlite:///cats.db', echo=False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session


def __main__():
    session = Database().create_session()
    # adds example cat to db
    cat_one = Cat(name="good cat")
    session.add(cat_one)
    session.commit()

    print("cat in db:"+str(session.query(Cat).first().timestamp))

