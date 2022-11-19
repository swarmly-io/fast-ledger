from sqlmodel import create_engine, SQLModel, Session

class TransactionalDatabase:
    def __init__(self, db_name = "database"):
        self.engine = create_engine("sqlite:///" + db_name + ".db")
        SQLModel.metadata.create_all(self.engine)
        
    def get_session(self):
        return Session(self.engine)        

