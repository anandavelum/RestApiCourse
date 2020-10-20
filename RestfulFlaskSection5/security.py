from user import User


def authenticate(username, password):
    print(username)
    user = User.find_by_username(username)
    print(user.name)
    print(user.password)
    if user is not None and password == user.password:
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)
