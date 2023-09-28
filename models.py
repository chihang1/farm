from typing import Optional, Any
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue

# def SuccessResponseModel(status_code, data, message):
#     return {
#         'data': [data],
#         'code': status_code,
#         'message': message
#     }

class PyObjectId(ObjectId):
    @classmethod
    def validate_object_id(cls, v: Any, handler) -> ObjectId:
        if isinstance(v, ObjectId):
            return v
        s = handler(v)
        if ObjectId.is_valid(s):
            return ObjectId(s)
        else:
            raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, _handler) -> core_schema.CoreSchema:
        assert source_type is ObjectId
        return core_schema.no_info_wrap_validator_function(
            cls.validate_object_id, 
            core_schema.str_schema(), 
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, handler) -> JsonSchemaValue:
        return handler(core_schema.str_schema())

class Task(BaseModel):
#     id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    title: str
    description: str
    completed: bool = False

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
        populate_by_name = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            'example': {
                'title': 'haha5622',
                'description': 'hahaahaha'
            }
        }
class UpdateTask(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {ObjectId: str}

class TaskResponseModel(BaseModel):
    id: str
    title: str
    description: str
    completed: bool