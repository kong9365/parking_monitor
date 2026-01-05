"""
입출차 변경 감지 모듈
새로운 입차 및 출차를 감지합니다.
"""
from typing import List, Dict, Any, Tuple
from database import ParkingDatabase
from logger import system_logger


class ChangeDetector:
    """입출차 변경 감지기"""
    
    def __init__(self, db: ParkingDatabase):
        """
        Args:
            db: 데이터베이스 인스턴스
        """
        self.db = db
    
    def detect_changes(self, new_records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        새로운 입차 및 출차 감지
        
        Args:
            new_records: 최신 조회된 기록 리스트
        
        Returns:
            (새로운 입차 리스트, 새로운 출차 리스트)
        """
        new_entries = []
        new_exits = []
        
        for record in new_records:
            car_number = record.get('car_number')
            entry_time = record.get('entry_time')
            exit_time = record.get('exit_time')
            
            if not car_number or not entry_time:
                continue
            
            # 데이터베이스에 기록이 있는지 확인
            existing = self.db.record_exists(car_number, entry_time)
            
            if not existing:
                # 새로운 입차
                new_entries.append(record)
                system_logger.info(
                    f"새로운 입차 감지: {car_number} - {entry_time}",
                    {'record': record}
                )
            else:
                # 기존 기록이 있는 경우, 출차 여부 확인
                if exit_time:
                    # 출차 정보가 업데이트되었는지 확인
                    existing_records = self.db.get_records_by_car_and_entry(car_number, entry_time)
                    if existing_records:
                        existing_record = existing_records[0]
                        existing_exit_time = existing_record.get('exit_time')
                        
                        # 기존에 출차 정보가 없었는데 새로 생긴 경우
                        if not existing_exit_time and exit_time:
                            new_exits.append(record)
                            system_logger.info(
                                f"새로운 출차 감지: {car_number} - {exit_time}",
                                {'record': record}
                            )
        
        system_logger.info(f"변경 감지 완료 - 입차: {len(new_entries)}건, 출차: {len(new_exits)}건")
        return new_entries, new_exits
    
    def get_entry_info(self, record: Dict[str, Any]) -> Tuple[str, str, str]:
        """
        입차 정보 추출
        
        Args:
            record: 입차 기록
        
        Returns:
            (차량번호, 이름, 위치)
        """
        car_number = record.get('car_number', '알 수 없음')
        name = record.get('name', '방문객')
        location = record.get('entry_location', '입구')
        
        # 위치 정보 정리 (언더스코어 제거)
        location = location.replace('_', ' ')
        
        return car_number, name, location
    
    def get_exit_info(self, record: Dict[str, Any]) -> Tuple[str, str, str]:
        """
        출차 정보 추출
        
        Args:
            record: 출차 기록
        
        Returns:
            (차량번호, 이름, 위치)
        """
        car_number = record.get('car_number', '알 수 없음')
        name = record.get('name', '방문객')
        location = record.get('exit_location', '출구')
        
        # 위치 정보 정리 (언더스코어 제거)
        location = location.replace('_', ' ')
        
        return car_number, name, location

