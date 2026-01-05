# 🚀 설치 및 실행 가이드

## 1. 저장소 클론

```bash
git clone <repository-url>
cd parking_monitor
```

## 2. Python 가상환경 생성 (선택사항)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

## 3. 의존성 설치

```bash
pip install -r requirements.txt
```

## 4. Playwright 브라우저 설치

```bash
playwright install chromium
```

## 5. 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 입력합니다:

```env
PARKING_USER_ID=01045429365
PARKING_PASSWORD=woghd9365.
PARKING_URL=http://gdjepgcapt3.realparking.net:9080/
```

## 6. 연결 테스트

```bash
cd src
python test_connection.py
```

## 7. 프로그램 실행

```bash
cd src
python main.py
```

## 📊 실행 결과

프로그램이 성공적으로 실행되면:

1. Real Parking 웹사이트에 자동 로그인
2. 오늘의 입출차 데이터 조회
3. 데이터베이스에 저장
4. 콘솔에 결과 출력
5. 로그 파일 생성 (`logs/` 폴더)

## 🔍 로그 확인

```bash
# 시스템 로그
cat logs/SYSTEM/20260105.json

# 스크래핑 로그
cat logs/SCRAPING/20260105.json

# 데이터베이스 로그
cat logs/DATABASE/20260105.json
```

## 🗄️ 데이터베이스 확인

```bash
# SQLite 데이터베이스 열기
sqlite3 data/parking_records.db

# 테이블 확인
.tables

# 데이터 조회
SELECT * FROM parking_records;
```

## ⚙️ 설정 변경

`src/config.py` 파일에서 다음 설정을 변경할 수 있습니다:

- `HEADLESS`: 브라우저 표시 여부 (True: 숨김, False: 표시)
- `TIMEOUT`: 타임아웃 시간 (밀리초)
- `DATE_FORMAT`: 날짜 형식
- `DATETIME_FORMAT`: 날짜시간 형식

## 🐛 문제 해결

### 로그인 실패

1. `.env` 파일의 로그인 정보 확인
2. 비밀번호에 점(.)이 포함되어 있는지 확인
3. `HEADLESS = False`로 설정하여 브라우저 동작 확인

### 데이터 조회 실패

1. 날짜 설정 확인
2. 웹사이트 접속 가능 여부 확인
3. 로그 파일 확인

### Playwright 오류

```bash
# Playwright 재설치
playwright install chromium
```

## 📝 추가 정보

- 프로그램은 중복 데이터를 자동으로 필터링합니다
- 로그는 날짜별로 자동 분류됩니다
- 데이터베이스는 SQLite를 사용하여 별도 설치가 필요 없습니다

