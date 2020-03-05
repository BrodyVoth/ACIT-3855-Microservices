from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class DayStats(Base):
    """ Day Stats """

    __tablename__ = "day"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(250), nullable=False)
    mood = Column(String(250), nullable=False)
    notes = Column(String(250), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, user_id, mood, notes):
        """ Initializes a sleep stats reading """
        self.user_id = user_id
        self.mood = mood
        self.notes = notes
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a sleep stats reading """
        dict = {}
        dict['id'] = self.id
        dict['user_id'] = self.user_id
        dict['mood'] = self.mood
        dict['notes'] = self.notes

        return dict
