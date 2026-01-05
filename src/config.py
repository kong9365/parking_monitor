"""
설정 파일
환경 변수 및 프로젝트 설정을 관리합니다.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 프로젝트 루트 디렉토리
PROJECT_ROOT = Path(__file__).parent.parent

# .env 파일 로드
load_dotenv(PROJECT_ROOT / '.env')

# Real Parking 로그인 정보
PARKING_USER_ID = os.getenv('PARKING_USER_ID')
PARKING_PASSWORD = os.getenv('PARKING_PASSWORD')
PARKING_URL = os.getenv('PARKING_URL', 'http://gdjepgcapt3.realparking.net:9080/')

# 디렉토리 설정
DATA_DIR = PROJECT_ROOT / 'data'
LOGS_DIR = PROJECT_ROOT / 'logs'

# 데이터베이스 설정
DATABASE_PATH = DATA_DIR / 'parking_records.db'

# 로그 카테고리
LOG_CATEGORIES = {
    'SYSTEM': LOGS_DIR / 'SYSTEM',
    'SCRAPING': LOGS_DIR / 'SCRAPING',
    'DATABASE': LOGS_DIR / 'DATABASE'
}

# 디렉토리 생성
DATA_DIR.mkdir(parents=True, exist_ok=True)
for log_dir in LOG_CATEGORIES.values():
    log_dir.mkdir(parents=True, exist_ok=True)

# Playwright 설정
HEADLESS = True  # 브라우저를 숨김 모드로 실행
TIMEOUT = 30000  # 타임아웃 (밀리초)

# 날짜 형식
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y/%m/%d %H:%M:%S'

# Google Home 설정
GOOGLE_HOME_DEVICE_NAME = os.getenv('GOOGLE_HOME_DEVICE_NAME', 'Living Room')
GOOGLE_BROADCASTER_TYPE = os.getenv('GOOGLE_BROADCASTER_TYPE', 'cast')  # 'assistant' 또는 'cast'

# 세대 차량 번호 리스트
RESIDENT_CARS = [
    '39가5514',
    '64우0364'
]

# 포인트 설정
BASE_POINTS = 6000  # 기준 포인트 (고정값)

