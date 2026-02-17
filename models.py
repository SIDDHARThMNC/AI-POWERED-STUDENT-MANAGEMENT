from pydantic import BaseModel, EmailStr
from typing import Optional

class Student(BaseModel):
    name: str
    age: int
    course: str
    email: Optional[EmailStr] = None


# 🔥 Add this
class Feedback(BaseModel):
    text: str
