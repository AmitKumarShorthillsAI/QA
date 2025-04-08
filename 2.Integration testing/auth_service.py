from user_service import UserService

class AuthService:
    def __init__(self):
        self.user_service = UserService()  # Dependency

    def authenticate(self, username, password):
        """Authenticate by checking username and password."""
        stored_password = self.user_service.get_password(username)
        if stored_password and stored_password == password:
            return "Access Granted"
        return "Access Denied"
