# 📊 Real Parking 입출차 모니터링 시스템 - 프로젝트 요약

## 🎯 프로젝트 목표

Real Parking 웹사이트에서 입출차 정보를 자동으로 수집하고 데이터베이스에 저장하는 시스템 구축

## ✅ 완료된 기능

### 1. 웹 스크래핑 모듈 (`parking_scraper.py`)
- ✅ Playwright를 사용한 브라우저 자동화
- ✅ Real Parking 자동 로그인
- ✅ 입출차 데이터 수집
- ✅ 날짜별 데이터 조회
- ✅ 최근 N일 데이터 조회

### 2. 데이터베이스 모듈 (`database.py`)
- ✅ SQLite 데이터베이스 자동 생성
- ✅ 입출차 기록 저장
- ✅ 중복 데이터 자동 필터링
- ✅ 날짜별 조회
- ✅ 통계 정보 제공

### 3. 로깅 시스템 (`logger.py`)
- ✅ 구조화된 JSON 로깅
- ✅ 카테고리별 로그 분리 (SYSTEM, SCRAPING, DATABASE)
- ✅ 날짜별 로그 파일 자동 생성
- ✅ 콘솔 및 파일 동시 출력

### 4. 설정 관리 (`config.py`)
- ✅ 환경 변수 관리
- ✅ 디렉토리 자동 생성
- ✅ 설정값 중앙 관리

### 5. 메인 프로그램 (`main.py`)
- ✅ 전체 프로세스 통합 실행
- ✅ 오늘 데이터 자동 수집
- ✅ 데이터베이스 저장
- ✅ 통계 정보 출력

### 6. 테스트 도구 (`test_connection.py`)
- ✅ 연결 테스트
- ✅ 로그인 테스트
- ✅ 데이터 조회 테스트

### 7. GitHub Actions 워크플로우
- ✅ 자동 실행 스케줄 (하루 3회)
- ✅ 수동 실행 가능
- ✅ 데이터베이스 자동 커밋
- ✅ 실패 시 로그 업로드

## 📁 프로젝트 구조

```
parking_monitor/
├── .github/
│   └── workflows/
│       └── parking_monitor.yml    # GitHub Actions 워크플로우
├── src/
│   ├── main.py                    # 메인 실행 파일
│   ├── parking_scraper.py         # 웹 스크래핑 모듈
│   ├── database.py                # 데이터베이스 관리
│   ├── logger.py                  # 로깅 시스템
│   ├── config.py                  # 설정 관리
│   └── test_connection.py         # 연결 테스트
├── data/
│   └── parking_records.db         # SQLite 데이터베이스
├── logs/
│   ├── SYSTEM/                    # 시스템 로그
│   ├── SCRAPING/                  # 스크래핑 로그
│   └── DATABASE/                  # 데이터베이스 로그
├── .env                           # 환경 변수 (로그인 정보)
├── .gitignore                     # Git 제외 파일
├── requirements.txt               # Python 의존성
├── README.md                      # 프로젝트 설명
├── SETUP.md                       # 설치 가이드
├── GITHUB_SETUP.md                # GitHub 설정 가이드
└── PROJECT_SUMMARY.md             # 프로젝트 요약 (이 파일)
```

## 🔧 기술 스택

- **언어**: Python 3.11+
- **웹 스크래핑**: Playwright
- **데이터베이스**: SQLite3
- **환경 변수 관리**: python-dotenv
- **CI/CD**: GitHub Actions

## 📊 데이터베이스 스키마

```sql
CREATE TABLE parking_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_number TEXT NOT NULL,           -- 차량번호
    name TEXT,                          -- 고객명
    type TEXT,                          -- 고객구분
    phone TEXT,                         -- 연락처
    entry_location TEXT,                -- 입차 위치
    entry_time TEXT NOT NULL,           -- 입차 시간
    exit_location TEXT,                 -- 출차 위치
    exit_time TEXT,                     -- 출차 시간
    status TEXT,                        -- 출차 여부
    note TEXT,                          -- 비고
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(car_number, entry_time)
);
```

## 🚀 실행 방법

### 로컬 실행

```bash
cd src
python main.py
```

### GitHub Actions 실행

1. GitHub Secrets 설정
2. 워크플로우 자동 실행 (하루 3회)
3. 또는 수동 실행

## 📈 실행 결과 예시

```
==================================================
Real Parking 입출차 모니터링 시스템 시작
==================================================

[INFO] 데이터베이스 초기화 완료
[INFO] 브라우저 시작 완료
[SUCCESS] 로그인 성공
[INFO] 입출차 조회 페이지 이동 완료
[SUCCESS] 입출차 데이터 2건 조회 완료

====================================================================================================
총 2건의 입출차 기록
====================================================================================================

[1] 106누4166
  이름: 이소영
  구분: 방문차량
  연락처: 01066289203
  입차: 후문_입구 - 2026/01/05 09:57:08
  출차: 미출차
  상태: 2시간 29분 이상 (미출차)
  비고: 친목

[2] 39가5514
  이름: 박재홍
  구분: 세대차량
  연락처: 01045429365
  입차: 후문_입구 - 2026/01/04 17:57:01
  출차: 후문_출구2 - 2026/01/05 08:09:22
  상태: 14시간 12분 이상 (출차)

====================================================================================================

[SUCCESS] 데이터베이스에 0건의 새 기록 저장 완료

[데이터베이스 통계]
  전체 기록: 7건
  오늘 기록: 1건
  미출차: 6건

[SUCCESS] 프로그램 정상 종료
```

## 🔐 보안

- ✅ 로그인 정보는 환경 변수로 관리
- ✅ `.env` 파일은 Git에서 제외
- ✅ GitHub Secrets 사용
- ✅ 민감한 정보는 로그에 기록하지 않음

## 📝 로그 형식

```json
{
  "timestamp": "2026-01-05T12:00:00.000000",
  "level": "INFO",
  "category": "SYSTEM",
  "message": "프로그램 시작",
  "data": {}
}
```

## 🎯 향후 계획

### Phase 1: 알림 기능 (예정)
- [ ] 갤럭시 홈 미니 연동
- [ ] 실시간 입출차 알림
- [ ] 음성 안내 기능

### Phase 2: 고급 기능 (예정)
- [ ] 웹 대시보드
- [ ] 통계 분석
- [ ] 이메일/SMS 알림
- [ ] 특정 차량 감지 알림

### Phase 3: 최적화 (예정)
- [ ] 실시간 모니터링
- [ ] WebSocket 연결
- [ ] 성능 최적화

## 📞 문의 및 지원

- GitHub Issues를 통해 버그 리포트 및 기능 요청
- Pull Request 환영

## 📄 라이선스

MIT License

---

**프로젝트 완료일**: 2026-01-05  
**버전**: 1.0.0  
**상태**: ✅ 완료 (알림 기능 제외)

