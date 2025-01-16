from flask import current_app, jsonify

from app.models.poll import Poll
from app.databases.database import db


def get_polls_impl(request):
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('PAGINATION_PER_PAGE', 10)
    filter_type = request.args.get('filter', 'all')
    order = request.args.get('order', 'desc')

    query = db.query(Poll)
    if order == 'asc':
        query = query.order_by(Poll.created_date.asc())
    else:
        query = query.order_by(Poll.created_date.desc())
    if filter_type == 'active':
        query = query.filter_by(is_active=True)
    elif filter_type == 'closed':
        query = query.filter_by(is_active=False)

    total_count = query.count()
    total_pages = (total_count + per_page - 1) // per_page
    offset = (page - 1) * per_page

    polls = query.limit(per_page).offset(offset).all()
    polls = [poll.to_dict() for poll in polls]

    return jsonify({
        "polls": polls,
        "total_pages": total_pages,
        "current_page": page
    }), 200
