# 🔧 GitHub 설정 가이드

## 1. GitHub 저장소 생성

1. GitHub에 로그인
2. 새 저장소 생성 (예: `parking-monitor`)
3. Private 또는 Public 선택

## 2. Secrets 설정

GitHub Actions에서 사용할 환경 변수를 설정합니다.

### 설정 방법

1. 저장소 페이지에서 `Settings` 클릭
2. 왼쪽 메뉴에서 `Secrets and variables` > `Actions` 클릭
3. `New repository secret` 클릭
4. 다음 3개의 Secret 추가:

#### PARKING_USER_ID
- Name: `PARKING_USER_ID`
- Value: `01045429365`

#### PARKING_PASSWORD
- Name: `PARKING_PASSWORD`
- Value: `woghd9365.`

#### PARKING_URL
- Name: `PARKING_URL`
- Value: `http://gdjepgcapt3.realparking.net:9080/`

## 3. 저장소에 코드 업로드

```bash
# Git 초기화
git init

# 원격 저장소 추가
git remote add origin https://github.com/YOUR_USERNAME/parking-monitor.git

# 파일 추가
git add .

# 커밋
git commit -m "Initial commit: Parking monitor system"

# 푸시
git branch -M main
git push -u origin main
```

## 4. GitHub Actions 실행 스케줄

워크플로우는 다음 시간에 자동 실행됩니다 (KST 기준):

- 오전 9시
- 오후 12시
- 오후 6시

### 수동 실행

1. 저장소 페이지에서 `Actions` 탭 클릭
2. 왼쪽에서 `Parking Monitor` 워크플로우 선택
3. `Run workflow` 버튼 클릭

## 5. 실행 결과 확인

### 성공 시

- 데이터베이스 파일(`data/parking_records.db`)이 자동으로 커밋됨
- Actions 탭에서 초록색 체크마크 표시

### 실패 시

- Actions 탭에서 빨간색 X 표시
- 로그 파일이 Artifacts로 업로드됨
- 로그 다운로드하여 오류 확인 가능

## 6. 데이터 확인

### 방법 1: 저장소에서 직접 확인

```bash
git pull
sqlite3 data/parking_records.db "SELECT * FROM parking_records ORDER BY entry_time DESC LIMIT 10;"
```

### 방법 2: GitHub에서 파일 다운로드

1. 저장소에서 `data/parking_records.db` 파일 클릭
2. `Download` 버튼 클릭
3. SQLite 뷰어로 열기

## 7. 알림 설정 (선택사항)

### 이메일 알림

GitHub 계정 설정에서 Actions 실패 시 이메일 알림 활성화:

1. GitHub 프로필 > `Settings`
2. `Notifications` > `Actions`
3. `Send notifications for failed workflows` 체크

### Slack 알림 (선택사항)

워크플로우 파일에 Slack 알림 단계 추가:

```yaml
- name: Slack 알림
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'Parking Monitor 실행 결과'
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## 8. 문제 해결

### Actions가 실행되지 않음

- Secrets가 올바르게 설정되었는지 확인
- 저장소의 Actions 탭이 활성화되어 있는지 확인

### 로그인 실패

- Secrets의 비밀번호에 점(.)이 포함되어 있는지 확인
- 웹사이트 접속 가능 여부 확인

### 데이터베이스 커밋 실패

- 저장소의 Write 권한이 있는지 확인
- `.gitignore`에서 `data/parking_records.db`가 제외되어 있는지 확인

## 9. 보안 주의사항

⚠️ **중요**: 
- `.env` 파일은 절대 Git에 커밋하지 마세요
- Secrets는 GitHub에서만 설정하세요
- 로그인 정보가 포함된 파일은 `.gitignore`에 추가하세요

## 10. 비용 관련

- GitHub Actions는 Public 저장소에서 무료입니다
- Private 저장소는 월 2,000분 무료 (이후 유료)
- 현재 워크플로우는 실행당 약 2-3분 소요
- 하루 3회 실행 시 월 약 180-270분 사용 (무료 범위 내)

