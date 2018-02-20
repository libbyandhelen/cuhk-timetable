from base.error import Error
from base.response import Ret
from base.session import load_session, save_session


def get_user_from_session(request):
    from User.models import User
    """get user from session if login"""
    user_id = load_session(request, 'user', once_delete=False)
    if user_id is None:
        return Ret(Error.REQUIRE_LOGIN)
    return User.get_user_by_id(user_id)


def save_user_to_session(request, user):
    """save user to session when login"""
    try:
        request.session.cycle_key()
    except NotImplementedError as err:
        print(str(err))
    save_session(request, 'user', user.pk)
    return None


def logout_user_from_session(request):
    """logout user from session"""
    load_session(request, 'user', once_delete=True)
