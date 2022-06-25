# django-vote-15th
15기 백엔드 투표 어플리케이션


## API 문서

[Postman API Documentation](https://documenter.getpostman.com/view/16157648/Uz59Q14o)
  
  
## ERD 이미지

<img width="673" alt="스크린샷 2022-05-26 오전 9 26 00" src="https://user-images.githubusercontent.com/78442839/170390704-e4f1ba60-c2af-4db4-987d-46cd9f859572.png">

- 각 유저는 무조건 한 번씩만 투표 가능
- 조회 요청(GET 요청) 의 경우 로그인 없이도 접근 가능
- 후보자는 가입된 유저인지의 유무 상관없이 등록 가능
  

## 📥 과제

Simple JWT를 이용하여 회원가입과 로그인에 필요한 토큰 발급

access 토큰의 유효기간은 3시간, refresh 토큰의 유효기간은 14일

### 회원가입

- 아이디, 이메일, 비밀번호를 입력하여 회원가입
- 이미 존재하는 아이디 혹은 이메일을 입력하면 에러 메세지 반환
- 회원가입 성공 시 access 토큰과 refresh 토큰 발급
- 성공 메세지, 아이디, access 토큰, refresh 토큰 반환

### 로그인

- 아이디, 비밀번호 입력하여 로그인
- 존재하지 않는 아이디 혹은 잘못된 비밀번호를 입력하면 에러 메세지 반환
- 로그인 성공 시 access 토큰과 refresh 토큰 발급
- 성공 메세지, 아이디, access 토큰, refresh 토큰, 투표 여부 반환
   
  

## 🔧 개선점

- 백엔드 서버에 HTTPS 적용 후 쿠키 인증 방식으로 리팩토링 필요
- Simple JWT에서 제공하는 `TokenVerifyView`, `TokenRefreshView` 이용하여 토큰 인증, 재발급 기능 구현 필요
