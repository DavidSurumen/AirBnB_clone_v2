#!/usr/bin/python3
""" State Module for HBNB project """
from models.city import City
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer
from models import storage_type


class State(BaseModel, Base):
    """ State class """

    def __init__(self):
        super().__init__()

    if storage_type == 'db':
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship('City', back_populates='state', cascade='delete')

    else:
        name = ""

    if storage_type == 'file':
        @property
        def cities(self):
            cities_list = []
            all_cities = models.storage.all(City).values()
            for city in all_cities:
                if city.state_id == self.id:
                    cities_list.append(city)

            return cities_list
