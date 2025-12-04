"""
FastAPI GET/POST 요청 처리 및 JSON 응답
- 경로 매개변수 처리
- 쿼리 매개변수 처리
- POST 요청 본문 처리
- JSON 응답 반환
"""

from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="요청/응답 처리 API",
    description="GET/POST 요청 처리 및 JSON 응답 예제",
    version="1.0.0"
)

# 요청 데이터 모델 정의
class UserCreate(BaseModel):
    name: str
    email: str
    age: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None
    message: str

# 임시 데이터 저장소
users_db = []
user_id_counter = 1

# GET 요청 - 경로 매개변수
@app.get("/users/{user_id}")
def get_user(user_id: int):
    """
    특정 사용자 정보 조회 (경로 매개변수 사용)
    """
    for user in users_db:
        if user["id"] == user_id:
            return {"user": user, "found": True}
    
    return {"message": f"사용자 ID {user_id}를 찾을 수 없습니다.", "found": False}

# GET 요청 - 쿼리 매개변수
@app.get("/users")
def get_users(
    limit: int = Query(10, description="반환할 사용자 수", ge=1, le=100),
    skip: int = Query(0, description="건너뛸 사용자 수", ge=0),
    name: Optional[str] = Query(None, description="이름으로 필터링")
):
    """
    사용자 목록 조회 (쿼리 매개변수 사용)
    """
    filtered_users = users_db
    
    # 이름으로 필터링
    if name:
        filtered_users = [user for user in filtered_users if name.lower() in user["name"].lower()]
    
    # 페이지네이션 적용
    paginated_users = filtered_users[skip:skip + limit]
    
    return {
        "users": paginated_users,
        "total": len(filtered_users),
        "limit": limit,
        "skip": skip
    }

# POST 요청 - JSON 본문 처리
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    """
    새 사용자 생성 (POST 요청 본문 처리)
    """
    global user_id_counter
    
    # 새 사용자 데이터 생성
    new_user = {
        "id": user_id_counter,
        "name": user.name,
        "email": user.email,
        "age": user.age
    }
    
    # 데이터베이스에 추가
    users_db.append(new_user)
    user_id_counter += 1
    
    # 응답 데이터 생성
    response = UserResponse(
        id=new_user["id"],
        name=new_user["name"],
        email=new_user["email"],
        age=new_user["age"],
        message="사용자가 성공적으로 생성되었습니다."
    )
    
    return response

# GET 요청 - 복합 쿼리 매개변수
@app.get("/search")
def search_users(
    q: str = Query(..., description="검색어", min_length=1),
    age_min: Optional[int] = Query(None, description="최소 나이", ge=0),
    age_max: Optional[int] = Query(None, description="최대 나이", le=150)
):
    """
    사용자 검색 (복합 쿼리 매개변수)
    """
    results = []
    
    for user in users_db:
        # 이름 또는 이메일에서 검색어 확인
        if (q.lower() in user["name"].lower() or 
            q.lower() in user["email"].lower()):
            
            # 나이 범위 확인
            if age_min is not None and user.get("age") and user["age"] < age_min:
                continue
            if age_max is not None and user.get("age") and user["age"] > age_max:
                continue
                
            results.append(user)
    
    return {
        "query": q,
        "age_range": {"min": age_min, "max": age_max},
        "results": results,
        "count": len(results)
    }

# POST 요청 - 복잡한 데이터 처리
@app.post("/users/batch")
def create_multiple_users(users: list[UserCreate]):
    """
    여러 사용자 일괄 생성
    """
    global user_id_counter
    created_users = []
    
    for user_data in users:
        new_user = {
            "id": user_id_counter,
            "name": user_data.name,
            "email": user_data.email,
            "age": user_data.age
        }
        
        users_db.append(new_user)
        created_users.append(new_user)
        user_id_counter += 1
    
    return {
        "message": f"{len(created_users)}명의 사용자가 생성되었습니다.",
        "created_users": created_users,
        "total_users": len(users_db)
    }

if __name__ == "__main__":
    import uvicorn
    # uvicorn 02_request_response:app --reload
    uvicorn.run(app, host="127.0.0.1", port=8000)
