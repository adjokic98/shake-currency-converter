from pydantic import BaseModel, EmailStr

class UserSignupRequest(BaseModel):
    email: EmailStr

class UserSignupResponse(BaseModel):
    api_key: str
    credits: int

class UserCreditsResponse(BaseModel):
    credits: int