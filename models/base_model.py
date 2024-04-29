#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime


class BaseModel:
    """A base class for all hbnb models"""
    def __init__(self, *args, **kwargs):
        """Instantiate a new model"""
        from models import storage
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        storage.new(self)
        
        if kwargs:
            if 'created_at' in kwargs:
                created_at_arg = kwargs.pop('created_at')
                if isinstance(created_at_arg, str):
                    self.created_at = datetime.strptime(created_at_arg, '%Y-%m-%dT%H:%M:%S.%f')
                else:
                    self.created_at = created_at_arg
            if 'updated_at' in kwargs:
                updated_at_arg = kwargs.pop('updated_at')
                if isinstance(updated_at_arg, str):
                    self.updated_at = datetime.strptime(updated_at_arg, '%Y-%m-%dT%H:%M:%S.%f')
                else:
                    self.updated_at = updated_at_arg
            if '__class__' in kwargs:
                del kwargs['__class__']
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary
