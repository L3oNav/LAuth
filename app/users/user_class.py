from app.users.models import User
from app.settings.database import get_session

class UserManager:

    def __init__(self):
        self.session = get_session

    def create_user_google(self, user_info):
        session = self.session
        session = next(session())
        exist = session.query(User).filter_by(email=user_info['email']).first()
        if exist:
            return False
        new_user = User(
            email=user_info['email'],
            email_verified=user_info['email_verified'],
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return True

user_manager = UserManager()
