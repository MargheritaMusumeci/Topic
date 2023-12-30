from backend.album import Album
from pydantic import BaseModel
import json

class BaseUser(BaseModel):
        username: str
        email: str
        password: str

class User(BaseUser):
    album: Album
    enabled: bool

    def login(self, username: str, password: str):
        if self.username == username and self.password == password:
            self.enabled = True
        return self.enabled
    
    def logout(self):
        self.enabled = False

class Users(BaseModel):
    registered_users: dict

    def register(self, base_user: BaseUser):
        username = base_user.username
        if not self.exist(username):
            self.registered_users[username] = User(
                        username = base_user.username,
                        email = base_user.email,
                        password = base_user.password,
                        album = Album() ,
                        enabled = False)
            return True
        return False

    def register_from_json(self, users: dict):
        for user in users:
            self.registered_users[user] = User(username = users[user]["username"],
                                               email = users[user]["email"],
                                               password = users[user]["password"],
                                               album = Album(pictures = users[user]["album"]["pictures"],
                                                             votes = users[user]["album"]["votes"]),
                                               enabled = False)

    def delete(self, username: str):
        if username in self.registered_users:
            del self.registered_users[username]

    def exist(self, username: str):
        return username in self.registered_users

    def create_user_from_dict(self, user_data: dict) -> User:
        return User(**user_data)

    def save_users_to_json(self):
        with open("users.json", "w") as file:
            json.dump({username: user.dict() for username, user in self.registered_users.items()}, file)
