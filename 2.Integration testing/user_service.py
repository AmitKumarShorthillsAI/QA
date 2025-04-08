class UserService:
    def __init__(self):
        # Simulated user database (in-memory dictionary)
        self.users = {
            "admin": "password123",
            "john_doe": "securepass"
        }

    def get_password(self, username):
        """Fetch the password for a given username (simulating a database query)."""
        return self.users.get(username, None)
