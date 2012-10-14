from sqlalchemy import create_engine
from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    ForeignKey,
    DateTime,
    Time,
    Enum,
    )

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    )


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import UniqueConstraint

import re

regex_description = re.compile("^\[([DdSs])\]")

DBSession = scoped_session(sessionmaker())
Base = declarative_base()


class Client(Base):
    __tablename__ = 'client'

    id = Column(Integer(2), primary_key=True, autoincrement=True)
    client_billable = Column(Enum('y', 'n'))
    client_name = Column(Unicode(length=10), unique=True)

    def __init__(self, client_name, client_billable):
        self.client_name = client_name
        self.client_billable = client_billable[0].lower()

    @staticmethod
    def get_client_id(client_name, client_billable):
        """Gets id for client. If client doesn't exist yet it inserts it

        client_billable is Yes or No
        """
        client = DBSession.query(Client) \
        .filter(Client.client_name == client_name) \
        .first()
        if client is None:
            client = Client(client_name, client_billable)
            DBSession.add(client)
            DBSession.flush()
        return client.id


class ClientProject(Base):
    __tablename__ = 'client_project'
    __table_args__ = (
        UniqueConstraint('client_id', 'project', name="client_proj"),
    )

    id = Column(Integer(3), primary_key=True, autoincrement=True)
    client_id = Column(Integer(2),
            ForeignKey('client.id')
            )
    project = Column(Unicode(length=50))
    client = relationship('Client')

    def __init__(self, client_id, project):
        self.client_id = client_id
        self.project = project

    @staticmethod
    def get_client_project_id(client_name, client_billable, project):
        """Gets id for client with project. If it doesn't exist yet it inserts it

        client_billable is Yes or No"""
        client_id = Client.get_client_id(client_name, client_billable)
        client_project = DBSession.query(ClientProject) \
                .filter(ClientProject.client_id == client_id) \
                .filter(ClientProject.project == project) \
                .first()
        if client_project is None:
            client_project = ClientProject(client_id, project)
            DBSession.add(client_project)
            DBSession.flush()
        return client_project.id


class Description(Base):
    __tablename__ = 'description'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    description = Column(Unicode(length=100))

    def __init__(self, description):
        self.description = description

    @staticmethod
    def clean_description(description):
        r = regex_description.match(description)
        kje = None
        if r:
            kje = r.groups()[0].lower()
            description = description[3:]
        return kje, description

    @staticmethod
    def get_description_id(description_text):
        description = DBSession.query(Description) \
                .filter(Description.description == description_text) \
                .first()
        if description is None:
            description = Description(description_text)
            DBSession.add(description)
            DBSession.flush()
        return description.id


class TimeSlice(Base):
    __tablename__ = 'cas'
    __table_args__ = (
        UniqueConstraint('client_proj', 'fk_description', 'datum', name="client_proj_uniq"),
        )


    id = Column(Integer(10), primary_key=True, unique=True, autoincrement=True)
    kje = Column(Enum('d', 's'))
    client_proj = Column(Integer(3),
            ForeignKey('client_project.id')
            )
    datum = Column(DateTime)
    duration = Column(Time)
    fk_description = Column(Integer(3),
            ForeignKey('description.id')
            )
    description = relationship('Description')
    client_project = relationship('ClientProject')

    def __init__(self, client_name, client_billable, project, description, \
            date, duration):
        self.client_proj = ClientProject.get_client_project_id(client_name, \
                client_billable, project)
        self.kje, description = Description.clean_description(description)
        self.fk_description = Description.get_description_id(description)
        self.datum = date
        self.duration = duration

if __name__ == "__main__":
    from connectSettings import connectString
    engine = create_engine(connectString,  echo=True)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
