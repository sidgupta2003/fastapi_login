from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role_id: int

class UserOut(BaseModel):
    id: int
    username: str
    role_id: int

    class Config:
        orm_mode = True
