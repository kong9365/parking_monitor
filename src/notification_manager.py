"""
알림 관리 모듈
입출차 변경을 감지하고 Google Home으로 안내방송을 전송합니다.
"""
from typing import List, Dict, Any, Optional
from database import ParkingDatabase
from change_detector import ChangeDetector
from google_assistant import GoogleAssistantBroadcaster, GoogleHomeCastBroadcaster
from logger import system_logger
import config


def is_resident_car(car_number: str) -> bool:
    """
    세대 차량 여부 확인
    
    Args:
        car_number: 차량번호
    
    Returns:
        세대 차량 여부
    """
    return car_number in config.RESIDENT_CARS


class NotificationManager:
    """알림 관리자"""
    
    def __init__(self, db: ParkingDatabase, broadcaster_type: str = 'cast'):
        """
        Args:
            db: 데이터베이스 인스턴스
            broadcaster_type: 방송 타입 ('assistant' 또는 'cast')
        """
        self.db = db
        self.detector = ChangeDetector(db)
        self.current_points = 0  # 현재 포인트 저장
        
        # 방송기 선택
        if broadcaster_type == 'assistant':
            self.broadcaster = GoogleAssistantBroadcaster()
        else:
            self.broadcaster = GoogleHomeCastBroadcaster()
        
        self.broadcaster_type = broadcaster_type
    
    def set_current_points(self, points: int):
        """
        현재 포인트 설정
        
        Args:
            points: 현재 포인트
        """
        self.current_points = points
    
    def initialize_broadcaster(self) -> bool:
        """
        방송기 초기화
        
        Returns:
            초기화 성공 여부
        """
        try:
            # GitHub Actions 환경에서는 방송 건너뛰기
            import os
            if os.getenv('GITHUB_ACTIONS') == 'true':
                system_logger.info("GitHub Actions 환경 감지: 방송 기능을 건너뜁니다.")
                system_logger.info("데이터 수집 및 저장은 정상적으로 진행됩니다.")
                return False
            
            if self.broadcaster_type == 'assistant':
                # Google Assistant 인증
                return self.broadcaster.authenticate()
            else:
                # Chromecast 연결
                return self.broadcaster.connect()
        except Exception as e:
            system_logger.error(f"방송기 초기화 실패: {str(e)}")
            return False
    
    def process_new_records(self, new_records: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        새로운 기록 처리 및 알림 전송
        
        Args:
            new_records: 최신 조회된 기록 리스트
        
        Returns:
            처리 결과 통계 {'entries': 입차 수, 'exits': 출차 수, 'notifications': 알림 수}
        """
        stats = {
            'entries': 0,
            'exits': 0,
            'notifications': 0
        }
        
        try:
            # 변경 감지
            new_entries, new_exits = self.detector.detect_changes(new_records)
            
            stats['entries'] = len(new_entries)
            stats['exits'] = len(new_exits)
            
            # 입차 알림
            for entry in new_entries:
                car_number, name, location = self.detector.get_entry_info(entry)
                is_resident = is_resident_car(car_number)
                
                car_type = "세대 차량" if is_resident else "방문차량"
                system_logger.info(f"입차 알림 전송: [{car_type}] {car_number} - {name}")
                
                if self.broadcaster.broadcast_entry(car_number, name, location, is_resident):
                    stats['notifications'] += 1
            
            # 출차 알림
            for exit_record in new_exits:
                car_number, name, location = self.detector.get_exit_info(exit_record)
                is_resident = is_resident_car(car_number)
                
                car_type = "세대 차량" if is_resident else "방문차량"
                system_logger.info(f"출차 알림 전송: [{car_type}] {car_number} - {name}")
                
                # 방문차량 출차 시 포인트 정보 포함
                if self.broadcaster.broadcast_exit(car_number, name, location, is_resident, 
                                                  self.current_points if not is_resident else 0):
                    stats['notifications'] += 1
            
            system_logger.success(
                f"알림 처리 완료 - 입차: {stats['entries']}건, 출차: {stats['exits']}건, 알림: {stats['notifications']}건"
            )
            
            return stats
        
        except Exception as e:
            system_logger.error(f"알림 처리 중 오류: {str(e)}")
            return stats
    
    def notify_entry(self, car_number: str, name: str, location: str) -> bool:
        """
        입차 알림 전송
        
        Args:
            car_number: 차량번호
            name: 고객명
            location: 입차 위치
        
        Returns:
            알림 성공 여부
        """
        try:
            is_resident = is_resident_car(car_number)
            return self.broadcaster.broadcast_entry(car_number, name, location, is_resident)
        except Exception as e:
            system_logger.error(f"입차 알림 실패: {str(e)}")
            return False
    
    def notify_exit(self, car_number: str, name: str, location: str) -> bool:
        """
        출차 알림 전송
        
        Args:
            car_number: 차량번호
            name: 고객명
            location: 출차 위치
        
        Returns:
            알림 성공 여부
        """
        try:
            is_resident = is_resident_car(car_number)
            return self.broadcaster.broadcast_exit(car_number, name, location, is_resident)
        except Exception as e:
            system_logger.error(f"출차 알림 실패: {str(e)}")
            return False

