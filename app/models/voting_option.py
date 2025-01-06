from app import db

class VotingOption(db.Model):
    __tablename__ = 'voting_option'
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    media_type = db.Column(db.String(50), nullable=False)
    media_url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

    poll = db.relationship('Poll', back_populates='voting_options')

    def __init__(self, media_type, media_url, description=None):
        self.media_type = media_type
        self.media_url = media_url
        self.description = description