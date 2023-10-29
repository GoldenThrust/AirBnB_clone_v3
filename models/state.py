#!/usr/bin/python3
""" State Module for HBNB project """
import models
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship("City", cascade='all, delete, delete-orphan',
                              backref="state")
    else:
        @property
        def cities(self):
            """returns the list of Cities instances with state_id
            equals to the current State.id """
            model = models.storage.all()
            city = []
            ref = []

            for mode in model:
                cls = mode.split(".")

                if (cls[0] == 'City'):
                    city.append(model[mode])

            for cit in city:
                if cit.state_id == self.id:
                    ref.append(cit)

            return(ref)
