from user_package.user import User
from uuid import uuid4

VALID_USER_TYPES = ['user', 'admin', 'guest']

class AppUser(User):
    """
    App User class

    Subclass of User class that could be used in an application.
    """
    def __init__(self, name: str, user_type: str, email: str = ""):
        """
        Constructor
        :param name: username
        :param user_type: user type, see VALID_USER_TYPES
        :param email: user email

        Raises ValueError if user type is invalid
        """
        if user_type.lower() not in VALID_USER_TYPES:
            raise ValueError("Invalid user type")
        super().__init__(name)
        self.user_type = user_type.lower()
        self.id = ""
        self.is_active = False
        self.email = email

    def generate_id(self):
        """
        Generate a random user id
        :return: unique user id
        """
        self.id = str(uuid4())
        return self.id

    def is_admin(self):
        """
        Check if user is admin
        :return: True is admin, False otherwise
        """
        return self.user_type.lower() == 'admin'

    def is_guest(self):
        """
        Check if user is guest
        :return: True is guest, False otherwise
        """
        return self.user_type.lower() == 'guest'

    def is_user(self):
        """
        Check if user is user
        :return: True is user, False otherwise
        """
        return self.user_type.lower() == 'user'

    def is_active(self):
        """
        Check if user is active
        :return: True is active, False otherwise
        """
        return self.is_active == True


