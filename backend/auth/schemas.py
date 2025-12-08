"""
Pydantic schemas for authentication requests and responses.
Provides data validation and serialization.
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserRegister(BaseModel):
    """Schema for user registration request."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)


class UserLogin(BaseModel):
    """Schema for user login request."""
    username: str
    password: str


class UserResponse(BaseModel):
    """Schema for user data response."""
    id: int
    username: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
