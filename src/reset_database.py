"""
데이터베이스 초기화 스크립트
GitHub에 저장된 입출차 기록 데이터를 초기화합니다.
"""
import sys
import os
from pathlib import Path

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent))

from database import ParkingDatabase
from logger import system_logger


def reset_database():
    """데이터베이스 초기화 (모든 기록 삭제)"""
    try:
        db = ParkingDatabase()
        
        # 데이터베이스 파일 경로
        db_path = db.db_path
        
        print("\n" + "="*60)
        print("데이터베이스 초기화")
        print("="*60)
        print(f"데이터베이스 경로: {db_path}")
        
        # 기존 기록 수 확인
        stats = db.get_statistics()
        total_records = stats.get('total_records', 0)
        
        print(f"\n현재 저장된 기록 수: {total_records}건")
        
        if total_records == 0:
            print("✅ 데이터베이스가 이미 비어있습니다.")
            return True
        
        # 확인
        response = input(f"\n⚠️  정말로 {total_records}건의 모든 기록을 삭제하시겠습니까? (yes/no): ")
        
        if response.lower() != 'yes':
            print("❌ 초기화가 취소되었습니다.")
            return False
        
        # 데이터베이스 파일 삭제
        if db_path.exists():
            db_path.unlink()
            print(f"✅ 기존 데이터베이스 파일 삭제: {db_path}")
        
        # 새 데이터베이스 생성 (테이블 구조만)
        db = ParkingDatabase()
        print("✅ 빈 데이터베이스 생성 완료")
        
        # 확인
        stats = db.get_statistics()
        print(f"\n초기화 후 기록 수: {stats.get('total_records', 0)}건")
        
        print("\n" + "="*60)
        print("✅ 데이터베이스 초기화 완료!")
        print("="*60)
        print("\n다음 단계:")
        print("1. git add data/parking_records.db")
        print("2. git commit -m 'Reset parking records database'")
        print("3. git push")
        
        return True
        
    except Exception as e:
        system_logger.error(f"데이터베이스 초기화 실패: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    try:
        success = reset_database()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n초기화가 중단되었습니다.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

