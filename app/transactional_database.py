from sqlmodel import create_engine, SQLModel, Session

class TransactionalDatabase:
    def __init__(self):
        self.engine = create_engine("sqlite:///database.db")
        SQLModel.metadata.create_all(self.engine)
        
    def get_session(self):
        return Session(self.engine)

