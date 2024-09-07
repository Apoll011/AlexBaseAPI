import os
import uuid
import json

class SearchUsers:
    """Let You serche trought a list of users"""
    def __init__(self, users):
        self.users = users
    def by_name(self, query):
        result = []
        for user in self.users:
            if query in user["name"]:
                result.append(user["id"])
        return result
    
    def by_tags(self, query, conditon = ">:0", exclude = []):
        result = []
        condition_parsed = {
            "symbol": conditon.split(":")[0],
            "value": int(conditon.split(":")[1])
        }
        for user in self.users:
            if user["id"] in exclude:
                continue
            else:
                for tag in user["tags"]:
                    query_list:list[str] = query if type(query) == list else [query] # type: ignore
                    tag[1] = int(tag[1])
                    for individual_query in query_list:
                        if individual_query.lower() == tag[0].lower():
                            if condition_parsed["symbol"] == ">":
                                if tag[1] > condition_parsed["value"]:
                                    result.append(user["id"])
                            elif condition_parsed["symbol"] == "<":
                                if tag[1] < condition_parsed["value"]:
                                    result.append(user["id"])
                            elif condition_parsed["symbol"] == ">=" or condition_parsed["symbol"] == "=>":
                                if tag[1] >= condition_parsed["value"]:
                                    result.append(user["id"])
                            elif condition_parsed["symbol"] == "<=":
                                if tag[1] <= condition_parsed["value"]:
                                    result.append(user["id"])
                            elif condition_parsed["symbol"] == "!=":
                                if tag[1] != condition_parsed["value"]:
                                    result.append(user["id"])
                            elif condition_parsed["symbol"] == "=":
                                if tag[1] == condition_parsed["value"]:
                                    result.append(user["id"])
        return result

class GetUsers:
    def __init__(self, users):
        self.users = users
    def by_id(self, id):
        #print(self.users)
        if id != None:
            users = []
            for user in self.users:
                if type(id) != list:
                    #print(u)
                    if user["id"] == id:
                        return user
                else:
                    for ii in id:
                        if user["id"] == ii:
                            users.append(user)
            return users
        else:
            return None

class CreateUsers:
    def __init__(self, user_data):
        user = json.loads(user_data.model_dump_json())
        user["id"] = str(uuid.uuid4())
        with open("./features/user_backend/users/"+user["id"]+".user", 'a') as ui:
            json.dump(user, ui)
            


"""
import json
import os
import uuid
from enum import Enum

class RelationshipType(Enum):
    ""Enum for relationship types""
    FRIEND = 1
    FAMILY = 2
    COLLEAGUE = 3
    NEIGHBOR = 4

class TagType(Enum):
    ""Enum for tag types""
    SOFTWARE_ENGINEER = 1
    DATA_SCIENTIST = 2
    PRODUCT_MANAGER = 3
    MARKETING_EXPERT = 4

class Person:
    ""
    Represents a person with attributes like name, age, citizenship, etc.

    Attributes:
        id (str): Unique ID for the person
        name (str): Name of the person
        age (int): Age of the person
        citizenship (str): Citizenship of the person
        body_structure (dict): Body structure of the person (e.g. height, weight)
        face_metadata (dict): Face metadata of the person (e.g. face ID)
        tags (list): List of tags associated with the person
        relationships (list): List of relationships associated with the person
    ""
    def __init__(self, name, age, citizenship, body_structure, face_metadata):
        self.id = str(uuid.uuid4())
        self.name = name
        self.age = age
        self.citizenship = citizenship
        self.body_structure = body_structure
        self.face_metadata = face_metadata
        self.tags = []
        self.relationships = []

class Relationship:
    ""
    Represents a relationship between two people.

    Attributes:
        id (str): Unique ID for the relationship
        person_id (str): ID of the person who initiated the relationship
        related_person_id (str): ID of the person who is related to the initiator
        relationship_type (RelationshipType): Type of relationship (e.g. friend, family, colleague)
    ""
    def __init__(self, person_id, related_person_id, relationship_type):
        self.id = str(uuid.uuid4())
        self.person_id = person_id
        self.related_person_id = related_person_id
        self.relationship_type = relationship_type

class Tag:
    ""
    Represents a tag associated with a person.

    Attributes:
        id (str): Unique ID for the tag
        person_id (str): ID of the person who the tag is associated with
        tag_type (TagType): Type of tag (e.g. software engineer, data scientist)
    ""
    def __init__(self, person_id, tag_type):
        self.id = str(uuid.uuid4())
        self.person_id = person_id
        self.tag_type = tag_type

class Database:
    ""
    Represents a database that stores people, relationships, and tags.

    Attributes:
        filename (str): File name where the data is stored
        people (dict): Dictionary of people, keyed by ID
        relationships (dict): Dictionary of relationships, keyed by ID
        tags (dict): Dictionary of tags, keyed by ID
    ""
    def __init__(self, filename):
        self.filename = filename
        self.people = {}
        self.relationships = {}
        self.tags = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.people = {p['id']: Person(**p) for p in data['people']}
                self.relationships = {r['id']: Relationship(**r) for r in data['relationships']}
                self.tags = {t['id']: Tag(**t) for t in data['tags']}

    def save_data(self):
        data = {
            'people': [p.__dict__ for p in self.people.values()],
            'relationships': [r.__dict__ for r in self.relationships.values()],
            'tags': [t.__dict__ for t in self.tags.values()]
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def add_person(self, person):
        self.people[person.id] = person
        self.save_data()

    def get_person(self, id):
        return self.people.get(id)

    def add_relationship(self, relationship):
        self.relationships[relationship.id] = relationship
        self.save_data()

    def get_relationships(self):
        return list(self.relationships.values())

    def add_tag(self, tag):
        self.tags[tag.id] = tag
        self.save_data()

    def get_tags(self):
        return list(self.tags.values())

    def search_people(self, query):
        # implement search logic here
        pass

class API:
    ""
    Represents an API that interacts with the database.

    Attributes:
        database (Database): The database instance
    ""
    def __init__(self, database):
        self.database = database

    def create_person(self, data):
        person = Person(**data)
        self.database.add_person(person)
        return person

    def get_person(self, id):
        return self.database.get_person(id)

    def create_relationship(self, data):
        relationship = Relationship(**data)
        self.database.add_relationship(relationship)
        return relationship

    def get_relationships(self):
        return self.database.get_relationships()

    def create_tag(self, data):
        tag = Tag(**data)
        self.database.add_tag(tag)
        return tag

    def get_tags(self):
        return self.database.get_tags()

    def search_people(self, query):
        return self.database.search_people(query)

# usage
database = Database('data.json')
api = API(database)

# create some sample data
person1 = api.create_person({"name": "John Doe", "age": 30, "citizenship": "USA", "body_structure": {"height": 180, "weight": 70}, "face_metadata": {"face_id": "123456"}})
person2 = api.create_person({"name": "Jane Doe", "age": 25, "citizenship": "Canada", "body_structure": {"height": 165, "weight": 55}, "face_metadata": {"face_id": "789012"}})

relationship = api.create_relationship({"person_id": person1.id, "related_person_id": person2.id, "relationship_type": RelationshipType.FRIEND})

tag = api.create_tag({"person_id": person1.id, "tag_type": TagType.SOFTWARE_ENGINEER})

# retrieve data
print(api.get_person(person1.id))  # Person(id=..., name=John Doe, age=30)
print(api.get_relationships())  # [Relationship(id=..., person_id=..., related_person_id=..., type=FRIEND)]
print(api.get_tags())  # [Tag(id=..., person_id=..., tag_type=SOFTWARE_ENGINEER)]
"""