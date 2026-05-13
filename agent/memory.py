class UserMemory:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.preferences = {}

    def update(self, key, value):
        self.preferences[key] = value

    def get(self, key, default=None):
        return self.preferences.get(key, default)