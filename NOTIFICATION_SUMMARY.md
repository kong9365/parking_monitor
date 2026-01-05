# 🔊 Google Home 안내방송 기능 구현 완료 보고서

## ✅ 구현 완료 내역

### 1. 새로운 모듈 개발 ✅

#### `google_assistant.py`
- **GoogleAssistantBroadcaster**: Google Assistant SDK를 사용한 방송
  - OAuth 인증 처리
  - 토큰 자동 갱신
  - 입차/출차 안내방송 메서드
  
- **GoogleHomeCastBroadcaster**: pychromecast를 사용한 방송 (권장)
  - Chromecast 기기 자동 검색
  - gTTS를 사용한 한국어 음성 생성
  - 입차/출차 안내방송 메서드

#### `change_detector.py`
- 새로운 입차 감지
- 새로운 출차 감지
- 데이터베이스와 비교하여 변경사항 추출
- 입차/출차 정보 추출 및 포맷팅

#### `notification_manager.py`
- 변경 감지 및 알림 통합 관리
- 방송기 초기화 (Assistant 또는 Cast)
- 입차/출차 알림 자동 전송
- 통계 정보 제공

#### `main_with_notification.py`
- 알림 기능이 통합된 메인 프로그램
- 명령줄 옵션:
  - `--no-notification`: 알림 비활성화
  - `--broadcaster [assistant|cast]`: 방송 타입 선택

### 2. 데이터베이스 개선 ✅

`database.py`에 추가된 메서드:
- `get_records_by_car_and_entry()`: 차량번호와 입차시간으로 조회
- 출차 정보 업데이트 감지 지원

### 3. 설정 파일 업데이트 ✅

#### `config.py`
```python
GOOGLE_HOME_DEVICE_NAME = os.getenv('GOOGLE_HOME_DEVICE_NAME', 'Living Room')
GOOGLE_BROADCASTER_TYPE = os.getenv('GOOGLE_BROADCASTER_TYPE', 'cast')
```

#### `.env` (예시)
```env
GOOGLE_HOME_DEVICE_NAME=Living Room
GOOGLE_BROADCASTER_TYPE=cast
```

### 4. 의존성 추가 ✅

`requirements.txt`에 추가:
```
google-auth==2.27.0
google-auth-oauthlib==1.2.0
google-auth-httplib2==0.2.0
google-api-python-client==2.116.0
pychromecast==13.1.0
gtts==2.5.0
```

### 5. GitHub Actions 워크플로우 업데이트 ✅

`.github/workflows/parking_monitor.yml`:
- Google 인증 토큰 설정 단계 추가
- 환경 변수 추가 (GOOGLE_HOME_DEVICE_NAME, GOOGLE_BROADCASTER_TYPE)
- 알림 기능이 포함된 메인 프로그램 실행

### 6. 문서 작성 ✅

- **GOOGLE_HOME_SETUP.md**: 상세한 설정 가이드
- **README.md**: 알림 기능 설명 추가
- **NOTIFICATION_SUMMARY.md**: 이 문서

## 📊 프로젝트 구조 (업데이트)

```
parking_monitor/
├── .github/
│   └── workflows/
│       └── parking_monitor.yml          # ✅ 업데이트됨
├── src/
│   ├── main.py                          # 기본 프로그램 (알림 없음)
│   ├── main_with_notification.py       # 🆕 알림 기능 포함
│   ├── parking_scraper.py               # 웹 스크래핑
│   ├── database.py                      # ✅ 업데이트됨
│   ├── logger.py                        # 로깅
│   ├── config.py                        # ✅ 업데이트됨
│   ├── google_assistant.py              # 🆕 Google Home 방송
│   ├── change_detector.py               # 🆕 변경 감지
│   ├── notification_manager.py          # 🆕 알림 관리
│   └── test_connection.py               # 연결 테스트
├── data/
│   ├── parking_records.db               # 데이터베이스
│   └── token.json                       # Google OAuth 토큰 (생성 필요)
├── logs/                                # 로그 파일
├── client_secret.json                   # ✅ OAuth 클라이언트 (적용됨)
├── .env                                 # ✅ 업데이트됨
├── requirements.txt                     # ✅ 업데이트됨
├── README.md                            # ✅ 업데이트됨
├── GOOGLE_HOME_SETUP.md                 # 🆕 Google Home 설정 가이드
└── NOTIFICATION_SUMMARY.md              # 🆕 이 문서
```

## 🎯 안내방송 시나리오

### 입차 시
```
"차량번호 106누4166, 이소영님이 후문 입구로 입차하셨습니다."
```

### 출차 시
```
"차량번호 39가5514, 박재홍님이 후문 출구2로 출차하셨습니다."
```

### ❌ 제외된 기능
- 미출차 경고 (사용자 요청에 따라 제외)

## 🚀 사용 방법

### 로컬 실행

#### 1. 알림 기능 포함 (Chromecast)
```bash
cd src
python main_with_notification.py --broadcaster cast
```

#### 2. 알림 기능 포함 (Google Assistant SDK)
```bash
cd src
python main_with_notification.py --broadcaster assistant
```

#### 3. 알림 없이 실행
```bash
cd src
python main_with_notification.py --no-notification
```

또는

```bash
cd src
python main.py
```

### GitHub Actions 실행

1. **GitHub Secrets 설정** (필수)
   - `PARKING_USER_ID`: 01045429365
   - `PARKING_PASSWORD`: woghd9365.
   - `PARKING_URL`: http://gdjepgcapt3.realparking.net:9080/
   - `GOOGLE_HOME_DEVICE_NAME`: Living Room
   - `GOOGLE_BROADCASTER_TYPE`: cast 또는 assistant
   - `GOOGLE_TOKEN_JSON`: OAuth 토큰 JSON (Assistant SDK 사용 시)

2. **자동 실행**
   - 하루 3회 자동 실행 (오전 9시, 오후 12시, 오후 6시 KST)

3. **수동 실행**
   - Actions 탭 > Parking Monitor > Run workflow

## 🔧 설정 가이드

### Chromecast 방식 (권장)

**장점:**
- 설정이 간단
- 안정적
- API 제한 없음

**단점:**
- 로컬 네트워크에서만 작동
- GitHub Actions에서 사용 불가

**설정:**
```env
GOOGLE_HOME_DEVICE_NAME=Living Room
GOOGLE_BROADCASTER_TYPE=cast
```

### Google Assistant SDK 방식

**장점:**
- 원격에서도 작동 가능
- GitHub Actions에서 사용 가능

**단점:**
- 설정이 복잡
- API 할당량 제한 (하루 500회)

**설정:**
1. Google Cloud Console에서 Google Assistant API 활성화
2. 기기 모델 등록
3. OAuth 토큰 생성
4. GitHub Secrets에 토큰 저장

자세한 내용은 [GOOGLE_HOME_SETUP.md](GOOGLE_HOME_SETUP.md) 참고

## 📈 실행 결과 예시

```
[INFO] ==================================================
[INFO] Real Parking 입출차 모니터링 시스템 시작
[INFO] ==================================================
[INFO] 알림 기능 활성화 (방송 타입: cast)
[SUCCESS] 기기 연결 완료: Living Room
[SUCCESS] 로그인 성공
[INFO] 입출차 조회 페이지 이동 완료
[INFO] 오늘의 입출차 데이터 조회 중...
[SUCCESS] 입출차 데이터 2건 조회 완료

====================================================================================================
총 2건의 입출차 기록
====================================================================================================

[1] 106누4166
  이름: 이소영
  구분: 방문차량
  연락처: 01066289203
  입차: 후문 입구 - 2026/01/05 09:57:08
  출차: 미출차
  상태: 2시간 29분 이상 (미출차)
  비고: 친목

[2] 39가5514
  이름: 박재홍
  구분: 세대차량
  연락처: 01045429365
  입차: 후문 입구 - 2026/01/04 17:57:01
  출차: 후문 출구2 - 2026/01/05 08:09:22
  상태: 14시간 12분 이상 (출차)

====================================================================================================

[INFO] 변경 감지 및 알림 전송 중...
[INFO] 새로운 입차 감지: 106누4166 - 2026/01/05 09:57:08
[INFO] 입차 알림 전송: 106누4166 - 이소영
[SUCCESS] 음성 재생 완료: 차량번호 106누4166, 이소영님이 후문 입구로 입차하셨습니다.
[INFO] 변경 감지 완료 - 입차: 1건, 출차: 0건
[SUCCESS] 알림 처리 완료 - 입차: 1건, 출차: 0건, 알림: 1건

[알림 처리 결과]
  새로운 입차: 1건
  새로운 출차: 0건
  전송된 알림: 1건

[SUCCESS] 데이터베이스에 1건의 새 기록 저장 완료

[데이터베이스 통계]
  전체 기록: 8건
  오늘 기록: 2건
  미출차: 7건

[SUCCESS] 프로그램 정상 종료
```

## 🐛 문제 해결

### "기기를 찾을 수 없습니다"
- Google Home과 컴퓨터가 같은 Wi-Fi에 연결되어 있는지 확인
- 기기 이름을 정확히 입력했는지 확인
- 방화벽에서 mDNS (포트 5353) 허용

### "인증 실패"
- `client_secret.json` 파일 확인
- Google Cloud Console에서 OAuth 클라이언트 상태 확인
- `data/token.json` 삭제 후 재인증

### "방송이 들리지 않음"
- Google Home 볼륨 확인
- 네트워크 연결 상태 확인
- Google Home이 다른 작업 중인지 확인

## 🔐 보안 주의사항

- `client_secret.json`: Git에 커밋하지 마세요
- `token.json`: GitHub Secrets로 관리
- OAuth 토큰은 주기적으로 자동 갱신됨

## 📚 참고 문서

- [GOOGLE_HOME_SETUP.md](GOOGLE_HOME_SETUP.md) - 상세한 설정 가이드
- [README.md](README.md) - 프로젝트 전체 설명
- [GITHUB_SETUP.md](GITHUB_SETUP.md) - GitHub 설정 가이드

## ✨ 완료 요약

### 구현된 기능
✅ Google Home 안내방송 (입차/출차)  
✅ 변경 감지 시스템  
✅ 두 가지 방송 방법 지원 (Chromecast, Assistant SDK)  
✅ GitHub Actions 통합  
✅ 상세한 설정 가이드  

### 제외된 기능
❌ 미출차 경고 (사용자 요청)

---

**프로젝트 완료일**: 2026-01-05  
**버전**: 2.0.0  
**상태**: ✅ 완료 (알림 기능 포함)

