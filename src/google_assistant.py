"""
Google Assistant SDK 모듈
Google Home으로 안내방송을 전송합니다.
"""
import json
import os
import ssl
from pathlib import Path
from typing import Optional
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import config
from logger import system_logger

# SSL 인증서 검증 비활성화 (회사 네트워크 환경)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ['REQUESTS_CA_BUNDLE'] = ''
os.environ['CURL_CA_BUNDLE'] = ''


# OAuth 2.0 스코프
SCOPES = [
    'https://www.googleapis.com/auth/assistant-sdk-prototype',
    'https://www.googleapis.com/auth/gcm'
]


class GoogleAssistantBroadcaster:
    """Google Assistant를 통한 방송 기능"""
    
    def __init__(self, credentials_path: Optional[Path] = None, token_path: Optional[Path] = None):
        """
        Args:
            credentials_path: OAuth 클라이언트 시크릿 파일 경로
            token_path: 토큰 저장 경로
        """
        self.credentials_path = credentials_path or config.PROJECT_ROOT / 'client_secret.json'
        self.token_path = token_path or config.DATA_DIR / 'token.json'
        self.credentials = None
    
    def authenticate(self) -> bool:
        """
        Google OAuth 인증 수행
        
        Returns:
            인증 성공 여부
        """
        try:
            # 기존 토큰 로드
            if self.token_path.exists():
                self.credentials = Credentials.from_authorized_user_file(
                    str(self.token_path), SCOPES
                )
                system_logger.info("기존 토큰 로드 완료")
            
            # 토큰이 없거나 만료된 경우
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    # 토큰 갱신
                    system_logger.info("토큰 갱신 중...")
                    import requests
                    session = requests.Session()
                    session.verify = False
                    self.credentials.refresh(Request(session=session))
                    system_logger.success("토큰 갱신 완료")
                else:
                    # 새로운 인증 플로우
                    if not self.credentials_path.exists():
                        system_logger.error(f"클라이언트 시크릿 파일을 찾을 수 없습니다: {self.credentials_path}")
                        return False
                    
                    system_logger.info("새로운 인증 플로우 시작...")
                    
                    # SSL 검증 비활성화
                    import httplib2
                    http = httplib2.Http(disable_ssl_certificate_validation=True)
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(self.credentials_path), SCOPES
                    )
                    # SSL 검증 우회
                    import requests
                    original_post = requests.post
                    def patched_post(*args, **kwargs):
                        kwargs['verify'] = False
                        return original_post(*args, **kwargs)
                    requests.post = patched_post
                    
                    self.credentials = flow.run_local_server(port=0)
                    requests.post = original_post
                    system_logger.success("인증 완료")
                
                # 토큰 저장
                with open(self.token_path, 'w') as token_file:
                    token_file.write(self.credentials.to_json())
                system_logger.info("토큰 저장 완료")
            
            return True
        
        except Exception as e:
            system_logger.error(f"인증 실패: {str(e)}")
            return False
    
    def broadcast(self, message: str, device_name: Optional[str] = None) -> bool:
        """
        Google Home으로 메시지 방송
        Google Assistant SDK 인증 후 Chromecast를 통해 방송
        
        Args:
            message: 방송할 메시지
            device_name: Google Home 기기 이름 (기본값: config에서 가져옴)
        
        Returns:
            방송 성공 여부
        """
        try:
            if not self.credentials:
                system_logger.error("인증이 필요합니다")
                return False
            
            system_logger.info(f"Google Assistant SDK를 통한 방송 메시지: {message}")
            
            # Chromecast로 재생하기 위해 pychromecast 사용
            try:
                import pychromecast
            except ImportError:
                system_logger.error("pychromecast 모듈이 설치되지 않았습니다")
                return False
            
            device_name = device_name or config.GOOGLE_HOME_DEVICE_NAME
            
            # gTTS로 음성 생성 (Google Assistant SDK 인증은 완료된 상태)
            from gtts import gTTS
            import tempfile
            import time
            import http.server
            import socketserver
            import threading
            import socket
            
            # TTS 생성
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_file = fp.name
                tts = gTTS(text=message, lang='ko')
                tts.save(temp_file)
            
            # Chromecast 기기 검색
            system_logger.info(f"Google Home 기기 검색 중: {device_name}")
            chromecasts, browser = pychromecast.get_listed_chromecasts(
                friendly_names=[device_name]
            )
            
            if not chromecasts:
                system_logger.error(f"기기를 찾을 수 없습니다: {device_name}")
                os.unlink(temp_file)
                browser.stop_discovery()
                return False
            
            device = chromecasts[0]
            device.wait()
            system_logger.info(f"기기 연결 완료: {device.name}")
            
            # HTTP 서버 시작 (Chromecast는 로컬 파일을 직접 재생할 수 없음)
            PORT = 8000
            Handler = http.server.SimpleHTTPRequestHandler
            
            # 파일이 있는 디렉토리로 이동
            original_dir = os.getcwd()
            file_dir = os.path.dirname(temp_file)
            file_name = os.path.basename(temp_file)
            
            os.chdir(file_dir)
            
            httpd = socketserver.TCPServer(("", PORT), Handler)
            server_thread = threading.Thread(target=httpd.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            
            # 로컬 IP 주소 가져오기
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(('8.8.8.8', 80))
                local_ip = s.getsockname()[0]
                s.close()
            except:
                local_ip = '127.0.0.1'
            
            media_url = f'http://{local_ip}:{PORT}/{file_name}'
            system_logger.info(f"미디어 URL: {media_url}")
            
            # Chromecast로 재생
            mc = device.media_controller
            mc.play_media(media_url, 'audio/mp3')
            mc.block_until_active()
            
            # 재생 완료 대기 (메시지 길이에 따라 조정)
            wait_time = max(5, len(message) * 0.1)
            time.sleep(wait_time)
            
            # 정리
            os.chdir(original_dir)
            httpd.shutdown()
            httpd.server_close()
            os.unlink(temp_file)
            browser.stop_discovery()
            
            system_logger.success(f"Google Assistant SDK를 통한 방송 완료: {message}")
            return True
        
        except Exception as e:
            system_logger.error(f"방송 실패: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def broadcast_entry(self, car_number: str, name: str, location: str, is_resident: bool = False) -> bool:
        """
        입차 안내방송
        
        Args:
            car_number: 차량번호
            name: 고객명
            location: 입차 위치
            is_resident: 세대 차량 여부
        
        Returns:
            방송 성공 여부
        """
        if is_resident:
            message = f"세대 차량 {car_number}가 {location}로 입차하였습니다."
        else:
            message = f"방문차량 {car_number}, {name}님이 {location}로 입차하셨습니다."
        return self.broadcast(message)
    
    def broadcast_exit(self, car_number: str, name: str, location: str, is_resident: bool = False, 
                      current_points: int = 0) -> bool:
        """
        출차 안내방송
        
        Args:
            car_number: 차량번호
            name: 고객명
            location: 출차 위치
            is_resident: 세대 차량 여부
            current_points: 현재 포인트 (방문차량 출차 시 사용)
        
        Returns:
            방송 성공 여부
        """
        if is_resident:
            message = f"세대 차량 {car_number}가 {location}로 출차하였습니다."
        else:
            message = f"방문차량 {car_number}, {name}님이 {location}로 출차하셨습니다."
            
            # 방문차량 출차 시 포인트 정보 추가
            if current_points > 0:
                import config
                base_points = config.BASE_POINTS
                percentage = int((current_points / base_points) * 100)
                message += f" 잔여 포인트 {current_points:,}P, 기준 대비 {percentage}% 남았습니다."
        
        return self.broadcast(message)


class GoogleHomeCastBroadcaster:
    """
    pychromecast를 사용한 Google Home 방송
    (Google Assistant SDK의 대안)
    """
    
    def __init__(self, device_name: Optional[str] = None):
        """
        Args:
            device_name: Google Home 기기 이름
        """
        self.device_name = device_name or os.getenv('GOOGLE_HOME_DEVICE_NAME', 'Living Room')
        self.device = None
    
    def connect(self) -> bool:
        """
        Google Home 기기에 연결
        
        Returns:
            연결 성공 여부
        """
        try:
            import pychromecast
            
            system_logger.info(f"Google Home 기기 검색 중: {self.device_name}")
            
            # Chromecast 기기 검색
            chromecasts, browser = pychromecast.get_listed_chromecasts(
                friendly_names=[self.device_name]
            )
            
            if not chromecasts:
                system_logger.error(f"기기를 찾을 수 없습니다: {self.device_name}")
                return False
            
            self.device = chromecasts[0]
            self.device.wait()
            
            system_logger.success(f"기기 연결 완료: {self.device.name}")
            return True
        
        except ImportError:
            system_logger.error("pychromecast 모듈이 설치되지 않았습니다")
            return False
        except Exception as e:
            system_logger.error(f"기기 연결 실패: {str(e)}")
            return False
    
    def speak(self, text: str, language: str = 'ko') -> bool:
        """
        TTS로 텍스트 읽기
        
        Args:
            text: 읽을 텍스트
            language: 언어 코드
        
        Returns:
            성공 여부
        """
        try:
            if not self.device:
                system_logger.error("기기가 연결되지 않았습니다")
                return False
            
            from gtts import gTTS
            import tempfile
            
            # TTS 생성
            tts = gTTS(text=text, lang=language)
            
            # 임시 파일에 저장
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_file = fp.name
                tts.save(temp_file)
            
            # Chromecast로 재생
            mc = self.device.media_controller
            mc.play_media(f'file://{temp_file}', 'audio/mp3')
            mc.block_until_active()
            
            system_logger.success(f"음성 재생 완료: {text}")
            
            # 임시 파일 삭제
            os.unlink(temp_file)
            
            return True
        
        except Exception as e:
            system_logger.error(f"음성 재생 실패: {str(e)}")
            return False
    
    def broadcast_entry(self, car_number: str, name: str, location: str, is_resident: bool = False) -> bool:
        """입차 안내방송"""
        if is_resident:
            message = f"세대 차량 {car_number}가 {location}로 입차하였습니다."
        else:
            message = f"방문차량 {car_number}, {name}님이 {location}로 입차하셨습니다."
        return self.speak(message)
    
    def broadcast_exit(self, car_number: str, name: str, location: str, is_resident: bool = False,
                      current_points: int = 0) -> bool:
        """출차 안내방송"""
        if is_resident:
            message = f"세대 차량 {car_number}가 {location}로 출차하였습니다."
        else:
            message = f"방문차량 {car_number}, {name}님이 {location}로 출차하셨습니다."
            
            # 방문차량 출차 시 포인트 정보 추가
            if current_points > 0:
                import config
                base_points = config.BASE_POINTS
                percentage = int((current_points / base_points) * 100)
                message += f" 잔여 포인트 {current_points:,}P, 기준 대비 {percentage}% 남았습니다."
        
        return self.speak(message)

