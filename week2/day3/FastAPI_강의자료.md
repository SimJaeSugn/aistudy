# FastAPI를 활용한 API 제작

## FastAPI 개요

FastAPI는 Python으로 API를 빠르고 쉽게 구축할 수 있는 현대적인 웹 프레임워크입니다. Starlette과 Pydantic을 기반으로 하여 높은 성능과 개발자 친화적인 기능을 제공합니다.

### FastAPI의 주요 특징

**빠른 성능**
- NodeJS와 Go에 필적하는 높은 성능
- 비동기 처리 지원으로 동시성 향상

**쉬운 개발**
- 직관적이고 간단한 문법
- Python 타입 힌트 기반의 자동 검증
- 자동 API 문서 생성 (Swagger UI, ReDoc)

**표준 준수**
- OpenAPI 표준 완전 지원
- JSON Schema 자동 생성
- OAuth2, JWT 등 보안 표준 지원

**개발자 경험**
- IDE에서 뛰어난 자동완성 지원
- 런타임 에러 감소
- 테스트 작성이 용이

## 설치 및 기본 설정

FastAPI 설치:
```bash
pip install fastapi uvicorn
```

기본 서버 실행:
```bash
uvicorn main:app --reload
```

## API 서버 구현 기초

### GET 요청 처리
- 데이터 조회에 사용
- URL 경로나 쿼리 파라미터로 데이터 전달
- 응답은 주로 JSON 형태

### POST 요청 처리
- 데이터 생성에 사용
- 요청 본문(body)에 JSON 데이터 포함
- 생성된 데이터나 상태 정보를 JSON으로 응답

### 경로 매개변수와 쿼리 매개변수
- 경로 매개변수: URL 경로의 일부로 전달되는 값
- 쿼리 매개변수: URL 뒤에 ?key=value 형태로 전달되는 값

## 데이터베이스 연동

### SQLite 사용
- 파일 기반의 경량 데이터베이스
- 개발 및 테스트 환경에 적합
- 별도 서버 설치 불필요

### 데이터 모델링
- Pydantic 모델을 사용한 데이터 검증
- 요청/응답 데이터의 구조 정의
- 자동 타입 검증 및 변환

### CRUD 연산
- Create: 데이터 생성 (POST)
- Read: 데이터 조회 (GET)
- Update: 데이터 수정 (PUT/PATCH)
- Delete: 데이터 삭제 (DELETE)

## 프론트엔드와의 연결

### CORS 설정
- Cross-Origin Resource Sharing
- 브라우저에서 다른 도메인의 API 호출 허용
- 개발 환경에서 필수 설정

### API 엔드포인트 설계
- RESTful API 원칙 준수
- 명확하고 일관된 URL 구조
- HTTP 상태 코드 적절한 사용

### 데이터 교환
- JSON 형태의 데이터 교환
- 요청/응답 데이터 구조 명확히 정의
- 에러 처리 및 상태 코드 관리

## 실습 파일 구성

1. `01_basic_api.py` - 기본 API 서버 구현
2. `02_request_response.py` - GET/POST 요청 처리
3. `03_database_api.py` - 데이터베이스 연동 API

각 파일은 단계별로 학습할 수 있도록 구성되어 있으며, 실제 실행 가능한 코드로 작성되었습니다.
