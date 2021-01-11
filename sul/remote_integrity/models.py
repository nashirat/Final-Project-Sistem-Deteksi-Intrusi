#!/usr/bin/env python

import os
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE_PATH = os.path.join(os.getcwd(), 'integrity.db')

engine = create_engine('sqlite:///' + DATABASE_PATH)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Model(object):

    def to_anonymous_object(self):
     
        return type('', (object,), self.to_dict())()

    def to_dict(self):
       
        return dict(((key, getattr(self, key)) for key in self.__mapper__.columns.keys()))

    def values(self):
       
        return list(((getattr(self, key)) for key in self.keys()))

    @classmethod
    def keys(cls):
    
        return cls.__mapper__.columns.keys()

    def delete(self):
     
        session.delete(self)

    def __iter__(self):
        values = vars(self)
        for attr in self.__mapper__.columns.keys():
            if attr in values:
                yield [attr, values[attr]]

    @classmethod
    def as_list(cls):
    
        return list(cls)

    @classmethod
    def query(cls):
    
        return session.query(cls)


class Server(Model, Base):
    __tablename__ = "servers"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    @classmethod
    def get(cls, name):
       
        return session.query(cls).filter(cls.name == name).one_or_none()

    @classmethod
    def exists(cls, name):
        
        return cls.get(name=name) is not None

    @classmethod
    def create(cls, name):
       
        server = cls(name=name)
        session.add(server)
        return server

    def get_related_checksum(self, path, checksum):
        
        for row in self.checksums:
            if row.path == path and row.checksum == checksum:
                return row


class Checksum(Model, Base):
    __tablename__ = "checksums"
    id = Column(Integer, primary_key=True)
    path = Column(String, nullable=False)
    checksum = Column(String(128), nullable=False)

    server = relationship(Server, backref="checksums")
    server_id = Column(Integer, ForeignKey("servers.id"), index=True, nullable=False)

    @classmethod
    def create(cls, path, checksum, server):
  
        record = cls(path=path, checksum=checksum, server=server)
        session.add(record)
        return record


class Event(Model, Base):
    FILE_ADDED = 1
    FILE_REMOVED = 2
    FILE_MODIFIED = 3

    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    event = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    checksum = relationship(Checksum)
    checksum_id = Column(Integer, ForeignKey("checksums.id"), index=True, nullable=False)

    @classmethod
    def create(cls, event, description, checksum):

        record = cls(event=event, description=description, checksum=checksum, timestamp=datetime.now())
        session.add(record)
        return record


def create_database():

    Base.metadata.create_all(engine)


def database_exists():

    return os.path.exists(DATABASE_PATH)
