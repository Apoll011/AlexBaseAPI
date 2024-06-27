import json
import os
from .enums import *

class Database:
    """
    Represents a database that stores people, relationships, and tags.

    Attributes:
        filename (str): File name where the data is stored
        people (dict): Dictionary of people, keyed by ID
        relationships (dict): Dictionary of relationships, keyed by ID
        tags (dict): Dictionary of tags, keyed by ID
    """
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
                self.people = {p['id']: Person().load(**p) for p in data['people']}
                self.relationships = {r['id']: Relationship().load(**r) for r in data['relationships']}
                self.tags = {t['id']: Tag().load(**t) for t in data['tags']}

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
    """
    Represents an API that interacts with the database.

    Attributes:
        database (Database): The database instance
    """
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


database = Database('data.json')
api = API(database)


print(api.get_relationships())  # [Relationship(id=..., person_id=..., related_person_id=..., type=FRIEND)]
print(api.get_tags())  # [Tag(id=..., person_id=..., tag_type=SOFTWARE_ENGINEER)]
