from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role_id: int

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role_id: int

    class Config:
        from_attributes = True  # Use the new configuration key

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None