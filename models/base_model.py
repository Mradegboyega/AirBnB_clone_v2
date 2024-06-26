#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from datetime import datetime
from uuid import uuid4

Base = declarative_base()

class BaseModel:
    """A base class for all hbnb models"""
<<<<<<< HEAD
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
=======
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialize BaseModel instance"""
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    if isinstance(value, str):
                        setattr(self, key, datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f'))
                    else:
                        setattr(self, key, value)
                elif key != '__class__':
                    setattr(self, key, value)
        self.id = str(uuid4())  # Always generate a new UUID
        self.created_at = self.updated_at = datetime.now()
>>>>>>> 53ba316e0683fb474eb57d54522d28560a47b42b


    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = dict(self.__dict__)
        dictionary['__class__'] = type(self).__name__
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        """Deletes the current instance from the storage"""
        from models import storage
        storage.delete(self)
