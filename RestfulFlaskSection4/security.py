from user import User

users = [
    User(1,'anand','asdf')
]

username_mapping = {u.username:u for u in users}

userid_mapping = { u.id:u for u in users}


def authenticate(username, password):
    print(username)
    print(password)
    print(username_mapping)
    user = username_mapping.get(username, None)  # similar to userid_mapping[username]
    print(user)
    if user is not None and password == user.password:
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id,None)
