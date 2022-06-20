# django-vote-15th

### Erd 구성
<img width="1038" alt="스크린샷 2022-05-27 오후 9 01 01" src="https://user-images.githubusercontent.com/59060780/170695491-b80cc391-e290-4fcf-a7d2-65e53850b5c6.png">

[ERD Diagram](https://www.erdcloud.com/d/QfRE7RTFGHdbL85uG)

### API 명세서
[API Documentation](https://documenter.getpostman.com/view/18320343/UzBjs7uf)

-----

### 회원가입/로그인

* simple-jwt로 회원가입 및 로그인 시 access_token/refresh_token 반환
* 각각 1시간/24시간의 만료 기간을 가짐
* access_token 만료 시 헤더에 refresh_token 담아서 api/refreshes로 요청 시 새로운 access_token 발급
* 회원가입 시 필요한 정보는 이름/이메일/비밀번호/파트 (이메일은 중복 불가)
* 로그인 시 필요한 정보는 이메일/비밀번호

### 투표
* 후보자는 미리 등록되어 있음
* 투표는 기본적으로 여러 명 투표 가능
* 동일 후보자에게 중복 투표 불가능
* 본인한테 투표 불가능
* 투표는 로그인 한 사용자만 이용 가능
* 투표 결과는 파트별로 보여줌 (득표수 순 => 동수 득표면 이름 순)


### Https 
> docker compose로 certbot을 같이 빌드하며 적용하려 했으나 알 수 없는 이유로 실패 => AWS의 router 53으로 도메인 발급 -> Certificate Manager를 이용하여 SSL인증 -> EC2의 로드밸런서를 이용하여 https 요청이 들어오면 로드밸런서가 nginx에게 http로 수정하여 전송 nginx는 8000 포트의 내 프로젝트에게 전송 하는 방식으로 https를 연동했다.


#### 과정

![스크린샷 2022-06-21 오전 12 07 32](https://user-images.githubusercontent.com/59060780/174631508-c2c5a888-84eb-43e4-b1e8-fef099f6c921.png)

* router 53을 이용하여 도메인 발급


![스크린샷 2022-06-21 오전 12 08 37](https://user-images.githubusercontent.com/59060780/174631688-28c65c46-db48-4dc4-a5c7-9a97578b4be2.png)

* Certificate Manager를 이용하여 발급받은 도메인에 SSL 인증서 발급 (Certificate Manager를 이용하려면 AWS에서 발급받은 도메인이 필요)

![스크린샷 2022-06-21 오전 12 13 42](https://user-images.githubusercontent.com/59060780/174632553-49c81fd6-21af-4a98-80a5-039f481b5cfa.png)

* Ec2의 로드밸런서를 사용하여 https의 443포트 요청을 처리할 수 있게 해줌
* http로 요청이 와도 https로 리디렉션 되도록 설정


![스크린샷 2022-06-21 오전 12 15 47](https://user-images.githubusercontent.com/59060780/174632907-5e058dde-061a-414d-8581-84ce56905403.png)

* 마지막으로 발급받은 도메인에 A 타입으로 로드밸런서를 연결해주면 설정이 완료된다

![스크린샷 2022-06-21 오전 12 06 37](https://user-images.githubusercontent.com/59060780/174631343-e8803153-90a8-4b7b-a144-cbe5f5e207e7.png)

