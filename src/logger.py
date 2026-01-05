"""
구조화된 JSON 로깅 시스템
카테고리별로 분리된 로그 파일에 JSON 형식으로 기록합니다.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import config


class StructuredLogger:
    """구조화된 JSON 로거"""
    
    def __init__(self, category: str):
        """
        Args:
            category: 로그 카테고리 (SYSTEM, SCRAPING, DATABASE)
        """
        self.category = category
        self.log_dir = config.LOG_CATEGORIES.get(category, config.LOGS_DIR / category)
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_log_file(self) -> Path:
        """오늘 날짜의 로그 파일 경로 반환"""
        today = datetime.now().strftime('%Y%m%d')
        return self.log_dir / f'{today}.json'
    
    def _write_log(self, level: str, message: str, data: Optional[Dict[str, Any]] = None):
        """로그 엔트리 작성"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'category': self.category,
            'message': message
        }
        
        if data:
            log_entry['data'] = data
        
        log_file = self._get_log_file()
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def info(self, message: str, data: Optional[Dict[str, Any]] = None):
        """정보 로그"""
        self._write_log('INFO', message, data)
        print(f"[INFO] {message}")
    
    def warning(self, message: str, data: Optional[Dict[str, Any]] = None):
        """경고 로그"""
        self._write_log('WARNING', message, data)
        print(f"[WARNING] {message}")
    
    def error(self, message: str, data: Optional[Dict[str, Any]] = None):
        """에러 로그"""
        self._write_log('ERROR', message, data)
        print(f"[ERROR] {message}")
    
    def success(self, message: str, data: Optional[Dict[str, Any]] = None):
        """성공 로그"""
        self._write_log('SUCCESS', message, data)
        print(f"[SUCCESS] {message}")


# 로거 인스턴스 생성
system_logger = StructuredLogger('SYSTEM')
scraping_logger = StructuredLogger('SCRAPING')
database_logger = StructuredLogger('DATABASE')

