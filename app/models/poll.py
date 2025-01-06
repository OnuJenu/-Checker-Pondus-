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

from app import db
from datetime import datetime

from app.models.voting_option import VotingOption

class Poll(db.Model):
    __tablename__ = 'polls'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Establish relationship to VotingOption
    voting_options = db.relationship('VotingOption', back_populates='poll', cascade="all, delete-orphan")
    user = db.relationship('User', backref=db.backref('polls', lazy=True))

    def __init__(self, question, user_id):
        self.question = question
        self.user_id = user_id

    @classmethod
    def create_poll(cls, question, voting_options, user_id):
        if len(voting_options) != 2:
            raise ValueError("Exactly two voting options are required.")
        
        new_poll = cls(question=question, user_id=user_id)
        db.session.add(new_poll)
        db.session.flush()  # To get the poll ID before adding voting options

        # Add voting options to this poll
        for option_data in voting_options:
            option = VotingOption(
                media_type=option_data['media_type'],
                media_url=option_data['media_url'],
                description=option_data.get('description'),
                poll_id=new_poll.id
            )
            db.session.add(option)

        db.session.commit()
        return new_poll

    @classmethod
    def get_poll_by_id(cls, poll_id):
        return cls.query.get(poll_id)

    def update_poll(self, question=None, voting_options=None):
        if question:
            self.question = question
        if voting_options and len(voting_options) == 2:
            for i, option_data in enumerate(voting_options):
                option = self.voting_options[i]
                option.media_type = option_data['media_type']
                option.media_url = option_data['media_url']
                option.description = option_data.get('description')
        db.session.commit()
