from fastapi import FastAPI, HTTPException
from typing import List, Optional
from models import Student, Feedback
from database import students
from nlp_utils import analyze_sentiment, smart_search

app = FastAPI(
    title="Student Management API",
    description="CRUD + Filter + Search + Smart Search + Sentiment Analysis",
    version="2.0.0"
)


# Home Route
@app.get("/")
def home():
    return {"message": "Welcome to Student Management API 🚀"}


# Get All Students
@app.get("/students", response_model=List[Student])
def get_students():
    return students


# Create Single Student
@app.post("/students", response_model=Student)
def create_student(student: Student):
    students.append(student)
    return student


# Bulk Create Students
@app.post("/students/bulk", response_model=List[Student])
def create_multiple_students(new_students: List[Student]):
    students.extend(new_students)
    return new_students


# Get Student by ID
@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    if student_id < 0 or student_id >= len(students):
        raise HTTPException(status_code=404, detail="Student not found")
    return students[student_id]


# Update Student
@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    if student_id < 0 or student_id >= len(students):
        raise HTTPException(status_code=404, detail="Student not found")

    students[student_id] = updated_student

    return {
        "message": "Student updated successfully",
        "data": updated_student
    }


# Delete Student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id < 0 or student_id >= len(students):
        raise HTTPException(status_code=404, detail="Student not found")

    deleted_student = students.pop(student_id)

    return {
        "message": "Student deleted successfully",
        "deleted_student": deleted_student
    }


# Filter Students by Course
@app.get("/filter")
def filter_students(course: Optional[str] = None):

    if not course:
        return {"message": "Please provide course query parameter"}

    filtered = [
        s for s in students
        if s.course.lower() == course.lower()
    ]

    return {
        "count": len(filtered),
        "students": filtered
    }


# Normal Search by Name
@app.get("/search")
def search_student(name: str):

    result = [
        s for s in students
        if name.lower() in s.name.lower()
    ]

    if not result:
        raise HTTPException(
            status_code=404,
            detail="No student found with this name"
        )

    return {
        "count": len(result),
        "students": result
    }


# Smart Search (Name + Course)
@app.get("/smart-search")
def smart_search_api(query: str):

    results = smart_search(students, query)

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No matching students found"
        )

    return {
        "count": len(results),
        "students": results
    }


# Sentiment Analysis API
@app.post("/analyze-feedback")
def analyze_feedback(feedback: Feedback):
    result = analyze_sentiment(feedback.text)

    return {
        "text": feedback.text,
        "analysis": result
    }
