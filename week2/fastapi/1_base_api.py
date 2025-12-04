from fastapi import FastAPI,Form
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    age: int


app = FastAPI(
    title="My API",
    description="This is a simple API",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/users")
def create_user(name: str = Form(...), email: str = Form(...), age: int = Form(...)):
    return {"message": "User created successfully", "name": name, "email": email, "age": age}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)