from app import login_manager
from app.models import User


@login_manager.request_loader
def load_user_from_request(request):
    auth = request.authorization
    if auth and auth.type == 'basic':
        user = User.query.filter_by(username=auth.username).first()
        if user and user.check_password(auth.password):
            return user

    return None
