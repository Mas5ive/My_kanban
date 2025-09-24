from flask import Blueprint, render_template
from flask_jwt_extended import get_jwt_identity, jwt_required

bp = Blueprint('profile', __name__)


@bp.route('/profile')
@jwt_required()
def show():
    username = get_jwt_identity()
    return render_template(
        'profile.html',
        username=username,
    )
