# django-vote-15th
15기 백엔드 투표 어플리케이션


## API 문서

[Postman API Documentation](https://documenter.getpostman.com/view/16157648/Uz59Q14o)
  
  
## ERD 이미지

<img width="673" alt="스크린샷 2022-05-26 오전 9 26 00" src="https://user-images.githubusercontent.com/78442839/170390704-e4f1ba60-c2af-4db4-987d-46cd9f859572.png">

---

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

---

### 투표하기

- 로그인 상태의 유저에 한하여 투표 허용
- 각 유저는 무조건 한 번씩만 투표 가능
- 투표 후 `candidate 모델의 count` 증가, `user 모델의 is_voted 필드` True로 업데이트
- 투표 성공 시 message, 유저 이름, 투표 여부 반환

### 후보자 등록하기

- 로그인 상태의 유저에 한하여 후보자 등록 허용
- 이미 등록되어 있는 이름의 후보자는 등록할 수 없음
- 성공 시 message, 등록된 후보자의 id, 이름, 투표수 반환

### 투표 현황 조회

- 후보자 목록 전체를 count 순으로 내림차순 정렬하여 반환
- 로그인 여부 상관없이 접근 가능하도록 구현

### 후보자별 투표자 조회

- 각 후보자별 투표자 리스트 반환

---

## 💡 회고

- 서버 세팅 후, CORS 에러 해결하기 위해 `django-cors-headers` 라는 모듈 사용
  - `base.py`에서 최대한 위 쪽에 위치해서 세팅해야 cors 에러가 재발하지 않는 것을 알 수 있었음
- 도커의 web 컨테이너에서 어드민을 생성하여 편리하게 관리
    ```
  sudo docker-compose exec web python manage.py createsuperuser
  ```
- 쿠키 설정 후 서버에는 쿠키 반영되지만 프론트 브라우저에서 쿠키가 확인되지 않는 이슈

  <img width="1048" alt="스크린샷 2022-06-23 오후 5 34 22" src="https://user-images.githubusercontent.com/78442839/175762002-7f7dcb9f-4a78-4a59-bf83-0c5e70b5e11e.png">

  - 백엔드에서 쿠키 설정 시 samesite 옵션이 지정되어 있으면 chrome 과 같은 브라우저에서 자동으로 `samesite=Lax` 로 받아들이도록 정책 변경
    - 참고로 Lax 의 경우 자사 도메인이 아니어도 일부 케이스(GET 요청 등)에서는 접근이 허용되나, POST 요청 등과 같은 경우 접근 불가
  - 쿠키를 cross-domain에서 허용하기 위해서는 `samesite=None, secure=True` 설정 필요
    - `samesite=None` 사용하기 위해서는 secure 옵션 필수
    - secure 옵션은 HTTPS 요청만 허용하기 위한 것이므로 HTTPS 설정 필수<br>


- HTTPS 설정
  - 무료 도메인 발급 후, docker-compose 로 certbot 컨테이너 빌드하여 인증서 발급하려 했으나 실패 → certbot 으로 직접 인증서 발급 완료하여 nginx에서 HTTPS 설정하며 인증 시도했으나 실패
  - 원인을 알 수 없어 AWS에서 HTTPS 설정하기로 결정<br>

  ```
  1. Route 53에서 발급받은 도메인 주소로 호스팅 영역 생성
  2. 도메인 발급받은 사이트에 ec2 IP 주소와 위 호스팅 영역에서 생성된 DNS 업데이트
  3. ACM(AWS Certificate Manager)에서 인증서 발급
  4. HTTP 요청은 HTTPS 로 리디렉션 되도록, HTTPS 요청은 ec2 인스턴스의 HTTP 타겟 그룹으로 연결되도록 로드밸런서 생성
  5. Route 53에 위 로드밸런서 추가
  ```

## 🔧 개선점

- 백엔드 서버에서 HTTPS 적용 확인 후 쿠키 인증 방식으로 최종 리팩토링 필요
- Simple JWT에서 제공하는 `TokenVerifyView`, `TokenRefreshView` 이용하여 토큰 인증, 재발급 기능 구현 필요
