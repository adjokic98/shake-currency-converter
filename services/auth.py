import uuid

class AuthService:
    @staticmethod
    def generate_api_key():
        """Generates a unique API key."""
        return str(uuid.uuid4())