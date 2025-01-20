# 생일 카페 중계 플랫폼 iOS 앱 프로젝트

## 프로젝트 소개
이 프로젝트는 SwiftUI를 사용하여 프론트엔드를 구성하고, Swift를 사용하여 백엔드를 구현하여 앱 애플리케이션을 개발하는 것을 목표로 한다.

X.com 에서 크롤링을 통해 정보를 가져오고 gpt API를 통해 정제 후 mySQL에 데이터를 저장한다. 

Flask API를 사용하여 mySQL에 저장된 데이터를 앱에서 받도록 구현하였다.

해당 Repository는 https://github.com/indextrown/senior-project 에서 담당한 부분을 clone 및 수정하여 재게시하였습니다.

## 사용 및 담당한 기술 및 도구
- **프론트엔드**
    - SwiftUI
- **백엔드**
    - Swift
- **데이터베이스**
    - mySQL
    - SQLAlchemy
- **API**
    - Flask 

## 지원되는 iOS 디바이스
- **기본 계획**
    - iPhone XS Max
    - iPhone 11 Pro
    - iPhone 15 Pro Max
    - iPhone 16 Pro

- **최종 계획**
    - iOS 18을 지원하는 모든 디바이스
    
- **최적화된 디바이스**
    - iPhone 15 Pro

## 앱 화면
<table>
    <tr>
     <td align="center" width="200">
      <img src="./iOS/gif/메인화면.gif" width="200" />
      <p><strong>메인화면</strong></p>
    </td>
     <td align="center" width="200">
      <img src="./iOS/gif/소셜로그인.gif" width="200" />
      <p><strong>소셜 로그인</strong></p>
    </td>
    <td align="center" width="200">
      <img src="./iOS/gif/로그아웃.gif" width="200" />
      <p><strong>로그아웃</strong></p>
    </td>
  </tr>
  <tr>
    <td align="center" width="200">
      <img src="./iOS/gif/게시판-글 검색.gif" width="200" />
      <p><strong>게시판 - 글 검색</strong></p>
    </td>
    <td align="center" width="200">
      <img src="./iOS/gif/게시판-글작성.gif" width="200" />
      <p><strong>게시판 - 글 작성</strong></p>
    </td>
        <td align="center" width="200">
      <img src="./iOS/gif/게시판-제목 검색.gif" width="200" />
      <p><strong>게시판 - 제목 검색</strong></p>
    </td>
  </tr>
  <tr>
    <td align="center" width="200">
      <img src="./iOS/gif/스케줄-확장.gif" width="200" />
      <p><strong>스케줄 - 확장</strong></p>
    </td>
    <td align="center" width="200">
      <img src="./iOS/gif/스케줄-디테일.gif" width="200" />
      <p><strong>스케줄 - 디테일</strong></p>
    </td>
    <td align="center" width="200">
      <img src="./iOS/gif/스케줄-확장-디테일.gif" width="200" />
      <p><strong>스케줄 - 확장 디테일</strong></p>
    </td>
  </tr>
  <tr>
    <td align="center" width="200">
      <img src="./iOS/gif/스케줄-리스트.gif" width="200" />
      <p><strong>스케줄 - 리스트</strong></p>
    </td>
    <td align="center" width="200">
      <img src="./iOS/gif/스케줄-날짜변경.gif" width="200" />
      <p><strong>스케줄 - 날짜 변경</strong></p>
    </td>
  </tr>
  <tr>
    <td align="center" width="200">
      <img src="./iOS/gif/프로필-알람토글.gif" width="200" />
      <p><strong>프로필 - 알람 토글</strong></p>
    </td>
    <td align="center" width="200">
      <img src="./iOS/gif/프로필-내가올린글.gif" width="200" />
      <p><strong>프로필 - 내가 올린 글</strong></p>
    </td>
    <td align="center" width="200">
      <img src="./iOS/gif/프로필-키워드 추가삭제.gif" width="200" />
      <p><strong>프로필 - 키워드 추가/삭제</strong></p>
    </td>
  </tr>
  <tr>
    <td align="center" width="200">
      <img src="./iOS/gif/생일카페-링크.gif" width="200" />
      <p><strong>생일카페 - 링크</strong></p>
    </td>
    <td align="center" width="200">
      <img src="./iOS/gif/생일카페-아티스트 추가.gif" width="200" />
      <p><strong>생일카페 - 아티스트 추가</strong></p>
    </td>
    <td align="center" width="200">
      <img src="./iOS/gif/생일카페-아티스트 삭제.gif" width="200" />
      <p><strong>생일카페 - 아티스트 삭제</strong></p>
    </td>
  </tr>
  <tr>
    <td align="center" width="200">
      <img src="./iOS/gif/생일카페-날짜변경.gif" width="200" />
      <p><strong>생일카페 - 날짜 변경</strong></p>
    </td>
  </tr>
</table>

## API

이 API는 `Content` 키워드를 기준으로 요청 데이터를 구분하며, `Content`의 값에 따라 서로 다른 데이터를 가져올 수 있습니다.  

---

## 1. Content: "bboard" (게시판 데이터)  

게시판 데이터를 조회하거나 게시글을 작성할 때 사용합니다.  

### 📌 전체 게시판 데이터 조회  
```json
{
    "Content": "bboard",
    "all": "_"
}
```
**용도:** 게시판에 등록된 모든 데이터를 조회할 때 사용합니다.  

### 📌 게시글 작성 요청  
```json
{
    "Content": "bboard",
    "write": "_",
    "nickname": "{사용자 닉네임}",
    "title": "{게시글 제목}",
    "content": "{게시글 내용}",
    "post_date": "{yyyy-MM-dd / HH:mm:ss}",
    "artist": "{아티스트 이름}"
}
```
**용도:** 사용자가 새로운 게시글을 작성할 때 사용합니다.  

### 📌 특정 사용자의 게시글 조회  
```json
{
    "Content": "bboard",
    "nickname": "{사용자 닉네임}"
}
```
**용도:** 특정 사용자가 작성한 게시글을 조회할 때 사용합니다.  

---

## 2. Content: "cafe" (생일카페 데이터)  

특정 날짜 범위 내에서 등록된 생일카페 데이터를 조회할 때 사용합니다.  

### 📌 생일카페 데이터 조회  
```json
{
    "Content": "cafe",
    "startDate": "{yyyy-MM-dd}",
    "endDate": "{yyyy-MM-dd}"
}
```
**용도:** 지정한 날짜 범위 사이에 등록된 생일카페 데이터를 가져올 때 사용합니다.  

---

## 3. Content: "image" (이미지 데이터)  

서버에 저장된 특정 이미지 파일을 불러올 때 사용합니다.  

### 📌 이미지 파일 불러오기  
```json
{
    "Content": "image",
    "filename": "{원하는 이미지 파일명}"
}
```
**용도:** 특정 이미지 파일을 서버에서 가져올 때 사용합니다.  

---

## 4. Content: "x" (아이돌 공식 계정 데이터)  

특정 날짜 범위 내에서 아이돌 공식 계정에 작성된 데이터를 조회할 때 사용합니다.  

### 📌 아이돌 공식 계정 데이터 조회  
```json
{
    "Content": "x",
    "startDate": "{yyyy-MM-dd}",
    "endDate": "{yyyy-MM-dd}"
}
```
**용도:** 지정한 날짜 범위 내에서 작성된 아이돌 공식 계정 데이터를 가져올 때 사용합니다.  

---
