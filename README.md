<h1>에이블리 과제</h1>
<h2>로컬 실행 방법</h2>

- 가상환경 설치 (https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)
- 가상환경 실행 
- requirement 설치 (pip install -r requirements.txt)
- migrate 실행 (python manage.py migrate)
- runserver (python manage.py runserver)

<h2>프로젝트 설명</h2>
<h3>개발환경</h3>
- OS: Windows
- Language: Python
- Framework: Django
- DB: SQLite3

<h3>주요 기능</h3>
- 회원 가입 기능
  - 세션키가 있어야 접근할 수 있도록 제한 (핸드폰 인증 후)
  - 중복 아이디, 필수값 체크 후 유저 생성
- 로그인 기능
  - JWT 토큰 사용하여 로그인 기능 구현
  - 식별 가능한 정보는 아이디(username) 하나로만 했습니다.</br>한 명의 사람이 같은 핸드폰이나 이메일로 여러개의 아이디를 생성 할 수 있는것이 보통의 접근이라 판단하였습니다.</br>다른 사이트에서 핸드폰 인증을 하면 내가 가입한 아이디 리스트가 뜨는 것처럼 말입니다.</br>여기서 좀 더 신경을 쓴다면 같은 인증(핸드폰, 이메일)을 사용하여 가입할 수 있는 계정의 수를 제한하는 식으로 접근하면 좋을 것 같습니다.</br>이메일 가입의 경우 OAuth를 사용하면 좋을 것 같습니다.
- 내 정보 보기 기능
  - 토큰을 지니고 있는 유저가 자신의 정보를 볼 수 있도록 구현
  - 본인의 user_id 와 일치하는 정보만 조회할 수 있도록 제외
- 비밀번호 찾기 (재설정) 기능
  - 세션키가 있어야 접근할 수 있도록 제한 (핸드폰 인증 후)
- 핸드폰 인증 기능
  - 기본적인 데이터 검증 (핸드폰 번호 유효성, 필수 데이터 검증)
  - 1번의 인증 당 3번의 인증 기회 부여, 3분의 유효기간
  - 인증 완료 시 세션 생성

<h3>보완 사항</h3>
- 미리 아이디 중복체크 가능한 API 생성
- 세션 테이블을 커스텀해서 해당 세션이 어떤 기능을 수행할 지 정해놓기 (보안성 향상 기대)
- 그룹, 권한 관리까지 더 들어가서 API 별 권한 관리가 이루어 질 수 있을 것임