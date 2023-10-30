#!/usr/bin/python3
""" Place Module for HBNB project """

import models
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship


metadata = Base.metadata
place_amenity = Table("place_amenity", metadata,
                      Column("place_id", String(60),
                             ForeignKey("places.id"),
                             primary_key=True,
                             nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship('Review',  cascade='all, delete, delete-orphan',
                               backref='place')
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False,
                                 back_populates="place_amenities")
    else:
        @property
        def reviews(self):
            """ getter attribute reviews that returns the list of
            Review instances with place_id equals to the current Place.id """
            model = models.storage.all()
            review = []
            ref = []

            for mode in model:
                cls = mode.split(".")

                if (cls[0] == 'Review'):
                    review.append(models[mode])

            for rev in review:
                if rev.place_id == self.id:
                    ref.append(rev)

            return(ref)

        @property
        def amenities(self):
            """ returns the list of Amenity instances based on the attribute
              amenity_ids that contains all Amenity.id linked to the Place """
            return [a_id for a_id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj=None):
            """ append method for adding an Amenity.id
              to the attribute amenity_ids """
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
