# django-vote-15th

### 회원가입, 로그인
1. 유저 회원가입
> URI: /api/users/signups `POST`
![image](https://user-images.githubusercontent.com/59060780/170649600-af7be397-f2c2-4d4d-a158-6faeabf7ea54.png)

2. 유저 로그인
> URI: /api/users/logins `POST`
![스크린샷 2022-05-27 오후 3 57 31](https://user-images.githubusercontent.com/59060780/170649095-24e303aa-e6ef-408a-8d4e-ae37046e18bc.png)


### 투표
1. 후보 투표 결과 조회 [FE/BE] (득표 수 내림차순)
> URI: /api/candidates/?part=FE `GET`
![image](https://user-images.githubusercontent.com/63996052/170671996-afa4b312-5cfc-4771-92ab-f5e45cc7c884.png)

> URI: /api/candidates/?part=BE `GET`
![image](https://user-images.githubusercontent.com/63996052/170671946-83bb6bcd-df9e-4310-9a66-8d830177f9f3.png)

2. 후보 투표 (중복 투표 불가능, 로그인한 유저만 투표 가능)
> URI: /api/votes `POST`
![image](https://user-images.githubusercontent.com/63996052/170424183-0908ea53-ee5c-464e-be70-70cb28c0b78b.png)
![image](https://user-images.githubusercontent.com/63996052/170671346-30e18559-63ca-482c-ae30-53a7549b3c8e.png)
![image](https://user-images.githubusercontent.com/63996052/170670297-6c51ebe4-90e9-474e-ad18-a188a1a9c054.png)
