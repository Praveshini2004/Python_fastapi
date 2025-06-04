client.py
import requests

# Base URL of the FastAPI server
Base_url = "http://127.0.0.1:8020"

def create_publisher():
    """Function to create a new publisher."""
    name = input("Enter publisher name: ")
    country = input("Enter publisher country: ")
    response = requests.post(f"{Base_url}/publishers/", json={"name": name, "country": country})
    if response.status_code == 200:
        print("Publisher created successfully!")
        print(response.json())
    else:
        print(f"Failed to create publisher: {response.json()}")

def list_publishers():
    """Function to list all publishers."""
    response = requests.get(f"{Base_url}/publishers/")
    if response.status_code == 200:
        publishers = response.json()
        if publishers:
            print("Publishers:")
            for publisher in publishers:
                print(f"ID: {publisher['id']}, Name: {publisher['name']}, Country: {publisher['country']}")
        else:
            print("No publishers found.")
    else:
        print(f"Failed to fetch publishers: {response.json()}")

def create_book():
    """Function to create a new book."""
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    price = float(input("Enter book price: "))
    stock = int(input("Enter book stock: "))
    publisher_id = int(input("Enter publisher ID: "))
    response = requests.post(f"{Base_url}/books/", json={
        "title": title,
        "author": author,
        "price": price,
        "stock": stock,
        "publisher_id": publisher_id
    })
    if response.status_code == 200:
        print("Book created successfully!")
        print(response.json())
    else:
        print(f"Failed to create book: {response.json()}")

def list_books():
    """Function to list all books."""
    response = requests.get(f"{Base_url}/books/")
    if response.status_code == 200:
        books = response.json()
        if books:
            print("Books:")
            for book in books:
                print(f"ID: {book['id']}, Title: {book['title']}, Author: {book['author']}, "
                      f"Price: {book['price']}, Stock: {book['stock']}, Publisher ID: {book['publisher_id']}")
        else:
            print("No books found.")
    else:
        print(f"Failed to fetch books: {response.json()}")

def search_books():
    """Function to search for books by title or author."""
    title = input("Enter book title to search (leave blank to skip): ")
    author = input("Enter book author to search (leave blank to skip): ")
    params = {}
    if title:
        params["title"] = title
    if author:
        params["author"] = author
    response = requests.get(f"{Base_url}/books/search-books", params=params)
    if response.status_code == 200:
        books = response.json()
        if books:
            print("Search Results:")
            for book in books:
                print(f"ID: {book['id']}, Title: {book['title']}, Author: {book['author']}, "
                      f"Price: {book['price']}, Stock: {book['stock']}, Publisher ID: {book['publisher_id']}")
        else:
            print("No books found matching the search criteria.")
    else:
        print(f"Failed to search books: {response.json()}")

def delete_book():
    """Function to delete a book by ID."""
    book_id = int(input("Enter the ID of the book to delete: "))
    response = requests.delete(f"{Base_url}/books/{book_id}")
    if response.status_code == 200:
        print(response.json()["message"])
    else:
        print(f"Failed to delete book: {response.json()}")

def update_book():
    """Function to update a book's price and stock."""
    book_id = int(input("Enter the ID of the book to update: "))
    price = float(input("Enter the new price: "))
    stock = int(input("Enter the new stock: "))
    response = requests.put(f"{Base_url}/books/{book_id}", json={"price": price, "stock": stock})
    if response.status_code == 200:
        print("Book updated successfully!")
        print(response.json())
    else:
        print(f"Failed to update book: {response.json()}")

def menu():
    """Main menu for the client."""
    while True:
        print("\nBook Inventory Management")
        print("1. Create Publisher")
        print("2. List Publishers")
        print("3. Create Book")
        print("4. List Books")
        print("5. Search Books")
        print("6. Delete Book")
        print("7. Update Book")
        print("8. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            create_publisher()
        elif choice == "2":
            list_publishers()
        elif choice == "3":
            create_book()
        elif choice == "4":
            list_books()
        elif choice == "5":
            search_books()
        elif choice == "6":
            delete_book()
        elif choice == "7":
            update_book()
        elif choice == "8":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()


crud.py
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

def update_book(db:Session,book:schemas.BookUpdate):
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

database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Database_Url="sqlite:///./books.db"

engine=create_engine(Database_Url,connect_args={"check_same_thread":False})

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

models.py
from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
import models,schemas,crud
from database import SessionLocal,engine
models.Base.metadata.create_all(bind=engine)
app=FastAPI(title="BookStore Inventory API")

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.put("/books/",response_model=schemas.Book)
def update_book(book_id:int,book:schemas.BookUpdate,db:Session=Depends(get_db)):
    db_book=crud.update_book(db,book_id,book)
    if not db_book:
        raise HTTPException(status_code=404,detail="Book not found")
    return db_book

@app.delete("/books/{book_id}")
def delete_book(book_id:int,db:Session=Depends(get_db)):
    db_book=crud.delete_book(db,book_id)
    if not db_book:
        raise HTTPException(status_code=404,detail="Book not found")
    return {"message":f"Book with Id {book_id} deleted successfully"}
@app.get("/books/search-books", response_model=list[schemas.Book])
def search_books(title: str = None, author: str = None, db: Session = Depends(get_db)):
    return crud.search_books(db, title, author)

@app.get("/books/",response_model=list[schemas.Book])
def read_books(db:Session=Depends(get_db)):
    return crud.get_all_books(db)

@app.get("/books/{book_id}",response_model=schemas.Book)
def read_book(book_id:int,db:Session=Depends(get_db)):
    book=crud.get_book_by_id(db,book_id)
    if not book:
        raise HTTPException(status_code=404,detail="Book not found")
    return book



@app.post("/publishers/",response_model=schemas.Publisher)
def create_publisher(publisher:schemas.PublisherCreate,db:Session=Depends(get_db)):
    return crud.create_publisher(db,publisher)

@app.get("/publishers/",response_model=list[schemas.Publisher])
def read_publishers(db:Session=Depends(get_db)):
    return crud.get_all_publishers(db)

@app.get("/publishers/{publisher_id}",response_model=schemas.Publisher)
def read_publisher(publisher_id:int,db:Session=Depends(get_db)):
    publisher=crud.get_publisher_by_id(db,publisher_id)
    if not publisher:
        raise HTTPException(status_code=404,detail="Publisher not found")
    return publisher







schemas.py
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


