"""
FastAPI 데이터베이스 연동 API
- SQLite 데이터베이스 연결
- 데이터베이스 테이블 생성
- 데이터 CRUD 연산
- 데이터베이스 연동 API 엔드포인트
"""

import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import os

app = FastAPI(
    title="데이터베이스 연동 API",
    description="SQLite 데이터베이스와 연동된 API 서버",
    version="1.0.0"
)

# 데이터베이스 파일 경로
DB_PATH = "users.db"

# 데이터 모델 정의
class UserBase(BaseModel):
    name: str
    email: str
    age: Optional[int] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None

class UserResponse(UserBase):
    id: int

# 데이터베이스 초기화
def init_database():
    """
    데이터베이스 테이블 생성
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER
        )
    """)
    
    conn.commit()
    conn.close()

# 데이터베이스 연결 헬퍼 함수
def get_db_connection():
    """
    데이터베이스 연결 반환
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 딕셔너리 형태로 결과 반환
    return conn

# 애플리케이션 시작 시 데이터베이스 초기화
@app.on_event("startup")
def startup_event():
    init_database()

# 모든 사용자 조회
@app.get("/users", response_model=List[UserResponse])
def get_all_users():
    """
    모든 사용자 목록 조회
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    
    return [dict(user) for user in users]

# 특정 사용자 조회
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """
    특정 사용자 정보 조회
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    
    return dict(user)

# 사용자 생성
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    """
    새 사용자 생성
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            (user.name, user.email, user.age)
        )
        user_id = cursor.lastrowid
        conn.commit()
        
        # 생성된 사용자 정보 조회
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        created_user = cursor.fetchone()
        conn.close()
        
        return dict(created_user)
    
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")

# 사용자 정보 수정
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate):
    """
    사용자 정보 수정
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 사용자 존재 확인
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    existing_user = cursor.fetchone()
    
    if existing_user is None:
        conn.close()
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    
    # 업데이트할 필드 준비
    update_fields = []
    update_values = []
    
    if user_update.name is not None:
        update_fields.append("name = ?")
        update_values.append(user_update.name)
    
    if user_update.email is not None:
        update_fields.append("email = ?")
        update_values.append(user_update.email)
    
    if user_update.age is not None:
        update_fields.append("age = ?")
        update_values.append(user_update.age)
    
    if not update_fields:
        conn.close()
        raise HTTPException(status_code=400, detail="수정할 데이터가 없습니다.")
    
    # 업데이트 실행
    update_values.append(user_id)
    update_query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
    
    try:
        cursor.execute(update_query, update_values)
        conn.commit()
        
        # 수정된 사용자 정보 조회
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        updated_user = cursor.fetchone()
        conn.close()
        
        return dict(updated_user)
    
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")

# 사용자 삭제
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    """
    사용자 삭제
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 사용자 존재 확인
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    
    if user is None:
        conn.close()
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    
    # 사용자 삭제
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    return {"message": f"사용자 ID {user_id}가 삭제되었습니다."}

# 이메일로 사용자 검색
@app.get("/users/search/email/{email}", response_model=UserResponse)
def get_user_by_email(email: str):
    """
    이메일로 사용자 검색
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user is None:
        raise HTTPException(status_code=404, detail="해당 이메일의 사용자를 찾을 수 없습니다.")
    
    return dict(user)

# 나이 범위로 사용자 검색
@app.get("/users/search/age", response_model=List[UserResponse])
def get_users_by_age_range(min_age: int = 0, max_age: int = 150):
    """
    나이 범위로 사용자 검색
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM users WHERE age BETWEEN ? AND ?",
        (min_age, max_age)
    )
    users = cursor.fetchall()
    conn.close()
    
    return [dict(user) for user in users]

# 데이터베이스 통계
@app.get("/stats")
def get_database_stats():
    """
    데이터베이스 통계 정보
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 총 사용자 수
    cursor.execute("SELECT COUNT(*) as total FROM users")
    total_users = cursor.fetchone()["total"]
    
    # 평균 나이
    cursor.execute("SELECT AVG(age) as avg_age FROM users WHERE age IS NOT NULL")
    avg_age_result = cursor.fetchone()["avg_age"]
    avg_age = round(avg_age_result, 2) if avg_age_result else None
    
    # 최고/최저 나이
    cursor.execute("SELECT MIN(age) as min_age, MAX(age) as max_age FROM users WHERE age IS NOT NULL")
    age_range = cursor.fetchone()
    
    conn.close()
    
    return {
        "total_users": total_users,
        "average_age": avg_age,
        "min_age": age_range["min_age"],
        "max_age": age_range["max_age"]
    }

if __name__ == "__main__":
    import uvicorn
    
    # uvicorn 03_database_api:app --reload --port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
