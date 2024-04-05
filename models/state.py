#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from datetime import datetime

class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all, delete-orphan", backref="state")

    def __init__(self, *args, **kwargs):
        """ Initializes State """
        if 'created_at' in kwargs and isinstance(kwargs['created_at'], datetime):
            kwargs['created_at'] = kwargs['created_at'].strftime('%Y-%m-%dT%H:%M:%S.%f')
        if 'updated_at' in kwargs and isinstance(kwargs['updated_at'], datetime):
            kwargs['updated_at'] = kwargs['updated_at'].strftime('%Y-%m-%dT%H:%M:%S.%f')
        super().__init__(*args, **kwargs)


