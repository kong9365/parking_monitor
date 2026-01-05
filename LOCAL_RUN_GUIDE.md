# 🏠 로컬 실행 가이드 (진정한 실시간!)

GitHub Actions는 최소 5분이지만, 로컬 실행은 **1분마다 또는 더 자주** 가능합니다!

## 📋 목차
1. [Windows 작업 스케줄러로 1분마다 실행](#windows)
2. [Linux/Mac Cron으로 1분마다 실행](#linux)
3. [무한 루프로 30초마다 실행](#loop)

---

## 🪟 Windows 작업 스케줄러 (1분마다)

### 1. 배치 파일 생성

`run_parking_monitor.bat` 파일을 프로젝트 폴더에 생성:

```batch
@echo off
cd /d C:\Users\user\Desktop\Coding\cusor\parking_monitor
call venv\Scripts\activate
python src\main_with_notification.py
```

### 2. 작업 스케줄러 설정

1. **Windows 검색**에서 "작업 스케줄러" 실행
2. **작업 만들기** 클릭
3. **일반 탭**:
   - 이름: `Parking Monitor - 1분마다`
   - 설명: `주차장 입출차 실시간 모니터링`
   - 최고 권한으로 실행 체크
4. **트리거 탭**:
   - **새로 만들기** 클릭
   - 시작: `매일`
   - 고급 설정:
     - ✅ **반복 간격: 1분**
     - ✅ **기간: 무기한**
5. **동작 탭**:
   - **새로 만들기** 클릭
   - 프로그램/스크립트: `C:\Users\user\Desktop\Coding\cusor\parking_monitor\run_parking_monitor.bat`
6. **확인** 클릭

### 3. 테스트

작업 스케줄러에서 방금 만든 작업을 **마우스 우클릭 → 실행**하여 테스트!

---

## 🐧 Linux/Mac Cron (1분마다)

### 1. Cron 편집

```bash
crontab -e
```

### 2. 1분마다 실행 추가

```bash
# 매 1분마다 실행
* * * * * cd /home/user/parking_monitor && /home/user/parking_monitor/venv/bin/python src/main_with_notification.py >> logs/cron.log 2>&1
```

### 3. Cron 서비스 재시작

```bash
sudo systemctl restart cron
```

---

## 🔄 무한 루프 (30초마다 또는 원하는 간격)

가장 유연한 방법! **30초, 15초, 심지어 10초마다**도 가능!

### 1. 새로운 스크립트 생성

`src/realtime_monitor.py` 생성:

```python
import asyncio
import time
from datetime import datetime
from main_with_notification import main
from logger import Logger

logger = Logger('REALTIME_MONITOR').get_logger()

async def realtime_monitor(interval_seconds=60):
    """
    실시간 모니터링 루프
    
    Args:
        interval_seconds: 체크 간격 (초)
                         60 = 1분마다
                         30 = 30초마다
                         15 = 15초마다
    """
    logger.info(f"실시간 모니터링 시작 - {interval_seconds}초 간격")
    
    while True:
        try:
            start_time = time.time()
            logger.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 입출차 체크 시작")
            
            # 메인 로직 실행
            await main()
            
            elapsed = time.time() - start_time
            logger.success(f"실행 완료 ({elapsed:.1f}초 소요)")
            
            # 다음 실행까지 대기
            wait_time = max(0, interval_seconds - elapsed)
            if wait_time > 0:
                logger.info(f"다음 체크까지 {wait_time:.1f}초 대기...")
                await asyncio.sleep(wait_time)
            
        except KeyboardInterrupt:
            logger.info("사용자에 의해 중단됨")
            break
        except Exception as e:
            logger.error(f"오류 발생: {e}")
            logger.info("10초 후 재시도...")
            await asyncio.sleep(10)

if __name__ == "__main__":
    # 원하는 간격 설정 (초 단위)
    INTERVAL = 60  # 1분마다
    # INTERVAL = 30  # 30초마다
    # INTERVAL = 15  # 15초마다
    
    asyncio.run(realtime_monitor(INTERVAL))
```

### 2. 실행

```bash
# Windows
python src\realtime_monitor.py

# Linux/Mac
python src/realtime_monitor.py
```

### 3. 백그라운드 실행 (Linux/Mac)

```bash
nohup python src/realtime_monitor.py > logs/realtime.log 2>&1 &
```

### 4. 서비스로 등록 (Linux - systemd)

`/etc/systemd/system/parking-monitor.service` 생성:

```ini
[Unit]
Description=Parking Monitor Realtime Service
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/home/user/parking_monitor
ExecStart=/home/user/parking_monitor/venv/bin/python src/realtime_monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

서비스 시작:

```bash
sudo systemctl daemon-reload
sudo systemctl enable parking-monitor
sudo systemctl start parking-monitor
sudo systemctl status parking-monitor
```

---

## 📊 각 방법 비교

| 방법 | 최소 간격 | 장점 | 단점 |
|------|----------|------|------|
| **GitHub Actions** | 5분 | 무료, 서버 불필요 | 실시간 불가, 지연 가능 |
| **Windows 작업 스케줄러** | 1분 | 간단, GUI | PC 켜져있어야 함 |
| **Linux Cron** | 1분 | 안정적 | 1분 미만 불가 |
| **무한 루프** | **제한 없음** | 완전 유연, 30초/15초/10초 가능 | 직접 관리 필요 |

---

## 🎯 추천

### 일반 가정집
- **무한 루프 방식** (30초~1분 간격)
- 컴퓨터 또는 라즈베리파이에서 실행

### 항상 켜져있는 PC
- **Windows 작업 스케줄러** (1분 간격)
- 가장 간단함

### 서버/클라우드
- **systemd 서비스** (원하는 간격)
- 가장 안정적

---

## ⚡ 초단위 실시간이 필요하다면?

10초, 5초마다 체크하고 싶다면 **무한 루프 방식**이 유일한 방법입니다:

```python
# 10초마다
INTERVAL = 10

# 5초마다
INTERVAL = 5

# 1초마다 (비추천 - 서버 부담)
INTERVAL = 1
```

---

## 💡 팁

1. **배터리 절약**: 노트북이라면 30초~1분 간격 추천
2. **서버 부담**: 주차장 웹사이트에 부담 주지 않도록 최소 15초 이상 권장
3. **로그 확인**: `logs/` 폴더에서 실행 결과 확인
4. **자동 시작**: PC 부팅 시 자동 실행되도록 설정 가능

---

**이제 진짜 실시간 알림이 가능합니다!** 🚀

