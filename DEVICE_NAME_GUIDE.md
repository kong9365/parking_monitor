# Google Home Mini 기기 이름 확인 및 방송 타입 가이드

## 📱 기기 이름 확인 방법

### 방법 1: 스크립트로 자동 검색 (가장 쉬움)

```bash
cd parking_monitor/src
python test_local_broadcast.py --list
```

이 명령어를 실행하면 같은 네트워크에 있는 모든 Chromecast 기기 목록이 표시됩니다:

```
============================================================
사용 가능한 Chromecast 기기 검색 중...
============================================================

✅ 2개의 기기를 찾았습니다:

[1] 거실
    타입: cast
    IP: 192.168.0.100

[2] 침실
    타입: cast
    IP: 192.168.0.101
```

**출력된 `friendly_name`이 바로 기기 이름입니다!**

### 방법 2: Google Home 앱에서 확인

1. 스마트폰에서 **Google Home 앱** 실행
2. 앱 하단의 **"기기"** 탭 클릭
3. Google Home Mini 기기 선택
4. 기기 설정에서 **"기기 정보"** 확인
5. **"기기 이름"** 또는 **"이름"** 항목 확인

### 방법 3: Python 코드로 직접 확인

```python
import pychromecast

# 모든 Chromecast 기기 검색
chromecasts, browser = pychromecast.get_listed_chromecasts()

print("발견된 기기:")
for cast in chromecasts:
    print(f"이름: {cast.device.friendly_name}")
    print(f"IP: {cast.host}")
    print(f"타입: {cast.device.cast_type}")
    print()

browser.stop_discovery()
```

### 방법 4: 네트워크 스캔 도구 사용

- **Windows**: `nmap` 또는 `Advanced IP Scanner` 사용
- **Mac/Linux**: `avahi-browse` 명령어 사용
  ```bash
  avahi-browse -t _googlecast._tcp
  ```

## 🔊 GOOGLE_BROADCASTER_TYPE 종류

프로젝트에서 지원하는 방송 타입은 **2가지**입니다:

### 1. `cast` (Chromecast 방식) - **권장** ⭐

**특징:**
- ✅ 설정이 간단함
- ✅ Google OAuth 인증 불필요
- ✅ 안정적이고 빠름
- ✅ 로컬 네트워크에서 직접 통신
- ✅ gTTS (Google Text-to-Speech) 사용

**사용 방법:**
```bash
# .env 파일에 설정
GOOGLE_BROADCASTER_TYPE=cast

# 또는 명령줄에서
python main_with_notification.py --broadcaster cast
```

**동작 원리:**
1. pychromecast로 같은 네트워크의 Google Home Mini 검색
2. gTTS로 한국어 음성 생성
3. HTTP 서버를 띄워 음성 파일 제공
4. Chromecast 프로토콜로 Google Home Mini에 재생 명령 전송

**장점:**
- 인증 과정이 없어 빠름
- 네트워크만 연결되면 바로 사용 가능
- 실제로 작동함 (검증됨)

**단점:**
- 같은 네트워크에 있어야 함
- 로컬 네트워크에서만 작동

---

### 2. `assistant` (Google Assistant SDK 방식)

**특징:**
- ⚠️ Google OAuth 인증 필요
- ⚠️ 설정이 복잡함
- ⚠️ client_secret.json 파일 필요
- ⚠️ token.json 파일 필요
- ✅ 원격에서도 작동 가능 (이론상)

**사용 방법:**
```bash
# .env 파일에 설정
GOOGLE_BROADCASTER_TYPE=assistant

# 또는 명령줄에서
python main_with_notification.py --broadcaster assistant
```

**동작 원리:**
1. Google OAuth 인증 수행
2. Google Assistant SDK API 사용
3. 실제로는 내부적으로 Chromecast 방식 사용 (현재 구현)

**장점:**
- Google 공식 API 사용
- 원격 접근 가능 (이론상)

**단점:**
- 복잡한 인증 과정
- 설정이 어려움
- 현재 구현은 실제로 Chromecast 방식과 동일하게 작동

---

## 📊 비교표

| 항목 | `cast` | `assistant` |
|------|--------|-------------|
| 설정 난이도 | ⭐ 쉬움 | ⭐⭐⭐ 어려움 |
| 인증 필요 | ❌ 불필요 | ✅ 필요 |
| 네트워크 | 같은 네트워크 필요 | 같은 네트워크 필요 |
| 안정성 | ⭐⭐⭐ 높음 | ⭐⭐ 보통 |
| 속도 | ⭐⭐⭐ 빠름 | ⭐⭐ 보통 |
| 권장도 | ✅ **권장** | ⚠️ 특수한 경우만 |

## 🎯 권장 설정

**대부분의 경우 `cast` 방식을 권장합니다:**

```env
# .env 파일
GOOGLE_BROADCASTER_TYPE=cast
GOOGLE_HOME_DEVICE_NAME=거실
```

## 🔧 설정 예제

### 예제 1: Chromecast 방식 (권장)

```env
# .env 파일
GOOGLE_BROADCASTER_TYPE=cast
GOOGLE_HOME_DEVICE_NAME=거실
```

```bash
# 실행
python src/main_with_notification.py --broadcaster cast
```

### 예제 2: Google Assistant SDK 방식

```env
# .env 파일
GOOGLE_BROADCASTER_TYPE=assistant
GOOGLE_HOME_DEVICE_NAME=거실
```

```bash
# 사전 준비 필요:
# 1. client_secret.json 파일 (프로젝트 루트)
# 2. data/token.json 파일

# 실행
python src/main_with_notification.py --broadcaster assistant
```

## 🧪 테스트 방법

### 기기 이름 확인 후 테스트

```bash
# 1. 기기 목록 확인
cd parking_monitor/src
python test_local_broadcast.py --list

# 2. 확인된 기기 이름으로 테스트
python test_local_broadcast.py --method cast --device "거실" --message "테스트입니다"
```

## 💡 팁

1. **기기 이름은 대소문자를 구분하지 않습니다**
   - "거실" = "거실" (동일)

2. **기기 이름에 공백이 있어도 됩니다**
   - "거실 홈" ✅

3. **여러 기기가 있을 때**
   - 정확한 이름을 지정하면 해당 기기만 선택됩니다
   - 이름이 일치하지 않으면 첫 번째 기기를 사용합니다

4. **기기 이름 변경 방법**
   - Google Home 앱 > 기기 설정 > 기기 이름 변경

## ❓ 문제 해결

### 기기를 찾을 수 없을 때

1. **네트워크 확인**
   - PC와 Google Home Mini가 같은 Wi-Fi에 연결되어 있는지 확인
   - 방화벽이 mDNS 포트(5353)를 차단하지 않는지 확인

2. **기기 이름 확인**
   ```bash
   python test_local_broadcast.py --list
   ```

3. **수동으로 IP 주소 지정** (고급)
   - pychromecast는 IP 주소로도 연결 가능하지만, 현재 코드는 이름만 지원

## 📝 요약

- **기기 이름 확인**: `python test_local_broadcast.py --list`
- **권장 방송 타입**: `cast` (Chromecast 방식)
- **설정 파일**: `.env` 파일에 `GOOGLE_BROADCASTER_TYPE=cast` 추가

