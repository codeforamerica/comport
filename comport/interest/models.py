import datetime as dt
from comport.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)

class Interested(SurrogatePK, Model):
    __tablename__ = 'interesteds'
    name = Column(db.String(255), unique=False, nullable=False)
    agency = Column(db.String(255), unique=False, nullable=False)
    location = Column(db.String(255), unique=False, nullable=False)
    phone = Column(db.String(255), unique=False, nullable=False)
    email = Column(db.String(255), unique=False, nullable=False)
    comments = Column(db.String(255), unique=False, nullable=False)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)
