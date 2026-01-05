# 🚗 Real Parking 입출차 모니터링 시스템

Real Parking 웹사이트에서 입출차 정보를 자동으로 수집하고 데이터베이스에 저장하는 시스템입니다.

## 📋 주요 기능

- ✅ Real Parking 웹사이트 자동 로그인
- ✅ 입출차 데이터 자동 수집
- ✅ SQLite 데이터베이스 저장
- ✅ 구조화된 JSON 로깅
- ✅ 날짜별 데이터 조회
- ✅ 통계 정보 제공
- ✅ **Google Home 안내방송** (입차/출차 알림)
- ✅ 변경 감지 및 실시간 알림

## 🏗️ 프로젝트 구조

```
parking_monitor/
├── src/
│   ├── main.py              # 메인 실행 파일
│   ├── parking_scraper.py   # 웹 스크래핑 모듈
│   ├── database.py          # 데이터베이스 관리 모듈
│   ├── logger.py            # 로깅 시스템
│   └── config.py            # 설정 파일
├── data/
│   └── parking_records.db   # SQLite 데이터베이스 (자동 생성)
├── logs/
│   ├── SYSTEM/              # 시스템 로그
│   ├── SCRAPING/            # 스크래핑 로그
│   └── DATABASE/            # 데이터베이스 로그
├── .env                     # 환경 변수 (로그인 정보)
├── .gitignore
├── requirements.txt
└── README.md
```

## 🚀 설치 및 실행

### 1. 필수 요구사항

- Python 3.8 이상
- pip
- Google Home (갤럭시 홈 미니) - 알림 기능 사용 시

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. Playwright 브라우저 설치

```bash
playwright install chromium
```

### 4. 환경 변수 설정

`.env` 파일에 Real Parking 로그인 정보를 입력합니다:

```env
# Real Parking 로그인 정보
PARKING_USER_ID=01045429365
PARKING_PASSWORD=woghd9365.
PARKING_URL=http://gdjepgcapt3.realparking.net:9080/

# Google Home 설정 (알림 기능 사용 시)
GOOGLE_HOME_DEVICE_NAME=Living Room
GOOGLE_BROADCASTER_TYPE=cast
```

### 5. Google Home 설정 (선택사항)

알림 기능을 사용하려면 [GOOGLE_HOME_SETUP.md](GOOGLE_HOME_SETUP.md)를 참고하세요.

### 6. 프로그램 실행

**알림 기능 포함:**
```bash
cd src
python main_with_notification.py
```

**알림 없이 실행:**
```bash
cd src
python main.py
```

## 📊 데이터베이스 구조

### parking_records 테이블

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| id | INTEGER | 기본 키 (자동 증가) |
| car_number | TEXT | 차량번호 |
| name | TEXT | 고객명 |
| type | TEXT | 고객구분 (방문차량, 세대차량 등) |
| phone | TEXT | 연락처 |
| entry_location | TEXT | 입차 위치 |
| entry_time | TEXT | 입차 시간 |
| exit_location | TEXT | 출차 위치 |
| exit_time | TEXT | 출차 시간 |
| status | TEXT | 출차 여부 상태 |
| note | TEXT | 비고 |
| created_at | TEXT | 레코드 생성 시간 |

## 📝 로그 시스템

로그는 카테고리별로 분리되어 JSON 형식으로 저장됩니다:

- **SYSTEM**: 시스템 전반적인 로그
- **SCRAPING**: 웹 스크래핑 관련 로그
- **DATABASE**: 데이터베이스 작업 로그

각 로그 파일은 `logs/{CATEGORY}/{YYYYMMDD}.json` 형식으로 저장됩니다.

### 로그 엔트리 형식

```json
{
  "timestamp": "2026-01-05T12:00:00.000000",
  "level": "INFO",
  "category": "SYSTEM",
  "message": "프로그램 시작",
  "data": {}
}
```

## 🔧 주요 모듈 설명

### parking_scraper.py

Playwright를 사용하여 Real Parking 웹사이트에서 데이터를 수집합니다.

**주요 메서드:**
- `login()`: 로그인 수행
- `navigate_to_inout_list()`: 입출차 조회 페이지 이동
- `get_parking_data(start_date, end_date)`: 특정 기간의 데이터 조회
- `get_today_data()`: 오늘 데이터 조회
- `get_recent_days_data(days)`: 최근 N일 데이터 조회

### database.py

SQLite 데이터베이스를 관리합니다.

**주요 메서드:**
- `insert_record(record)`: 단일 기록 추가
- `insert_records(records)`: 여러 기록 추가
- `get_all_records()`: 모든 기록 조회
- `get_records_by_date(date)`: 날짜별 기록 조회
- `get_recent_records(limit)`: 최근 기록 조회
- `get_statistics()`: 통계 정보 조회

### logger.py

구조화된 JSON 로깅을 제공합니다.

**로그 레벨:**
- `info()`: 정보 로그
- `warning()`: 경고 로그
- `error()`: 에러 로그
- `success()`: 성공 로그

## 🔐 보안

- `.env` 파일은 `.gitignore`에 포함되어 있어 Git에 커밋되지 않습니다
- 로그인 정보는 환경 변수로 관리됩니다
- 데이터베이스 파일도 Git에서 제외됩니다

## 🔊 안내방송 기능

### 세대 차량 입차 알림
```
"세대 차량 39가5514가 후문 입구로 입차하였습니다."
```

### 방문차량 입차 알림
```
"방문차량 106누4166, 이소영님이 후문 입구로 입차하셨습니다."
```

### 세대 차량 출차 알림
```
"세대 차량 39가5514가 후문 출구2로 출차하였습니다."
```

### 방문차량 출차 알림
```
"방문차량 106누4166, 이소영님이 후문 출구2로 출차하셨습니다."
```

### 세대 차량 설정

`src/config.py` 파일에서 세대 차량 번호를 설정할 수 있습니다:

```python
# 세대 차량 번호 리스트
RESIDENT_CARS = [
    '39가5514',
    '64우0364'
]
```

### 지원하는 방송 방법
- **Chromecast (pychromecast)**: 로컬 네트워크에서 작동 (권장)
- **Google Assistant SDK**: 원격에서도 작동 가능

자세한 설정 방법은 [GOOGLE_HOME_SETUP.md](GOOGLE_HOME_SETUP.md)를 참고하세요.

## 📅 향후 계획

- [x] GitHub Actions를 통한 자동 실행
- [x] 갤럭시 홈 미니 알림 기능 추가
- [ ] 실시간 모니터링 기능
- [ ] 웹 대시보드 추가
- [ ] 이메일/SMS 알림 기능

## 🐛 문제 해결

### 로그인 실패

- `.env` 파일의 로그인 정보가 정확한지 확인하세요
- 비밀번호에 특수문자(.)가 포함되어 있는지 확인하세요

### Playwright 오류

```bash
# Playwright 재설치
playwright install chromium
```

### 데이터베이스 오류

- `data` 폴더에 쓰기 권한이 있는지 확인하세요
- 데이터베이스 파일이 손상된 경우 삭제 후 재생성하세요

## 📄 라이선스

MIT License

## 👤 작성자

입출차 모니터링 시스템 개발자

## 📞 문의

문제가 발생하거나 기능 요청이 있으시면 이슈를 등록해주세요.

