# Google Assistant SDK 테스트 가이드

Google Home Mini에서 실제로 방송이 되는지 테스트하는 방법입니다.

## 빠른 테스트 (Chromecast 방식 - 권장)

가장 간단하고 안정적인 방법입니다. Google Assistant SDK 인증 없이 바로 테스트할 수 있습니다.

### 1. 사용 가능한 기기 확인

```bash
cd parking_monitor/src
python test_google_assistant.py --method list
```

이 명령어로 같은 네트워크에 있는 Chromecast 기기 목록을 확인할 수 있습니다.

### 2. 기본 테스트 실행

```bash
cd parking_monitor/src
python test_google_assistant.py --method cast
```

기본 테스트 메시지 3개가 방송됩니다.

### 3. 특정 메시지 테스트

```bash
cd parking_monitor/src
python test_google_assistant.py --method cast --message "안녕하세요. 테스트입니다."
```

### 4. 특정 기기 지정

```bash
cd parking_monitor/src
python test_google_assistant.py --method cast --device "거실" --message "테스트 메시지"
```

## Google Assistant SDK 방식 테스트

Google OAuth 인증이 필요한 방식입니다.

### 1. 사전 준비

#### Google Cloud 프로젝트 설정

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성 또는 기존 프로젝트 선택
3. **API 및 서비스** > **라이브러리**에서 다음 API 활성화:
   - Google Assistant API
   - Google Cloud Text-to-Speech API (선택사항)

#### OAuth 2.0 클라이언트 ID 생성

1. **API 및 서비스** > **사용자 인증 정보** 이동
2. **사용자 인증 정보 만들기** > **OAuth 클라이언트 ID** 선택
3. 애플리케이션 유형: **기타** 선택
4. 이름 지정 후 생성
5. 생성된 클라이언트 ID의 JSON 파일 다운로드
6. 파일명을 `client_secret.json`으로 변경
7. 프로젝트 루트 디렉토리에 배치

### 2. 테스트 실행

```bash
cd parking_monitor/src
python test_google_assistant.py --method assistant
```

첫 실행 시 브라우저가 열리고 Google 계정으로 로그인하여 인증해야 합니다.

### 3. 특정 메시지 테스트

```bash
cd parking_monitor/src
python test_google_assistant.py --method assistant --message "테스트 메시지"
```

## 문제 해결

### 기기를 찾을 수 없습니다

1. **네트워크 확인**: PC와 Google Home Mini가 같은 Wi-Fi 네트워크에 연결되어 있는지 확인
2. **방화벽 확인**: Windows 방화벽이 mDNS 포트(5353)를 차단하지 않는지 확인
3. **기기 이름 확인**: Google Home 앱에서 정확한 기기 이름 확인

### 인증 실패

1. `client_secret.json` 파일이 프로젝트 루트에 있는지 확인
2. Google Cloud Console에서 API가 활성화되어 있는지 확인
3. OAuth 동의 화면이 설정되어 있는지 확인

### 방송은 되지만 소리가 안 들립니다

1. Google Home Mini의 볼륨 확인
2. 다른 앱이 재생 중인지 확인
3. 네트워크 지연 확인

## 권장 방법

**Chromecast 방식 (cast)**을 권장합니다:
- ✅ Google OAuth 인증 불필요
- ✅ 설정이 간단함
- ✅ 안정적이고 빠름
- ✅ 실제로 작동함

Google Assistant SDK 방식은:
- ⚠️ 복잡한 설정 필요
- ⚠️ OAuth 인증 필요
- ⚠️ 실제로는 Chromecast와 동일한 방식으로 작동

## 테스트 예제

```bash
# 1. 기기 목록 확인
python test_google_assistant.py --method list

# 2. 기본 테스트 (Chromecast)
python test_google_assistant.py --method cast

# 3. 입차 알림 테스트
python test_google_assistant.py --method cast --message "세대 차량 39가5514가 후문 입구로 입차하였습니다."

# 4. 출차 알림 테스트
python test_google_assistant.py --method cast --message "방문차량 106누4166, 이소영님이 후문 출구2로 출차하셨습니다."
```

