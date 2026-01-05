# 🔊 Google Home 안내방송 설정 가이드

## 📋 개요

이 가이드는 Google Home (갤럭시 홈 미니)을 통해 입출차 안내방송을 설정하는 방법을 설명합니다.

## 🎯 지원하는 방송 방법

### 방법 1: Chromecast (pychromecast) - 권장 ⭐
- **장점**: 설정이 간단하고 안정적
- **단점**: 로컬 네트워크에서만 작동
- **적합한 경우**: 집에서 실행하는 경우

### 방법 2: Google Assistant SDK
- **장점**: 원격에서도 작동 가능
- **단점**: 설정이 복잡하고 API 제한 있음
- **적합한 경우**: GitHub Actions에서 실행하는 경우

## 🚀 방법 1: Chromecast 설정 (권장)

### 1. Google Home 기기 이름 확인

Google Home 앱에서 기기 이름을 확인합니다:
1. Google Home 앱 열기
2. 기기 선택
3. 설정(⚙️) > 기기 정보 > 이름 확인

### 2. 환경 변수 설정

`.env` 파일에 추가:
```env
GOOGLE_HOME_DEVICE_NAME=Living Room
GOOGLE_BROADCASTER_TYPE=cast
```

### 3. 로컬 테스트

```bash
cd src
python main_with_notification.py --broadcaster cast
```

### 4. 문제 해결

**기기를 찾을 수 없는 경우:**
- Google Home과 컴퓨터가 같은 Wi-Fi 네트워크에 연결되어 있는지 확인
- 방화벽에서 mDNS (포트 5353) 허용
- 기기 이름을 정확히 입력했는지 확인

## 🌐 방법 2: Google Assistant SDK 설정

### 1. Google Cloud Console 설정

#### 1.1 프로젝트 생성 (이미 완료됨 ✅)
- 프로젝트 ID: `parking-notifier-483403`
- OAuth 클라이언트 ID: 이미 생성됨

#### 1.2 Google Assistant API 활성화

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 프로젝트 선택: `parking-notifier-483403`
3. "API 및 서비스" > "라이브러리" 클릭
4. "Google Assistant API" 검색
5. "사용 설정" 클릭

### 2. 기기 모델 등록

1. [Actions Console](https://console.actions.google.com/) 접속
2. 프로젝트 선택
3. "Device registration" 클릭
4. "Register Model" 클릭
5. 다음 정보 입력:
   - Product name: `Parking Monitor`
   - Manufacturer name: `Your Name`
   - Device type: `Speaker`
6. "Save" 클릭
7. **Device Model ID** 저장 (예: `parking-monitor-abc123`)

### 3. OAuth 인증 토큰 생성

#### 로컬에서 토큰 생성:

```bash
cd src
python -c "
from google_assistant import GoogleAssistantBroadcaster
broadcaster = GoogleAssistantBroadcaster()
broadcaster.authenticate()
print('인증 완료! token.json 파일이 생성되었습니다.')
"
```

브라우저가 열리면:
1. Google 계정 로그인
2. 권한 허용
3. `data/token.json` 파일 생성 확인

### 4. GitHub Secrets 설정

#### 4.1 토큰 JSON 복사

```bash
# Windows
type data\token.json | clip

# Linux/Mac
cat data/token.json | pbcopy
```

#### 4.2 GitHub Secrets 추가

GitHub 저장소 > Settings > Secrets and variables > Actions:

1. **GOOGLE_TOKEN_JSON**
   - Value: 복사한 token.json 내용 전체 붙여넣기

2. **GOOGLE_HOME_DEVICE_NAME**
   - Value: `Living Room` (또는 실제 기기 이름)

3. **GOOGLE_BROADCASTER_TYPE**
   - Value: `assistant` 또는 `cast`

4. **GOOGLE_DEVICE_MODEL_ID** (Assistant SDK 사용 시)
   - Value: 위에서 생성한 Device Model ID

## 🧪 테스트

### 로컬 테스트

```bash
# Chromecast 방식
cd src
python main_with_notification.py --broadcaster cast

# Google Assistant SDK 방식
cd src
python main_with_notification.py --broadcaster assistant
```

### 알림 없이 실행

```bash
cd src
python main_with_notification.py --no-notification
```

## 📊 실행 결과 예시

```
[INFO] Real Parking 입출차 모니터링 시스템 시작
[INFO] 알림 기능 활성화 (방송 타입: cast)
[SUCCESS] 기기 연결 완료: Living Room
[SUCCESS] 로그인 성공
[INFO] 입출차 데이터 조회 시작
[INFO] 새로운 입차 감지: 106누4166 - 2026/01/05 09:57:08
[INFO] 입차 알림 전송: 106누4166 - 이소영
[SUCCESS] 음성 재생 완료: 차량번호 106누4166, 이소영님이 후문 입구로 입차하셨습니다.

[알림 처리 결과]
  새로운 입차: 1건
  새로운 출차: 0건
  전송된 알림: 1건
```

## 🔧 고급 설정

### 음성 속도 조절 (TTS)

`google_assistant.py`에서 수정:

```python
# 느리게
tts = gTTS(text=text, lang='ko', slow=True)

# 빠르게 (기본값)
tts = gTTS(text=text, lang='ko', slow=False)
```

### 볼륨 조절

Google Home 앱에서 기기 볼륨을 미리 설정하거나, 코드에서 조절:

```python
# pychromecast 사용 시
mc = self.device.media_controller
mc.set_volume(0.5)  # 0.0 ~ 1.0
```

### 안내 메시지 커스터마이징

`notification_manager.py`에서 메시지 형식 수정:

```python
# 입차 메시지
message = f"{name}님이 {location}로 입차하셨습니다. 차량번호는 {car_number}입니다."

# 출차 메시지
message = f"{name}님이 {location}로 출차하셨습니다."
```

## ⚠️ 주의사항

### Chromecast 방식
1. **네트워크**: Google Home과 실행 환경이 같은 네트워크에 있어야 함
2. **방화벽**: mDNS 포트(5353) 허용 필요
3. **GitHub Actions**: 원격 서버에서는 작동 안 함

### Google Assistant SDK 방식
1. **API 할당량**: 하루 500회 제한 (무료)
2. **인증 토큰**: 주기적으로 갱신 필요 (자동 갱신 구현됨)
3. **개인 사용**: 상업적 사용 불가

## 🐛 문제 해결

### "기기를 찾을 수 없습니다"

```bash
# 네트워크 내 Chromecast 기기 검색
python -c "
import pychromecast
chromecasts, browser = pychromecast.get_chromecasts()
for cc in chromecasts:
    print(f'기기 이름: {cc.name}')
"
```

### "인증 실패"

1. `client_secret.json` 파일 확인
2. Google Cloud Console에서 OAuth 클라이언트 상태 확인
3. `data/token.json` 삭제 후 재인증

### "방송이 들리지 않음"

1. Google Home 볼륨 확인
2. Google Home이 다른 작업 중인지 확인
3. 네트워크 연결 상태 확인

## 📱 모바일에서 테스트

Google Home 앱에서 직접 테스트:
1. Google Home 앱 열기
2. 기기 선택
3. "테스트" 버튼으로 TTS 테스트

## 🔐 보안

- `client_secret.json`: Git에 커밋하지 마세요 (`.gitignore`에 포함됨)
- `token.json`: GitHub Secrets로 관리
- OAuth 토큰은 주기적으로 갱신됨

## 📚 참고 자료

- [Google Assistant SDK 문서](https://developers.google.com/assistant/sdk)
- [pychromecast 문서](https://github.com/home-assistant-libs/pychromecast)
- [gTTS 문서](https://gtts.readthedocs.io/)

## 💡 추천 설정

**집에서 실행하는 경우:**
```env
GOOGLE_BROADCASTER_TYPE=cast
GOOGLE_HOME_DEVICE_NAME=Living Room
```

**GitHub Actions에서 실행하는 경우:**
```env
GOOGLE_BROADCASTER_TYPE=assistant
```
(단, Chromecast 방식은 원격에서 작동하지 않으므로 Assistant SDK 사용 필요)

---

**설정 완료 후 테스트를 진행하세요!** 🎉

