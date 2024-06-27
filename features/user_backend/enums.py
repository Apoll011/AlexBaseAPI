import uuid
from enum import Enum


class RelationshipType(int, Enum):
    """Enum for relationship types"""
    FRIEND = 1
    FAMILY = 2
    COLLEAGUE = 3
    NEIGHBOR = 4

class TagType(int, Enum):
    """Enum for tag types"""
    SOFTWARE_ENGINEER = 1
    DATA_SCIENTIST = 2
    PRODUCT_MANAGER = 3
    MARKETING_EXPERT = 4

class Person:
    """
    Represents a person with attributes like name, age, citizenship, etc.
    """
    
    id: str
    """Unique ID for the person"""
    name: str 
    """Name of the person"""
    age: int 
    """Age of the person"""
    citizenship: str 
    """Citizenship of the person"""
    body_structure: dict
    """Body structure of the person (e.g. height, weight)"""
    face_metadata: dict 
    """Face metadata of the person (e.g. face ID)"""
    tags:list 
    """List of tags associated with the person"""
    relationships: list
    """List of relationships associated with the person"""
    
    def __init__(self, name = "", age = 0, citizenship = "", body_structure = dict(), face_metadata = dict()):
        self.id = str(uuid.uuid4())
        self.name = name
        self.age = age
        self.citizenship = citizenship
        self.body_structure = body_structure
        self.face_metadata = face_metadata

    def load(self, id, name, age, citizenship, body_structure, face_metadata, tags = [], relationships = []):
        self.id = id
        self.name = name
        self.age = age
        self.citizenship = citizenship
        self.body_structure = body_structure
        self.face_metadata = face_metadata
        self.tags = tags
        self.relationships = relationships

        return self

class Relationship:
    """
    Represents a relationship between two people.

    """
    
    id: str 
    """Unique ID for the relationship"""
    person_id: str
    """ID of the person who initiated the relationship"""
    related_person_id: str 
    """ID of the person who is related to the initiator"""
    relationship_type: RelationshipType 
    """Type of relationship (e.g. friend, family, colleague)"""

    def __init__(self, person_id = "", related_person_id = "", relationship_type = RelationshipType):
        self.id = str(uuid.uuid4())
        self.person_id = person_id
        self.related_person_id = related_person_id
        self.relationship_type = relationship_type
    
    def load(self, id, person_id, related_person_id, relationship_type):
        self.id = id
        self.person_id = person_id
        self.related_person_id = related_person_id
        self.relationship_type = relationship_type

        return self

class Tag:
    """
    Represents a tag associated with a person.
    """

    id: str 
    """Unique ID for the tag"""
    person_id: str
    """ID of the person who the tag is associated with"""
    tag_type: TagType
    """Type of tag (e.g. software engineer, data scientist)"""
    
    def __init__(self, person_id = "", tag_type = TagType):
        self.id = str(uuid.uuid4())
        self.person_id = person_id
        self.tag_type = tag_type
    
    def load(self, id, person_id, tag_type):
        self.id = id
        self.person_id = person_id
        self.tag_type = tag_type

        return self
