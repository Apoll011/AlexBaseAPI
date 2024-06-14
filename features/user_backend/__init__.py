import sys
import os
import io
import json
import typing
import socket
from os import makedirs

class SearchUsers:
    """Let You serche trought a list of users"""
    def __init__(self, users):
        self.users = users
    def by_name(self, query):
        result = []
        for user in self.users:
            if query in user["name"]:
                result.append(user["id"])
        return result if(len(result) > 0) else None
    def by_tags(self, query, value = ">:0", exclue = []):
        result = []
        v = value.split(":")
        v[1] = int(v[1])
        for user in self.users:
            if user["id"] in exclue:
                continue
            else:
                for t in user["tags"]:
                    quer = query if  type(query) == list else [query]
                    t[1] = int(t[1])
                    for que in quer:
                        if que.lower() == t[0].lower():
                            if v[0] == ">":
                                if t[1] > v[1]:
                                    result.append(user["id"])
                            elif v[0] == "<":
                                if t[1] < v[1]:
                                    result.append(user["id"])
                            elif v[0] == ">=" or v[0] == "=>":
                                if t[1] >= v[1]:
                                    result.append(user["id"])
                            elif v[0] == "<=":
                                if t[1] <= v[1]:
                                    result.append(user["id"])
                            elif v[0] == "!=":
                                if t[1] != v[1]:
                                    result.append(user["id"])
                            elif v[0] == "=":
                                if t[1] == v[1]:
                                    result.append(user["id"])
        return result if(len(result) > 0) else None

def user_id(user_id):
    uid = ""
    if int(user_id) < 10:
        uid = "000000000"+user_id
    elif int(user_id) >= 10 and int(user_id) < 100:
        uid = "00000000"+user_id
    elif int(user_id) >= 100 and int(user_id) < 1000:
        uid = "0000000"+user_id
    elif int(user_id) >= 1000 and int(user_id) < 10000:
        uid = "000000"+user_id
    elif int(user_id) >= 10000 and int(user_id) < 100000:
        uid = "00000"+user_id
    elif int(user_id) >= 100000 and int(user_id) < 1000000:
        uid = "0000"+user_id
    elif int(user_id) >= 1000000 and int(user_id) < 10000000:
        uid = "000"+user_id
    elif int(user_id) >= 10000000 and int(user_id) < 100000000:
        uid = "00"+user_id
    elif int(user_id) >= 100000000 and int(user_id) < 1000000000:
        uid = "0"+user_id
    elif int(user_id) >= 1000000000 and int(user_id) < 10000000000:
        uid = ""+user_id
    else:
        uid = user_id
    return uid

class GetUsers:
    def __init__(self, users):
        self.users = users
    def by_id(self, idd):
        #print(self.users)
        if idd != None:
            i = idd
            uu = []
            for u in self.users:
                if type(i) != list:
                    #print(u)
                    if u["id"] == i:
                        return u
                else:
                    for ii in i:
                        if u["id"] == ii:
                            uu.append(u)
            return uu
        else:
            return None

class CreateUsers:
    def __init__(self, user_data):
        try:
            a = "a"
            users_lengths = len(os.listdir("./users"))
            userid = str(users_lengths+1)
            user = user_data
            user["id"] = user_id(userid)
            with open("./users/"+user["id"]+".user", a) as ui:
                json.dump(user, ui)
            return 1
        except:
            return 0
