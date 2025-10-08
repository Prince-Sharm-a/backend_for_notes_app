from sqlalchemy import Column, Integer, Date, Float, String, func, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

from db.db import Base 

class Notes(Base):
    __tablename__="notes"
    
    id=Column(Integer,primary_key=True)
    title=Column(String,nullable=False)
    note=Column(String)
    important=Column(Boolean,default=False)
    archive=Column(Boolean,default=False)
    isdeleted=Column(Boolean,default=False)
    created_by=Column(Integer,ForeignKey("users.id"),nullable=False)
    created_time=Column(Date,server_default=func.now())
    updated_time=Column(DateTime,server_default=func.now())
    
class Users(Base):
    __tablename__="users"
    
    id=Column(Integer,primary_key=True)
    first_name=Column(String)
    last_name=Column(String)
    user_name=Column(String)
    email=Column(String)
    password=Column(String)
## Postgresql autoincreament query after creating table
## create sequence demo_id_seq start 1;
## alter table demo alter column id set default nextval('demo_id_seq');
## alter sequence demo_id_seq owned by demo.id;