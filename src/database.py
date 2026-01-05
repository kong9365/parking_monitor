"""
데이터베이스 관리 모듈
입출차 기록을 SQLite 데이터베이스에 저장하고 조회합니다.
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import config
from logger import database_logger


class ParkingDatabase:
    """입출차 기록 데이터베이스"""
    
    def __init__(self, db_path: Optional[Path] = None):
        """
        Args:
            db_path: 데이터베이스 파일 경로 (기본값: config.DATABASE_PATH)
        """
        self.db_path = db_path or config.DATABASE_PATH
        self._init_database()
    
    def _init_database(self):
        """데이터베이스 초기화 및 테이블 생성"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 입출차 기록 테이블 생성
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS parking_records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        car_number TEXT NOT NULL,
                        name TEXT,
                        type TEXT,
                        phone TEXT,
                        entry_location TEXT,
                        entry_time TEXT NOT NULL,
                        exit_location TEXT,
                        exit_time TEXT,
                        status TEXT,
                        note TEXT,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(car_number, entry_time)
                    )
                ''')
                
                # 인덱스 생성
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_car_number 
                    ON parking_records(car_number)
                ''')
                
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_entry_time 
                    ON parking_records(entry_time)
                ''')
                
                conn.commit()
                database_logger.success("데이터베이스 초기화 완료")
        
        except Exception as e:
            database_logger.error(f"데이터베이스 초기화 실패: {str(e)}")
            raise
    
    def insert_record(self, record: Dict[str, Any]) -> bool:
        """
        입출차 기록 추가
        
        Args:
            record: 입출차 기록 딕셔너리
        
        Returns:
            성공 여부
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR IGNORE INTO parking_records 
                    (car_number, name, type, phone, entry_location, entry_time, 
                     exit_location, exit_time, status, note)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    record.get('car_number'),
                    record.get('name'),
                    record.get('type'),
                    record.get('phone'),
                    record.get('entry_location'),
                    record.get('entry_time'),
                    record.get('exit_location'),
                    record.get('exit_time'),
                    record.get('status'),
                    record.get('note')
                ))
                
                conn.commit()
                
                if cursor.rowcount > 0:
                    database_logger.info(
                        f"새 기록 추가: {record.get('car_number')} - {record.get('entry_time')}",
                        {'record': record}
                    )
                    return True
                else:
                    return False
        
        except Exception as e:
            database_logger.error(f"기록 추가 실패: {str(e)}", {'record': record})
            return False
    
    def insert_records(self, records: List[Dict[str, Any]]) -> int:
        """
        여러 입출차 기록 추가
        
        Args:
            records: 입출차 기록 리스트
        
        Returns:
            추가된 기록 수
        """
        count = 0
        for record in records:
            if self.insert_record(record):
                count += 1
        
        database_logger.info(f"총 {count}개의 새 기록 추가됨 (전체: {len(records)}개)")
        return count
    
    def get_all_records(self) -> List[Dict[str, Any]]:
        """모든 입출차 기록 조회"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM parking_records 
                    ORDER BY entry_time DESC
                ''')
                
                records = [dict(row) for row in cursor.fetchall()]
                return records
        
        except Exception as e:
            database_logger.error(f"기록 조회 실패: {str(e)}")
            return []
    
    def get_records_by_date(self, date: str) -> List[Dict[str, Any]]:
        """
        특정 날짜의 입출차 기록 조회
        
        Args:
            date: 날짜 (YYYY-MM-DD 형식)
        
        Returns:
            입출차 기록 리스트
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM parking_records 
                    WHERE entry_time LIKE ?
                    ORDER BY entry_time DESC
                ''', (f'{date}%',))
                
                records = [dict(row) for row in cursor.fetchall()]
                return records
        
        except Exception as e:
            database_logger.error(f"날짜별 기록 조회 실패: {str(e)}")
            return []
    
    def get_recent_records(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        최근 입출차 기록 조회
        
        Args:
            limit: 조회할 기록 수
        
        Returns:
            입출차 기록 리스트
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM parking_records 
                    ORDER BY created_at DESC
                    LIMIT ?
                ''', (limit,))
                
                records = [dict(row) for row in cursor.fetchall()]
                return records
        
        except Exception as e:
            database_logger.error(f"최근 기록 조회 실패: {str(e)}")
            return []
    
    def record_exists(self, car_number: str, entry_time: str) -> bool:
        """
        기록 존재 여부 확인
        
        Args:
            car_number: 차량번호
            entry_time: 입차 시간
        
        Returns:
            존재 여부
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT COUNT(*) FROM parking_records 
                    WHERE car_number = ? AND entry_time = ?
                ''', (car_number, entry_time))
                
                count = cursor.fetchone()[0]
                return count > 0
        
        except Exception as e:
            database_logger.error(f"기록 존재 확인 실패: {str(e)}")
            return False
    
    def get_records_by_car_and_entry(self, car_number: str, entry_time: str) -> List[Dict[str, Any]]:
        """
        차량번호와 입차시간으로 기록 조회
        
        Args:
            car_number: 차량번호
            entry_time: 입차 시간
        
        Returns:
            입출차 기록 리스트
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM parking_records 
                    WHERE car_number = ? AND entry_time = ?
                ''', (car_number, entry_time))
                
                records = [dict(row) for row in cursor.fetchall()]
                return records
        
        except Exception as e:
            database_logger.error(f"기록 조회 실패: {str(e)}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """데이터베이스 통계 정보"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 전체 기록 수
                cursor.execute('SELECT COUNT(*) FROM parking_records')
                total_count = cursor.fetchone()[0]
                
                # 오늘 입차 기록 수
                today = datetime.now().strftime('%Y/%m/%d')
                cursor.execute('''
                    SELECT COUNT(*) FROM parking_records 
                    WHERE entry_time LIKE ?
                ''', (f'{today}%',))
                today_count = cursor.fetchone()[0]
                
                # 미출차 기록 수
                cursor.execute('''
                    SELECT COUNT(*) FROM parking_records 
                    WHERE exit_time IS NULL OR exit_time = ''
                ''')
                not_exited_count = cursor.fetchone()[0]
                
                stats = {
                    'total_records': total_count,
                    'today_records': today_count,
                    'not_exited': not_exited_count
                }
                
                return stats
        
        except Exception as e:
            database_logger.error(f"통계 조회 실패: {str(e)}")
            return {}

