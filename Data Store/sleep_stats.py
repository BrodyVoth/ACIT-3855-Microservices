from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class SleepStats(Base):
    """ Sleep Stats """

    __tablename__ = "sleep"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(250), nullable=False)
    sleep_start_time = Column(String(250), nullable=False)
    sleep_end_time = Column(String(250), nullable=False)
    feeling = Column(String(250), nullable=False)
    notes = Column(String(250), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, user_id, sleep_start_time, sleep_end_time, feeling, notes):
        """ Initializes a sleep stats reading """
        self.user_id = user_id
        self.sleep_start_time = sleep_start_time
        self.sleep_end_time = sleep_end_time
        self.feeling = feeling
        self.notes = notes
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a sleep stats reading """
        dict = {}
        dict['id'] = self.id
        dict['user_id'] = self.user_id
        dict['sleep_start_time'] = self.sleep_start_time
        dict['sleep_end_time'] = self.sleep_end_time
        dict['feeling'] = self.feeling
        dict['notes'] = self.notes

        return dict
