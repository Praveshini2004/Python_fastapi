
from sqlalchemy import Column,Integer,String,Float,ForeignKey
from sqlalchemy.orm import relationship
from database import Base
class Publisher(Base):
    __tablename__="publishers"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,unique=True,index=True)
    country=Column(String)

    books=relationship("Book",back_populates="publisher")

class Book(Base):
    __tablename__="books"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,index=True)
    author=Column(String,index=True)
    price=Column(Float)
    stock=Column(Integer)

    publisher_id=Column(Integer,ForeignKey("publishers.id"))
    publisher=relationship("Publisher",back_populates="books")