# 로컬 Google Home Mini 방송 테스트 가이드

GitHub Actions에서 설정한 정보를 사용하여 로컬에서 Google Home Mini 방송을 테스트합니다.

## 빠른 테스트 (가장 간단)

### 1. 기기 목록 확인

먼저 같은 네트워크에 있는 Google Home 기기를 확인합니다:

```bash
cd parking_monitor/src
python test_local_broadcast.py --list
```

### 2. Chromecast 방식 테스트 (권장)

가장 간단하고 안정적인 방법입니다:

```bash
cd parking_monitor/src
python test_local_broadcast.py --method cast --device "기기이름" --message "안녕하세요. 테스트입니다."
```

예시:
```bash
python test_local_broadcast.py --method cast --device "거실" --message "테스트입니다"
```

### 3. Google Assistant SDK 방식 테스트

GitHub Actions에서 사용하는 방식과 동일합니다:

```bash
cd parking_monitor/src
python test_local_broadcast.py --method assistant --device "기기이름" --message "테스트입니다"
```

## GitHub Secrets 정보 사용하기

GitHub Actions에서 사용하는 설정을 로컬에서도 사용하려면:

### 1. .env 파일 생성

프로젝트 루트에 `.env` 파일을 만들고 다음 정보를 입력합니다:

```env
# GitHub Secrets에서 가져온 정보
GOOGLE_HOME_DEVICE_NAME=거실
GOOGLE_BROADCASTER_TYPE=cast

# Parking 정보 (테스트에는 불필요하지만 설정해두면 좋습니다)
PARKING_USER_ID=your_user_id
PARKING_PASSWORD=your_password
PARKING_URL=http://gdjepgcapt3.realparking.net:9080/
```

**GitHub Secrets에서 정보 가져오기:**
1. GitHub 저장소 페이지로 이동
2. Settings > Secrets and variables > Actions
3. 각 Secret의 값을 복사하여 .env 파일에 입력

### 2. Google 토큰 파일 설정 (Google Assistant SDK 사용 시)

Google Assistant SDK 방식을 사용하려면 `data/token.json` 파일이 필요합니다:

```bash
# data 디렉토리 생성
mkdir -p parking_monitor/data

# GitHub Secrets의 GOOGLE_TOKEN_JSON 값을 복사하여 파일 생성
# Windows PowerShell:
echo '{"token":"...","refresh_token":"..."}' > parking_monitor/data/token.json

# 또는 직접 파일 생성
```

**GitHub Secrets에서 토큰 가져오기:**
1. GitHub 저장소 > Settings > Secrets and variables > Actions
2. `GOOGLE_TOKEN_JSON` Secret 클릭
3. "Reveal secret" 버튼 클릭하여 값 복사
4. `data/token.json` 파일에 저장

### 3. client_secret.json 파일 (Google Assistant SDK 사용 시)

Google Assistant SDK를 처음 사용하는 경우 `client_secret.json` 파일이 필요합니다:

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 프로젝트 선택
3. **API 및 서비스** > **사용자 인증 정보**
4. OAuth 2.0 클라이언트 ID 다운로드
5. 파일명을 `client_secret.json`으로 변경
6. 프로젝트 루트에 배치

## 테스트 예제

### 예제 1: 기본 테스트
```bash
cd parking_monitor/src
python test_local_broadcast.py --method cast --device "거실" --message "안녕하세요. 테스트입니다."
```

### 예제 2: 입차 알림 테스트
```bash
python test_local_broadcast.py --method cast --device "거실" --message "세대 차량 39가5514가 후문 입구로 입차하였습니다."
```

### 예제 3: 출차 알림 테스트
```bash
python test_local_broadcast.py --method cast --device "거실" --message "방문차량 106누4166, 이소영님이 후문 출구2로 출차하셨습니다."
```

## 문제 해결

### 기기를 찾을 수 없습니다

1. **네트워크 확인**: PC와 Google Home Mini가 같은 Wi-Fi 네트워크에 연결되어 있는지 확인
2. **방화벽 확인**: Windows 방화벽이 mDNS 포트(5353)를 차단하지 않는지 확인
3. **기기 이름 확인**: Google Home 앱에서 정확한 기기 이름 확인
   ```bash
   python test_local_broadcast.py --list
   ```

### 방송은 되지만 소리가 안 들립니다

1. Google Home Mini의 볼륨 확인
2. 다른 앱이 재생 중인지 확인
3. 네트워크 지연 확인
4. 메시지가 너무 짧으면 재생 시간이 짧을 수 있음

### Google Assistant SDK 인증 실패

1. `data/token.json` 파일이 있는지 확인
2. `client_secret.json` 파일이 프로젝트 루트에 있는지 확인
3. 토큰이 만료되었을 수 있으므로 재인증 필요

## GitHub Actions와 비교

GitHub Actions 로그를 보면:
- ✅ 인증 성공: "토큰 갱신 완료"
- ✅ 방송 메시지 생성: "방송 메시지: ..."
- ✅ 방송 완료: "방송 완료: ..."

하지만 실제로 Google Home Mini에서 소리가 났는지는 확인할 수 없습니다.

로컬 테스트를 통해 실제로 소리가 나는지 확인할 수 있습니다!

## 권장 테스트 순서

1. **기기 목록 확인**
   ```bash
   python test_local_broadcast.py --list
   ```

2. **간단한 메시지 테스트**
   ```bash
   python test_local_broadcast.py --method cast --device "기기이름" --message "테스트"
   ```

3. **실제 알림 메시지 테스트**
   ```bash
   python test_local_broadcast.py --method cast --device "기기이름" --message "세대 차량 39가5514가 후문 입구로 입차하였습니다."
   ```

4. **Google Assistant SDK 방식 테스트** (선택사항)
   ```bash
   python test_local_broadcast.py --method assistant --device "기기이름" --message "테스트"
   ```

