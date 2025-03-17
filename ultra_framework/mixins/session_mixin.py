from sqlalchemy.orm import Session


class SessionMixin:

    def __init__(self, session: Session):
        self.session = session

    def update_session(new_session: Session):
        self.session = new_session
        
