"""
Real Parking 입출차 모니터링 시스템
메인 실행 파일
"""
import sys
from datetime import datetime
from parking_scraper import ParkingScraper
from database import ParkingDatabase
from logger import system_logger


def display_records(records):
    """입출차 기록 출력"""
    if not records:
        print("\n조회된 데이터가 없습니다.")
        return
    
    print(f"\n{'='*100}")
    print(f"총 {len(records)}건의 입출차 기록")
    print(f"{'='*100}")
    
    for i, record in enumerate(records, 1):
        print(f"\n[{i}] {record.get('car_number', 'N/A')}")
        print(f"  이름: {record.get('name', 'N/A')}")
        print(f"  구분: {record.get('type', 'N/A')}")
        print(f"  연락처: {record.get('phone', 'N/A')}")
        print(f"  입차: {record.get('entry_location', 'N/A')} - {record.get('entry_time', 'N/A')}")
        
        if record.get('exit_time'):
            print(f"  출차: {record.get('exit_location', 'N/A')} - {record.get('exit_time', 'N/A')}")
        else:
            print(f"  출차: 미출차")
        
        print(f"  상태: {record.get('status', 'N/A')}")
        
        if record.get('note'):
            print(f"  비고: {record.get('note')}")
    
    print(f"\n{'='*100}\n")


def main():
    """메인 실행 함수"""
    try:
        system_logger.info("=" * 50)
        system_logger.info("Real Parking 입출차 모니터링 시스템 시작")
        system_logger.info("=" * 50)
        
        # 데이터베이스 초기화
        db = ParkingDatabase()
        
        # 스크래퍼 시작
        with ParkingScraper() as scraper:
            # 로그인
            if not scraper.login():
                system_logger.error("로그인 실패")
                return 1
            
            # 입출차 조회 페이지 이동
            if not scraper.navigate_to_inout_list():
                system_logger.error("입출차 조회 페이지 이동 실패")
                return 1
            
            # 오늘 데이터 조회
            system_logger.info("오늘의 입출차 데이터 조회 중...")
            records = scraper.get_today_data()
            
            # 결과 출력
            display_records(records)
            
            # 데이터베이스에 저장
            if records:
                new_count = db.insert_records(records)
                system_logger.success(f"데이터베이스에 {new_count}건의 새 기록 저장 완료")
            
            # 통계 정보 출력
            stats = db.get_statistics()
            print("\n[데이터베이스 통계]")
            print(f"  전체 기록: {stats.get('total_records', 0)}건")
            print(f"  오늘 기록: {stats.get('today_records', 0)}건")
            print(f"  미출차: {stats.get('not_exited', 0)}건")
            print()
        
        system_logger.success("프로그램 정상 종료")
        return 0
    
    except KeyboardInterrupt:
        system_logger.info("사용자에 의해 프로그램 중단")
        return 0
    
    except Exception as e:
        system_logger.error(f"프로그램 실행 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

