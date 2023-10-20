from app.users.models import User, Account
from app.settings.database import get_session

class UserManager:

    def __init__(self):
        self.session = get_session

    def _create_account(self, user_info, user_id):
        exist_account = session.query(Account).filter_by(issuer=user_info['iss'], subject=user_info['sub']).first()
        if exist_account:
            return None
        new_account = Account(
            issuer=user_info['iss'],
            subject=user_info['sub'],
            user_id=user_id
        )
        return new_account

    def create_user(self, user_info):
        session = self.session
        session = next(session())
        exist_user = session.query(User).filter_by(email=user_info['email']).first()
        if exist_user:
            raise 
        new_user = User(
            email=user_info['email'],
            email_verified=user_info['email_verified'],
        )
        new_account = self._create_account(self, user_info=user_info, new_user.id)
        new_user.accounts.append(new_account)
        new_account.user = new_user
        session.add(new_user)
        session.add(new_account)
        session.commit()
        session.close()
        return new_user 

user_manager = UserManager()
