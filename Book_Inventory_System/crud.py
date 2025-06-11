from sqlalchemy.orm import Session
import models,schemas
def get_all_books(db:Session):
    return db.query(models.Book).all()
def get_book_by_id(db:Session,book_id:int):
    return db.query(models.Book).filter(models.Book.id==book_id).first()
def search_books(db:Session,title:str=None,author:str=None):
    query=db.query(models.Book)
    if title:
        query=query.filter(models.Book.title.ilike(f"%{title}%"))
    if author:
        query=query.filter(models.Book.author.ilike(f"%{author}%"))
    return query.all()

def create_book(db:Session,book:schemas.BookCreate):
    new_book=models.Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def update_book(db:Session,book_id:int,book:schemas.BookUpdate):
    db_book=get_book_by_id(db,book_id)
    if db_book:
        db_book.price=book.price
        db_book.stock=book.stock
        db.commit()
        db.refresh(db_book)
    return db_book
    
def delete_book(db:Session,book_id:int):
    db_book=get_book_by_id(db,book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book

def create_publisher(db:Session,publisher:schemas.PublisherCreate):
    db_publisher=models.Publisher(**publisher.dict())
    db.add(db_publisher)
    db.commit()
    db.refresh(db_publisher)
    return db_publisher

def get_all_publishers(db:Session):
    return db.query(models.Publisher).all()
def get_publisher_by_id(db:Session,publisher_id:int):
    return db.query(models.Publisher).filter(models.Publisher.id==publisher_id).first()