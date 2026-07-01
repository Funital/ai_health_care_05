# Git & HTML 학습 정리

## 1. 팀 프로젝트 시 GitHub 이용 방법

팀 프로젝트에서 GitHub를 사용할 때는 여러 사람이 동시에 코드를
수정하므로, 서로의 작업이 얽히지 않도록 명확한 규칙(Git Flow 등)을
기반으로 협업해야 합니다.

일반적인 협업 흐름은 다음과 같습니다.

## 🎯 GitHub 협업 흐름

``` text
Issue 생성
   ↓
브랜치 생성
   ↓
기능 개발
   ↓
git add
   ↓
git commit
   ↓
git push
   ↓
Pull Request(PR)
   ↓
Code Review
   ↓
Merge
```

## 1️⃣ git clone vs git remote add

|    | `git clone` | `git remote add` |
|------|-------------|------------------|
| **목적** | 원격 저장소를 그대로 복제 | 기존 저장소에 원격 저장소 등록 |
| **초기화** | 자동 (`git init` 포함) | 기존 저장소 사용 |
| **origin 등록** | 자동 | 직접 지정 |
| **사용 시점** | 프로젝트를 처음 받을 때 | 이미 작업 중인 저장소를 원격 저장소와 연결할 때 |

💡 **정리:** Clone=새 프로젝트 시작 / Remote Add=주소록 추가

------------------------------------------------------------------------

## 2️⃣ 자주 사용하는 Git 명령어

| 명령어 | 역할 |
|--------|------|
| `git status` | 현재 저장소의 상태(변경된 파일, 스테이징 여부 등)를 확인 |
| `git fetch` | 원격 저장소의 최신 변경 사항만 가져오고 병합하지 않음 |
| `git merge` | 두 브랜치의 변경 내용을 하나로 병합 |
| `git pull` | `git fetch` + `git merge`를 한 번에 수행 |
| `git add .` | 변경된 모든 파일을 Staging Area에 등록 |
| `git commit -m "메시지"` | 스테이징된 변경 사항을 로컬 저장소에 커밋 |
| `git push origin 브랜치명` | 로컬 커밋을 원격 저장소에 업로드 |

### 협업 순서

``` bash
git switch feature/login
git pull origin develop

# 개발

git add .
git commit -m "Feat: 로그인 기능 구현"
git push origin feature/login
```



## Extra Git 명령어

### `git log --oneline`

커밋 기록을

    커밋해시 커밋메시지

형태로 한 줄씩 간단하게 보여줍니다.

------------------------------------------------------------------------

### `git cherry-pick`

다른 브랜치의 특정 커밋 하나만 가져오는 명령어입니다.

``` bash
git cherry-pick a1b2c3d
```

------------------------------------------------------------------------

## 3️⃣ Local vs Remote

| Local Repository | Remote Repository |
|------------------|-------------------|
| 내 컴퓨터 | GitHub 서버 |
| `git commit`으로 저장 | `git push`로 저장 |
| 혼자 작업 가능 | 팀원들과 협업 및 코드 공유 |
| 인터넷 없이도 작업 가능 | 인터넷 연결이 필요 |

⭐ commit ≠ push

------------------------------------------------------------------------

## 4️⃣ Issue & PR

### Issue

-   버그 관리
-   기능 추가
-   작업 분배

예시

``` text
[Feat] 로그인 API 연동
```

### Pull Request

-   코드 리뷰
-   Merge 요청
-   변경사항 설명

좋은 PR에는 **무엇을**, **왜**, **테스트 방법**을 작성합니다.


> `Closes #12`를 작성하면 PR Merge 시 Issue가 자동 종료됩니다.

------------------------------------------------------------------------

## ⚠️ 자주 하는 실수

-   pull 없이 개발 시작
-   main에서 직접 개발
-   너무 큰 commit
-   의미 없는 commit 메시지("fix", "수정")

추천 commit message 형식

``` text
Feat:
Fix:
Docs:
Refactor:
Style:
Test:
Chore:
```

------------------------------------------------------------------------

# [다음 수업 미리보기] 🌐 HTML 기초

## 기본 구조

``` html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>페이지 제목</title>
</head>
<body>
    <h1>가장 큰 제목</h1>
    <p>본문입니다.<br>줄바꿈</p>
</body>
</html>
```
```

### 태그 설명

  태그                역할
  ------------------- ------------------------------
  `<!DOCTYPE html>`   HTML5 문서 선언
  `<html>`            HTML 문서 전체
  `<head>`            메타데이터(제목, CSS, JS 등)
  `<body>`            실제 화면에 표시되는 내용
  `<h1>~<h6>`         제목 태그
  `<p>`               문단
  `<br>`              줄바꿈

💡 `head`는 브라우저 정보, `body`는 사용자에게 보이는 화면입니다.
