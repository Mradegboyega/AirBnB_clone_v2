#!/usr/bin/python3
"""City Module for HBNB project"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """The City class, which inherits from BaseModel and Base"""

    __tablename__ = 'cities'

    name = Column(String(128), nullable=False)

    # Relationship with Place
    places = relationship("Place", cascade="all, delete", back_populates="city")

    def __init__(self, *args, **kwargs):
        """Initializes City"""
        super().__init__(*args, **kwargs)
