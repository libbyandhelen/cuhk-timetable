def save_session(request, key, value):
    """save key-value pair in session"""
    request.session["saved_" + key] = value


def load_session(request, key, once_delete=True):
    """ given key, get value on session
    :param request: HttpRequest
    :param key: session key
    :param once_delete: whether remove this session after use
    :return: session value
    """
    value = request.session.get("saved_" + key)
    if value is None:
        return None
    if once_delete:
        del request.session["saved_" + key]
    return value
