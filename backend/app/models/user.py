"""
User Model

This model represents the users of the mobile voting platform. It handles user attributes and authentication details. The User model is a crucial part of the system, as it manages user-related data and operations, including:

Attributes:
- id: A unique identifier for each user, serving as the primary key.
- username: A unique string representing the user's chosen name, used for identification and login.
- email: A unique string representing the user's email address, used for communication and login.
- password_hash: A string storing the hashed version of the user's password for secure authentication.

Methods:
- create_user: A method to handle the logic for creating a new user in the system.
- get_user_by_id: A method to retrieve a user's information based on their unique ID.

The User model ensures that each user has a unique username and email, and it securely stores passwords using hashing techniques. This model is designed to integrate with the authentication system, supporting user registration, login, and profile management.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import session
from app.models import Base
from werkzeug.security import generate_password_hash, check_password_hash

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True)
    email = Column(String(150), unique=True)
    password_hash = Column(String(128))
    oauth_provider = Column(String(50))  # e.g., 'google', 'facebook'
    oauth_id = Column(String(150))       # Unique ID from OAuth provider

    def __init__(self, username=None, email=None, password=None, oauth_provider=None, oauth_id=None):
        if password:
            self.password_hash = generate_password_hash(password)
        self.username = username
        self.email = email
        self.oauth_provider = oauth_provider
        self.oauth_id = oauth_id

    def set_password(self, password):
        """Set the password for a user with a hashed version."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    @classmethod
    def create_user(cls, username=None, email=None, password=None, oauth_provider=None, oauth_id=None):
        """
        Create a new user with the given username, email, and password or OAuth details.
        
        Returns:
            User: The newly created user instance.
        Raises:
            ValueError: If the username or email already exists.
        """
        if session.query(cls).filter_by(username=username).first():
            raise ValueError(f"Username '{username}' is already taken.")
        if session.query(cls).filter_by(email=email).first():
            raise ValueError(f"Email '{email}' is already registered.")

        new_user = cls(username, email, password, oauth_provider, oauth_id)
        session.add(new_user)
        session.commit()
        return new_user

    @classmethod
    def get_user_by_id(cls, user_id):
        """
        Retrieve a user by their unique ID.
        
        Args:
            user_id (int): The ID of the user to retrieve.
        
        Returns:
            User: The user instance if found, otherwise None.
        """
        return session.query(cls).get(user_id)

    @classmethod
    def get_user_by_oauth(cls, provider, oauth_id):
        """
        Retrieve a user by OAuth provider and OAuth ID.
        
        Args:
            provider (str): The OAuth provider name (e.g., 'google', 'facebook').
            oauth_id (str): The unique ID from the OAuth provider.
        
        Returns:
            User: The user instance if found, otherwise None.
        """
        return session.query(cls).filter_by(oauth_provider=provider, oauth_id=oauth_id).first()

    def __repr__(self):
        return f"<User {self.username}>"
