from flask import request, jsonify, current_app, Blueprint
from app.models.poll import Poll
from app.models.voting_option import VotingOption
from app.models.vote import Vote
from app.utils.security import get_current_user
from sqlalchemy.exc import IntegrityError
from app import db

poll_blueprint = Blueprint('poll', __name__)

# Handles the creation of a new poll.
# Validates and saves media if provided.
# Ensures that each poll has exactly two options.
@poll_blueprint.route('/polls', methods=['POST'])
def create_poll():
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

# Retrieves a specific poll by its ID.
# Returns details including the question, media URL, options, and creation date.
# Retrieve specific poll
@poll_blueprint.route('/polls/<int:poll_id>', methods=['GET'])
def get_poll(poll_id):
    try:
        if not poll_id or poll_id < 1:
            return jsonify({"error": "Invalid poll ID"}), 400
            
        poll_details = current_app.poll_service.get_poll_details(poll_id)
        if not poll_details:
            return jsonify({"error": "Poll not found"}), 404
            
        return jsonify({
            "id": poll_details["id"],
            "question": poll_details["question"],
            "options": poll_details["options"],
            "created_at": poll_details["created_at"],
            "is_active": poll_details["is_active"]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting poll {poll_id}: {str(e)}")
        return jsonify({"error": "Failed to retrieve poll details"}), 500

# Allows users to vote on a poll.
# Ensures that the user has not already voted and that the poll is not closed.
# Records the vote in the database.
# Vote on a poll
@poll_blueprint.route('/polls/<int:poll_id>/vote', methods=['POST'])
def vote_on_poll(poll_id):
    data = request.json
    option_id = data.get('option_id')

    if not option_id:
        return jsonify({"error": "Option ID is required"}), 400

    user = get_current_user()
    poll = Poll.query.get_or_404(poll_id)
    option = VotingOption.query.filter_by(id=option_id, poll_id=poll.id).first()

    if not option:
        return jsonify({"error": "Invalid option ID"}), 400

    if poll.closed:
        return jsonify({"error": "Poll is closed for voting"}), 403

    existing_vote = Vote.query.filter_by(user_id=user.id, poll_id=poll.id).first()
    if existing_vote:
        return jsonify({"error": "You have already voted on this poll"}), 403

    vote = Vote(user_id=user.id, option_id=option_id)
    db.session.add(vote)
    db.session.commit()

    return jsonify({"message": "Vote recorded"}), 201

# Retrieves the results of a closed poll.
# Calculates the percentage of votes for each option.
# Returns the results in a user-friendly format.
# Get closed poll results
@poll_blueprint.route('/polls/<int:poll_id>/results', methods=['GET'])
def get_poll_results(poll_id):
    poll = Poll.query.get_or_404(poll_id)

    if not poll.closed:
        return jsonify({"error": "Poll results are not available yet"}), 403

    options = [
        {
            "id": option.id,
            "text": option.description,
            "vote_count": len(option.votes)
        }
        for option in poll.voting_options
    ]

    total_votes = sum([option['vote_count'] for option in options])
    results = [
        {**option, "percentage": (option["vote_count"] / total_votes) * 100 if total_votes > 0 else 0}
        for option in options
    ]

    return jsonify({
        "id": poll.id,
        "question": poll.question,
        "results": results,
        "total_votes": total_votes
    }), 200

# Provides a paginated list of polls.
# Supports filtering by active or closed polls.
# Returns a list of polls with basic details and pagination information.
# Retrieve a paginated list of polls
@poll_blueprint.route('/polls', methods=['GET'])
def get_polls():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('PAGINATION_PER_PAGE', 10)
    filter_type = request.args.get('filter', 'all')

    query = Poll.query
    if filter_type == 'active':
        query = query.filter_by(is_active=True)
    elif filter_type == 'closed':
        query = query.filter_by(is_active=False)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    polls = [poll.to_dict() for poll in pagination.items]

    return jsonify({
        "polls": polls,
        "total_pages": pagination.pages,
        "current_page": page
    }), 200

# Allows the creator of a poll to close it, preventing further voting.
# Ensures that only the creator can close the poll.
# Close a poll
@poll_blueprint.route('/polls/<int:poll_id>/close', methods=['PUT'])
def close_poll(poll_id):
    user = get_current_user()
    poll = Poll.query.get_or_404(poll_id)

    if poll.user_id != user.id:
        return jsonify({"error": "You are not authorized to close this poll"}), 403

    poll.closed = True
    db.session.commit()

    return jsonify({"message": "Poll closed"}), 200
