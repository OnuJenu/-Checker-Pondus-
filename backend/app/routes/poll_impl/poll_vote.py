from sqlite3 import IntegrityError
from flask import current_app, jsonify
import werkzeug

from app.utils.security import get_current_user, handle_auth_errors
from app import db

@handle_auth_errors
def poll_vote_impl(poll_id, request):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request must be JSON"}), 400
        
        if 'option_id' not in data:
            return jsonify({"error": "Missing option_id"}), 400
        
        user = get_current_user()

        # Vote using service layer
        vote_result = current_app.poll_service.record_vote(
            poll_id=poll_id,
            option_id=data['option_id'],
            user_id=user.id
        )

        return jsonify({
            "result": vote_result,
            "poll_id": poll_id,
            "option_id": data['option_id']
        }), 201
    
    except werkzeug.exceptions.HTTPException as e:
        return jsonify({"error": e.description}), e.code
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 500
    except Exception as e:
        current_app.logger.error(f"Error voting on poll: {str(e)}")
        return jsonify({"error": "Failed to vote on poll"}), 500