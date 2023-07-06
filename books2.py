from typing import Optional

from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status


app = FastAPI()
BOOKS = []



class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(title='id is not required')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=500)
    rating: int = Field(gt=0, lt=10)

    class Config:
        schema_extra = {
            'example': {
                'title': "Some New Book", 
                'author': 'An Author', 
                'description': 'Description of the New Book',
                'rating': 4,
            }
        }
    

BOOKS = [
    Book(1, 'Automate the Boring Stuff with Python', 'Al Sweigart', 
    'Learn how to use Python to write programs that do in minutes what would take you hours to do by hand', 8),
    Book(2, 'Grokking Algorithms', ' Aditya Bhargava', 
    'An Illustrated Guide for Programmers and Other Curious People', 7),
    Book(3, 'Data Structures the Fun Way', 'Jeremy Kubica', 
    'Learn how and when to use the right data structures in any situation, strengthening your computational thinking, problem-solving, and programming skills in the process.',
     6),
]

@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.get("/books_by_rating/{rating}")
async def get_book_by_rading(book_rating: int):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book


@app.post("/create_book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(assign_book_id(new_book))


def assign_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


