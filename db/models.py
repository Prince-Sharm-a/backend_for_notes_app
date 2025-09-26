from sqlalchemy import Column, Integer, Date, Float, String, func, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

from db.db import Base 

class Notes(Base):
    __tablename__="notes"
    
    id=Column(Integer,primary_key=True)
    title=Column(String,nullable=False)
    note=Column(String)
    important=Column(Boolean,nullable=False,default=False)
    archive=Column(Boolean,nullable=False,default=False)
    
## Postgresql autoincreament query after creating table
## create sequence demo_id_seq start 1;
## alter table demo alter column id set default nextval('demo_id_seq');
## alter sequence demo_id_seq owned by demo.id;