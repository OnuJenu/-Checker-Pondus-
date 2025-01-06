"""
Vote Model

This model represents the voting interactions within the mobile voting platform. It manages the recording and retrieval of votes, ensuring that each user can cast a vote on a poll. The Vote model is crucial for maintaining the integrity and accuracy of the voting process, including:

Attributes:
- id: A unique identifier for each vote, serving as the primary key.
- user_id: An integer referencing the user who cast the vote, linked to the User model.
- poll_id: An integer referencing the poll on which the vote was cast, linked to the Poll model.
- selected_option: A string representing the option selected by the user in the poll.

Methods:
- record_vote: A method to handle the logic for recording a new vote in the system.
- get_votes_by_poll: A method to retrieve all votes associated with a specific poll ID.

The Vote model ensures that each vote is associated with a specific user and poll, and it records the user's selected option. This model is designed to integrate with the voting system, supporting the accurate tracking and analysis of voting data.
"""
from app import db

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    selected_option = db.Column(db.String(255), nullable=False)

    def record_vote(self):
        # Logic to record a vote
        pass

    def get_votes_by_poll(self, poll_id):
        # Logic to retrieve votes by poll ID
        pass
