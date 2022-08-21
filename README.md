<h1>에이블리 과제</h1>
<h2>로컬 실행 방법</h2>

- 가상환경 설치 (https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)
- 가상환경 실행 
- requirement 설치 (pip install -r requirements.txt)
- migrate 실행 (python manage.py migrate)
- runserver (python manage.py runserver)

<h2>프로젝트 설명</h2>
<h3>환경</h3>
- OS: Windows
- Language: Python
- Framework: Django
- DB: SQLite3

<h3>주요 기능</h3>
- 회원 가입 기능
- 로그인 기능
- 내 정보 보기 기능
- 비밀번호 찾기 (재설정) 기능
- 핸드폰 인증 기능
  - 기본적인 데이터 검증 (핸드폰 번호 유효성, 필수 데이터 검증)
  - 1번의 인증 당 3번의 인증 기회 부여, 3분의 유효기간
