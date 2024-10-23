from repositories.user_repository import UserRepository

class UserService:
    def __init__(
        self, user_repository: UserRepository
    ):
        self._user_repository = user_repository

    def get_all(self):
        return self._user_repository.get_all()
    
    def create(self, name, email, password):
        user = self._user_repository.create(
            name,
            email,
            password
        )
        return user