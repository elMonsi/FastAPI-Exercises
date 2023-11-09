from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    published_date: int
    rating: int

    def __init__(self, id, title, author, description, published_date, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.published_date = published_date
        self.rating = rating

class BookRequest(BaseModel):
    id: Optional[int] = Field(default=None, title="ID is not mandatory")
    title: str = Field(min_length=3, title="Book Title")
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    published_date: int = Field(gt=1999, lt=2031)
    rating: int = Field(gt=-1, lt=6)

    class Config:
        json_schema_extra = {
            'example':{
                'title': 'A new book',
                'author': 'elMonsi',
                'description': 'A new book description',
                'published_date': 2023,
                'rating': 5
            }
        }

BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book!", 2009, 5),
    Book(2, "Be Fast with FastAPI", "codingwithroby", "A great book!", 2009, 5),
    Book(3, "Master Endpoints", "codingwithroby", "An awesome book!", 2008, 5),
    Book(4, "HP1", "Author 1", "Book Description", 2008, 2),
    Book(5, "Hp2", "Author 2", "Book Description", 2010, 3),
    Book(6, "HP3", "Author 3", "Book Description", 2010, 1),
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=-1, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_book_by_published_date(published_date: int = Query(gt=1999, lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    if len(BOOKS) > 0 :
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')