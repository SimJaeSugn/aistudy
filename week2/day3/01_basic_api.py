"""
FastAPI 기본 API 서버 구현
- 가장 간단한 FastAPI 애플리케이션
- 기본 라우트 설정
- 서버 실행 방법
"""

from fastapi import FastAPI

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="기본 API 서버",
    description="FastAPI를 사용한 가장 간단한 API 서버입니다.",
    version="1.0.0"
)

# 루트 경로 라우트
@app.get("/")
def read_root():
    """
    루트 경로에 대한 GET 요청 처리
    """
    return {"message": "Hello, FastAPI!"}

# 간단한 정보 제공 라우트
@app.get("/info")
def get_info():
    """
    서버 정보를 반환하는 엔드포인트
    """
    return {
        "server": "FastAPI",
        "version": "1.0.0",
        "description": "기본 API 서버 예제"
    }

# 상태 확인 라우트
@app.get("/health")
def health_check():
    """
    서버 상태를 확인하는 헬스체크 엔드포인트
    """
    return {"status": "healthy", "code": 200}

if __name__ == "__main__":
    import uvicorn
    
    # 서버 실행
    # 터미널에서 실행: uvicorn 01_basic_api:app --reload
    uvicorn.run(app, host="127.0.0.1", port=8000)
