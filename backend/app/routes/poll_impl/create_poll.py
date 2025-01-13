from sqlite3 import IntegrityError
from flask import current_app, jsonify

from app.utils.security import get_current_user, handle_auth_errors
from app import db

@handle_auth_errors
def create_poll_impl(request):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request must be JSON"}), 400
            
        # Validate required fields
        required_fields = ['question', 'option1', 'option2']
        if not all(field in data for field in required_fields):
            return jsonify({"error": f"Missing required fields: {', '.join(required_fields)}"}), 400
            
        # Validate options structure
        for option in [data['option1'], data['option2']]:
            if not isinstance(option, dict):
                return jsonify({"error": "Options must be objects"}), 400
            if 'media_type' not in option or 'media_url' not in option:
                return jsonify({"error": "Options must contain media_type and media_url"}), 400
            if option['media_type'] not in ['text', 'image', 'video', 'audio']:
                return jsonify({"error": "Invalid media_type. Must be 'text', 'image', 'video', or 'audio'"}), 400
            
        user = get_current_user()
        
        # Create poll using service layer
        poll = current_app.poll_service.create_new_poll(
            question=data['question'],
            option_one=data['option1'],
            option_two=data['option2'],
            user_id=user.id
        )
        return jsonify({"message": "Poll created", "poll_id": poll.id}), 201

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {e}"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 500
    except Exception as e:
        current_app.logger.error(f"Error creating poll: {str(e)}")
        return jsonify({"error": "Failed to create poll"}), 500
