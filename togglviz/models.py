from sqlalchemy import create_engine
from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    ForeignKey,
    DateTime,
    Enum,
    )

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    )


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import UniqueConstraint

DBSession = scoped_session(sessionmaker())
Base = declarative_base()


class Client(Base):
    __tablename__ = 'client'

    id = Column(Integer(2), primary_key=True, autoincrement=True)
    client_billable = Column(Enum('y', 'n'))
    client_name = Column(Unicode(length=10))


class ClientProject(Base):
    __tablename__ = 'client_project'

    id = Column(Integer(3), primary_key=True, autoincrement=True)
    client_id = Column(Integer(2),
            ForeignKey('client.id')
            )
    project = Column(Unicode(length=50))
    client = relationship('Client')
    UniqueConstraint('client_id', 'project', name="client_proj")


class Description(Base):
    __tablename__ = 'description'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    description = Column(Unicode(length=100))


class TimeSlice(Base):
    __tablename__ = 'cas'

    id = Column(Integer(10), primary_key=True, unique=True, autoincrement=True)
    kje = Column(Enum('d', 's'))
    client_proj = Column(Integer(3),
            ForeignKey('client_project.id')
            )
    datum = Column(DateTime)
    fk_description = Column(Integer(3),
            ForeignKey('description.id')
            )
    description = relationship('Description')
    client_project = relationship('ClientProject')

if __name__ == "__main__":
    from connectSettings import connectString
    engine = create_engine(connectString,  echo=True)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
