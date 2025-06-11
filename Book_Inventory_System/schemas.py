from pydantic import BaseModel,Field

class PublisherBase(BaseModel):
    name:str
    country:str
class PublisherCreate(PublisherBase):
    pass 
class Publisher(PublisherBase):
    id:int

    class Config:
        from_attributes=True

class BookBase(BaseModel):
    title:str
    author:str
    price:float=Field(...,ge=0)
    stock:int=Field(...,ge=0)
    publisher_id:int

class BookCreate(BookBase):
    pass 
class BookUpdate(BaseModel):
    price:float=Field(...,ge=0)
    stock:int=Field(...,ge=0)

class Book(BookBase):
    id:int
    publisher:Publisher
    class Config:
        from_attributes=True