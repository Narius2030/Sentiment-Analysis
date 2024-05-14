class User:
    def __init__(self, username, password=None):
        self._username = username 
        self._password = password 
    
    def get_username(self):
        return self._username
    
    def get_password(self):
        return self._password
