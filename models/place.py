#!/usr/bin/python3
""" Place Module for HBNB project """
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models import storage_type
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from models.review import Review
from sqlalchemy import Table


relationship_table = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False)
                      )


class Place(BaseModel, Base):
    """ A place to stay """

    if storage_type == 'db':
        __tablename__ = 'places'

        city_id = Column(String(60),
                         ForeignKey('cities.id', ondelete='CASCADE'),
                         nullable=False)

        user_id = Column(String(60),
                         ForeignKey('users.id', ondelete='CASCADE'),
                         nullable=False)

        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)

        reviews = relationship('Review', backref='place', cascade='delete')

        amenities = relationship('Amenity', secondary='place_amenity',
                                 back_populates='place_amenities', viewonly=False)

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Returns the list of Review instances with place_id equal to the
            current Place.id.
            -This is the relationship between Place and Review."""

            reviews_objs = models.storage.all(Review).values()
            return [rev for rev in review_objs if rev.place_id == self.id]

        @property
        def amenities(self):
            """Get linked amenities."""

            objs = models.storage.all(Amenity).values()
            return [obj for obj in objs if obj.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, value):
            """Sets linked amenities."""
            if type(value) == Amenity:
                self.amenity_ids.append(value.id)
