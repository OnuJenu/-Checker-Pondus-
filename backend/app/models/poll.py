"""
Poll Model

This model represents the polls within the mobile voting platform. It handles the creation and management of polls, which consist of a question and two voting options. The Poll model is essential for facilitating user interactions and voting processes, including:

Attributes:
- id: A unique identifier for each poll, serving as the primary key.
- question: A string representing the poll's question, which users will vote on.
- options: A relationship to the VotingOption model, representing the two voting options for the poll.
- is_active: A boolean indicating whether the poll is currently active and open for voting.
- created_at: A timestamp indicating when the poll was created.
- user_id: The ID of the user who created the poll, linking it to the User model.
Methods:
- create_poll: A method to handle the logic for creating a new poll in the system.
- get_poll_by_id: A method to retrieve a poll's information based on its unique ID.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.models import Base
from app.databases.database import db
from app.models.vote import Vote
from app.models.voting_option import VotingOption

class Poll(Base):
    __tablename__ = 'polls'
    id = Column(Integer, primary_key=True)
    question = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Establish relationship to VotingOption
    voting_options = relationship('VotingOption', back_populates='poll', cascade="all, delete-orphan")
    user = relationship('User', backref=backref('polls', lazy=True))

    def __init__(self, question, user_id):
        self.question = question
        self.user_id = user_id

    def to_dict(self):
        return {
            "id": self.id,
            "question": self.question,
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active,
            "options": [
                {
                    "id": opt.id,
                    "media_type": opt.media_type,
                    "media_url": opt.media_url,
                    "description": opt.description
                }
                for opt in self.voting_options
            ]
        }

    @classmethod
    def create_poll(cls, question, voting_options, user_id):        
        new_poll = cls(question=question, user_id=user_id)
        db.add(new_poll)
        db.flush()  # To get the poll ID before adding voting options

        # Add voting options to this poll
        for option_data in voting_options:
            option = VotingOption(
                media_type=option_data['media_type'],
                media_url=option_data['media_url'],
                description=option_data.get('description'),
                poll_id=new_poll.id
            )
            db.add(option)

        db.commit()
        return new_poll

    @classmethod
    def get_poll_by_id(cls, poll_id):
        return db.query(cls).get(poll_id)

    def update_poll(self, question=None, voting_options=None):
        if question:
            self.question = question
        if voting_options and len(voting_options) == 2:
            for i, option_data in enumerate(voting_options):
                option = self.voting_options[i]
                option.media_type = option_data['media_type']
                option.media_url = option_data['media_url']
                option.description = option_data.get('description')
        db.commit()

    def get_votes_for_option(self, option_id):
        """Check if a specific user has voted on this poll"""
        # Assuming there's a Vote model with poll_id and user_id
        return db.query(Vote).filter_by(poll_id=self.id, option_id=option_id).all()

    def has_user_voted(self, user_id):
        """Check if a specific user has voted on this poll"""
        # Assuming there's a Vote model with poll_id and user_id
        return db.query(Vote).filter_by(poll_id=self.id, user_id=user_id).first() is not None

    def is_valid_option(self, option_id):
        """Validate if a given option is valid for this poll"""
        # Check if the option_id exists in this poll's voting options
        return db.query(VotingOption).filter_by(poll_id=self.id, id=option_id).first() is not None

    def record_vote(self, user_id, option_id):
        """Record a vote for a user on a specific option"""
        if not self.is_active:
            raise ValueError("Poll is not active")
        if not self.is_valid_option(option_id):
            raise ValueError("Invalid voting option")
        if self.has_user_voted(user_id):
            raise ValueError("User has already voted")
        # Create and record the vote
    
        vote = Vote(poll_id=self.id, user_id=user_id, option_id=option_id)
        db.add(vote)
        db.commit()
