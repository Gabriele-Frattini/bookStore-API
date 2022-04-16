import os
from urllib.request import Request
from fastapi import (
    FastAPI,
    Body,
    Request,
    status)
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
import motor.motor_asyncio
from database import MONGODB_URL
from models import Schema, PostSchema
from scraper import Scraper
import pathlib

BASE_DIR = pathlib.Path(__file__).parent
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.books
db_collection = db.get_collection("books_collection")


@app.get("/")
async def home_view(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/books", response_description="List all books", response_model=List[Schema])
async def list_books():
    books = await db["books"].find().to_list(1000)
    return books


@app.post('/post/{bookTitle}/{isbn}', response_model=Schema, status_code=status.HTTP_201_CREATED)
async def get_post(input: PostSchema):

    if (data := await db["books"].find_one({"isbn": input.isbn})) is None:
        data = Scraper(isbn=input.isbn, bookTitle=input.bookTitle)
        data = data.cheapestBook()
        bson_data = jsonable_encoder(data)

        new_data = await db["books"].insert_one(bson_data)
        created_data = await db["books"].find_one({"_id": new_data.inserted_id})
        return created_data

    else:
        data = await db["books"].find_one({"isbn": input.isbn})
        return data
