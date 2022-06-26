## django-vote-15th
15기 백엔드 투표 어플리케이션


<h3> 0. 설계 사항들 </h3>
<ul>
  <li>한 유저당 한 번만 투표 가능함</li>
  <li>한 번 투표시 한 후보자에게만 투표 가능함</li>
  <li> 그 외에는 기본적인 요구 사항들을 충족시킴</li>
</ul>


<h3>1. 모델링</h3><br>

<image src = "./ERD.png">
  
<h3>2. api 페이지 -swagger </h3><br>
  localhost:8000/swagger
  
  <image src = "./api_document1.png">
  <image src = "./api_document2.png">
    

<h3>구현 기능</h3>
<ul>
  <li> 회원가입 </li>
  <li> 로그인 </li>
  <li> 투표 </li>
  <li> 회원 목록 확인 </li>
</ul>

<h3> 관련 사항들 </h3>
<ul>
  <li>knox 사용</li>
  <li>user 모델 - 상속하여 사용 (AbstractUser)</li>
</ul>
  
<strong>죄송합니다.</strong>
 



