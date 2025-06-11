
import requests

Base_url="http://127.0.0.1:8070"

def create_publisher():
    try:
        name=input("Enter publisher name:")
        country=input("Enter publisher country:")
        response=requests.post(f"{Base_url}/publishers/",json={"name":name,"country":country})
        response.raise_for_status()
        print("Publisher created successfully")
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error:Failed to create publisher{e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def list_publishers():
    try:
        response=requests.get(f"{Base_url}/publishers/")
        response.raise_for_status()
        publishers=response.json()
        if publishers:
            print("Publishers:")
            for publisher in publishers:
                print(f"ID:{publisher['id']},Name:{publisher['name']},Country:{publisher['country']}")
        else:
            print("No publishers found.")
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch publishers. {e}")
    except Exception as e:
        print(f"Unexpected error:{e}")

def create_book():
    try:
        title=input("Enter book title:")
        author=input("Enter book author:")
        price=float(input("Enter book price:"))
        stock=int(input("Enter book stock:"))
        publisher_id=int(input("Enter publisher ID:"))
        response=requests.post(f"{Base_url}/books/",json={
            "title": title,
            "author": author,
            "price": price,
            "stock": stock,
            "publisher_id": publisher_id
        })
        response.raise_for_status()
        print("Book created successfully!")
        print(response.json())
    except ValueError:
        print("Error:Invalid input.Please enter valid values for price,stock,and publisher ID.")
    except requests.exceptions.RequestException as e:
        print(f"Error:Failed to create book.{e}")
    except Exception as e:
        print(f"Unexpected error:{e}")

def list_books():
    try:
        response=requests.get(f"{Base_url}/books/")
        response.raise_for_status()
        books=response.json()
        if books:
            print("Books:")
            for book in books:
                print(f"ID: {book['id']}, Title: {book['title']}, Author: {book['author']}, "
                      f"Price: {book['price']}, Stock: {book['stock']}, Publisher ID: {book['publisher_id']}")
        else:
            print("No books found.")
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch books.{e}")
    except Exception as e:
        print(f"Unexpected error:{e}")

def search_books():
    try:
        title=input("Enter book title to search (leave blank to skip):")
        author=input("Enter book author to search (leave blank to skip):")
        params={}
        if title:
            params["title"]=title
        if author:
            params["author"]=author
        response=requests.get(f"{Base_url}/books/search-books",params=params)
        response.raise_for_status()
        books=response.json()
        if books:
            print("Search Results:")
            for book in books:
                print(f"ID:{book['id']},Title:{book['title']},Author:{book['author']}, "
                      f"Price:{book['price']},Stock:{book['stock']},Publisher ID:{book['publisher_id']}")
        else:
            print("No books found matching the search criteria.")
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to search books.{e}")
    except Exception as e:
        print(f"Unexpected error:{e}")

def delete_book():
    try:
        book_id = int(input("Enter the ID of the book to delete: "))
        response = requests.delete(f"{Base_url}/books/{book_id}")
        response.raise_for_status()
        print(response.json()["message"])
    except ValueError:
        print("Error:Invalid input.Please enter a valid book ID.")
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to delete book. {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def update_book():
    try:
        book_id=int(input("Enter the ID of the book to update: "))
        price=float(input("Enter the new price: "))
        stock=int(input("Enter the new stock: "))
        response=requests.put(f"{Base_url}/books/{book_id}",json={"price":price,"stock":stock})
        response.raise_for_status()
        print("Book updated successfully!")
        print(response.json())
    except ValueError:
        print("Error:Invalid input.Please enter valid values for price,stock,and book ID.")
    except requests.exceptions.RequestException as e:
        print(f"Error:Failed to update book.{e}")
    except Exception as e:
        print(f"Unexpected error:{e}")

def menu():
    while True:
        print("\nBook Inventory Management")
        print("1.Create Publisher")
        print("2.List Publishers")
        print("3.Create Book")
        print("4.List Books")
        print("5.Search Books")
        print("6.Delete Book")
        print("7.Update Book")
        print("8.Exit")
        choice=input("Enter your choice: ")
        try:
            if choice=="1":
                create_publisher()
            elif choice=="2":
                list_publishers()
            elif choice=="3":
                create_book()
            elif choice=="4":
                list_books()
            elif choice=="5":
                search_books()
            elif choice=="6":
                delete_book()
            elif choice=="7":
                update_book()
            elif choice=="8":
                print("Exiting...")
                break
            else:
                print("Invalid choice.Please try again.")
        except Exception as e:
            print(f"Unexpected error in menu:{e}")

if __name__=="__main__":
    menu()
