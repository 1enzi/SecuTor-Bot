from pymongo import MongoClient


class User:
    def __init__(self, new_first_name, new_last_name):
        self.first_name = new_first_name
        self.last_name = new_last_name
        self.is_register = False

    @property
    def get_first_name(self):
        return self.first_name

    @property
    def get_last_name(self):
        return self.last_name

    def register_user(self):
        self.is_register = True


class DataBase:
    def __init__(self):
        cluster = MongoClient(strings.clusterURL)

        self.users = cluster["SecuTor"]
        self.collection = self.users["SecuTor"]

        self.User_Count = len(list(self.users.find({})))

    def get_user(self, chat_id):
        user = self.users.find_one({"chat_id": chat_id})

        if user is not None:
            return user

        user = {
            "chat_id": chat_id,
            "task_index": None
        }

        self.users.insert_one(user)

        return user
