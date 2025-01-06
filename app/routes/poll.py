from app.models.voting_option import VotingOption
from flask import request, jsonify, current_app, Blueprint
from app.models.poll import Poll, VotingOption
from app.utils.security import get_current_user
from sqlalchemy.exc import IntegrityError
from app import db

poll_blueprint = Blueprint('poll', __name__)

# Handles the creation of a new poll.
# Validates and saves media if provided.
# Ensures that each poll has exactly two options.
@poll_blueprint.route('/polls', methods=['POST'])
def create_poll():
    data = request.form
    try:
        question = data['question']
        option1_data = data['option1']
        option2_data = data['option2']

        # Create the poll and options
        user = get_current_user()

        # Creating voting options with media information
        voting_options = [
            {'media_type': option1_data['media_type'], 'media_url': option1_data['media_url'],
             'description': option1_data.get('description')},
            {'media_type': option2_data['media_type'], 'media_url': option2_data['media_url'],
             'description': option2_data.get('description')}
        ]

        poll = Poll.create_poll(question, user.id, voting_options)
        return jsonify({"message": "Poll created", "poll_id": poll.id}), 201

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {e}"}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 500

# Retrieves a specific poll by its ID.
# Returns details including the question, media URL, options, and creation date.
# Retrieve specific poll
@poll_blueprint.route('/polls/<int:poll_id>', methods=['GET'])
def get_poll(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    options = [option.to_dict() for option in poll.options]
    options = [option.to_dict() for option in poll.voting_options]
    return jsonify({
        "id": poll.id,
        "question": poll.question,
        "options": options,
        "created_at": poll.created_at,
        "is_active": poll.is_active,
        "closed": poll.closed
    }), 200

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
        query = query.filter_by(closed=False)
    elif filter_type == 'closed':
        query = query.filter_by(closed=True)

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