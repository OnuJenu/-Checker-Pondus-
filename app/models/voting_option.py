from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base

class VotingOption(Base):
    __tablename__ = 'voting_option'
    id = Column(Integer, primary_key=True)
    poll_id = Column(Integer, ForeignKey('polls.id'), nullable=False)
    media_type = Column(String(50), nullable=False)
    media_url = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    poll = relationship('Poll', back_populates='voting_options')

    def __init__(self, media_type, media_url, description=None, poll_id=None):
        self.media_type = media_type
        self.media_url = media_url
        self.description = description
        self.poll_id = poll_id
