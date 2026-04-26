from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str
    email: Optional[EmailStr] = None

class User(UserBase):
    id: int
    avatar: Optional[str] = None
    bio: Optional[str] = None
    catchphrase: Optional[str] = None
    gender: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None
    catchphrase: Optional[str] = None
    gender: Optional[str] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Password reset schemas
class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    email: EmailStr
    verification_code: str
    new_password: str

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

class ReviewBase(BaseModel):
    content: str
    rating: int

class ReviewCreate(ReviewBase):
    merchant_id: int

class Review(ReviewBase):
    id: int
    user_id: int
    merchant_id: int
    created_at: datetime
    merchant: "Merchant"

    class Config:
        from_attributes = True

class MerchantBase(BaseModel):
    name: str
    description: str
    address: str
    category: str
    phone: str
    image_url: str

class MerchantCreate(MerchantBase):
    pass

class Merchant(MerchantBase):
    id: int
    rating: float
    reviews_count: int
    created_at: datetime

    class Config:
        from_attributes = True
