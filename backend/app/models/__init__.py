from sqlalchemy.ext.declarative import declarative_base

# Create the base class for all models
Base = declarative_base()

# Import all models to ensure they are registered with SQLAlchemy
from .poll import Poll
from .voting_option import VotingOption
from .media import Media
from .user import User
from .vote import Vote
