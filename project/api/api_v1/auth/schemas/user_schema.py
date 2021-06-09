from pydantic import BaseModel, Field, EmailStr


class ForeignLoginSchema(BaseModel):
    email: EmailStr
    password: str
    imsi: str = Field(default=None)
    code: str = Field(default=None)
    biz_type: str = Field(default=None)
