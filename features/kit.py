from features.user_backend import SearchUsers, CreateUsers, GetUsers
import json
import os

class UserKit:
    users = []
    def __init__(self) -> None:
        for user in os.listdir("./features/user_backend/users"):
            us = open("./features/user_backend/users/"+user, "r")
            self.users.append(json.load(us))
        
        self.searchUser = SearchUsers(self.users)
        self.getUser = GetUsers(self.users)
        self.createUser = CreateUsers
  