from urllib.parse import urlparse
import re
from app.models.poll import Poll
from app.models.media import Media
from app import db
from flask import abort

class PollService:
    """Service class for handling poll-related operations"""
    
    def create_new_poll(
        self,
        question: str,
        option_one: dict,
        option_two: dict,
        user_id: int
    ) -> Poll:
        """
        Create a new poll with two voting options that can be text, image, video or audio
        
        Args:
            question: The poll question text
            option_one: Dictionary containing first voting option details with keys:
                       - media_type: Type of media ('text', 'image', 'video', 'audio')
                       - media_url: URL or content for the media
                       - description: Optional description of the option
            option_two: Dictionary containing second voting option details with same keys
            user_id: ID of the user creating the poll
            
        Returns:
            Poll: The created poll object
            
        Raises:
            HTTPException: If poll creation fails
        """
        try:
            # Validate option dictionaries and media
            for option in [option_one, option_two]:
                if not isinstance(option, dict):
                    raise ValueError("Options must be dictionaries")
                if 'media_type' not in option or 'media_url' not in option:
                    raise ValueError("Options must contain media_type and media_url")
                if option['media_type'] not in ['text', 'image', 'video', 'audio']:
                    raise ValueError("Invalid media_type. Must be 'text', 'image', 'video', or 'audio'")
                
                # Validate media URL
                parsed_url = urlparse(option['media_url'])
                if not all([parsed_url.scheme, parsed_url.netloc]):
                    raise ValueError(f"Invalid media URL: {option['media_url']}")
                
                # Validate media type matches URL
                if option['media_type'] == 'image':
                    if not re.match(r'.*\.(jpg|jpeg|png|gif|webp)$', parsed_url.path.lower()):
                        raise ValueError("Image URL must end with .jpg, .jpeg, .png, .gif or .webp")
                elif option['media_type'] == 'video':
                    if not re.match(r'.*\.(mp4|mov|avi|webm)$', parsed_url.path.lower()):
                        raise ValueError("Video URL must end with .mp4, .mov, .avi or .webm")
                elif option['media_type'] == 'audio':
                    if not re.match(r'.*\.(mp3|wav|ogg)$', parsed_url.path.lower()):
                        raise ValueError("Audio URL must end with .mp3, .wav or .ogg")
            
            # Create media records if needed
            voting_options = []
            for i, option in enumerate([option_one, option_two]):
                media = None
                
                # if option['media_type'] != 'text':
                #     media = Media(
                #         media_type=option['media_type'],
                #         file_path=option['media_url'],
                #         poll_id=None  # Will be set after poll creation
                #     )
                #     db.session.add(media)
                #     db.session.flush()

                voting_options.append({
                    'media_type': option['media_type'],
                    'media_url': option['media_url'],
                    'description': option.get('description', f'Option {i+1}'),
                    'media_id': media.id if media else None
                })
            
            return Poll.create_poll(
                question=question,
                voting_options=voting_options,
                user_id=user_id
            )
            
        except ValueError as e:
            abort(400, description=str(e))
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Failed to create poll: {str(e)}")

    def get_poll_details(self, poll_id: int) -> dict:
        """
        Get details of a specific poll including voting options
        
        Args:
            poll_id: ID of the poll to retrieve
            
        Returns:
            dict: Poll details with options
            
        Raises:
            HTTPException: If poll is not found
        """
        try:
            poll = Poll.get_poll_by_id(poll_id)
            if not poll:
                abort(404, description="Poll not found")
                
            return {
                "id": poll.id,
                "question": poll.question,
                "created_at": poll.created_at.isoformat(),
                "is_active": poll.is_active,
                "options": [
                    {
                        "id": opt.id,
                        "media_type": opt.media_type,
                        "media_url": opt.media_url,
                        "description": opt.description
                    }
                    for opt in poll.voting_options
                ]
            }
            
        except Exception as e:
            return None

    def record_vote(self, poll_id: int, option_id: int, user_id: int) -> bool:
        """
        Record a user's vote on a poll
        
        Args:
            poll_id: ID of the poll being voted on
            option_id: ID of the option being voted for
            user_id: ID of the user voting
            
        Returns:
            bool: True if vote was successfully recorded
            
        Raises:
            HTTPException: If voting fails
        """
        poll: Poll|None = Poll.get_poll_by_id(poll_id)
        if not poll:
            abort(404, description="Poll not found")
        
        if not poll.is_active:
            abort(400, description="Poll is no longer active")
        
        if poll.has_user_voted(user_id):
            abort(400, description="User has already voted on this poll")
        
        if not poll.is_valid_option(option_id):
            abort(400, description="Invalid voting option")

        try:                
            poll.record_vote(user_id, option_id)
            db.session.commit()
            return True            

        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Failed to record vote: {str(e)}")
    
    def close_poll(self, poll_id: int, user_id: int) -> bool:
        """
        Close a poll, only the poll owner can perform this action
        
        Args:
            poll_id: ID of the poll to close
            user_id: ID of the user attempting to close the poll
            
        Returns:
            bool: True if poll was successfully closed
            
        Raises:
            HTTPException: If closing fails or user is not the owner
        """
        try:
            poll = Poll.get_poll_by_id(poll_id)
            if not poll:
                abort(404, description="Poll not found")
            
            if poll.user_id != user_id:
                abort(403, description="Only the poll owner can close the poll")
            
            poll.is_active = False
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Failed to close poll: {str(e)}")
