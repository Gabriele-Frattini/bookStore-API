from email.header import Header
from typing import Optional
from pydantic import BaseModel, Field
from bson.objectid import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Schema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    isbn: str = Field(...)
    bookTitle: str = Field(...)
    company: str = Field(...)
    price: int = Field(...)
    url: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                'isbn': '9780321270009',
                'bookTitle': 'calculus',
                'company': 'campusbokhandeln',
                'price': 228,
                'url': 'https://campusbokhandeln.se/b/9780321270009/calculus?'
            }

        }


class PostSchema(BaseModel):
    isbn: Optional[str]
    bookTitle: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

        schema_extra = {
            "example": {
                'isbn': '9780321270009',
                'bookTitle': 'calculus'
            }

        }


def ResponseModel(data, message):
    return {
        'data': [data],
        'code': 200,
        'message': message,
    }
