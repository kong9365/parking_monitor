"""
Real Parking 입출차 모니터링 시스템 (알림 기능 포함)
메인 실행 파일
"""
import sys
import argparse
from datetime import datetime
from parking_scraper import ParkingScraper
from database import ParkingDatabase
from notification_manager import NotificationManager
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
    # 명령줄 인자 파싱
    parser = argparse.ArgumentParser(description='Real Parking 입출차 모니터링 시스템')
    parser.add_argument('--no-notification', action='store_true', help='알림 기능 비활성화')
    parser.add_argument('--broadcaster', choices=['assistant', 'cast'], default='cast',
                        help='방송 타입 선택 (assistant: Google Assistant SDK, cast: Chromecast)')
    args = parser.parse_args()
    
    try:
        system_logger.info("=" * 50)
        system_logger.info("Real Parking 입출차 모니터링 시스템 시작")
        system_logger.info("=" * 50)
        
        # 데이터베이스 초기화
        db = ParkingDatabase()
        
        # 알림 관리자 초기화 (옵션)
        notification_manager = None
        if not args.no_notification:
            system_logger.info(f"알림 기능 활성화 (방송 타입: {args.broadcaster})")
            notification_manager = NotificationManager(db, args.broadcaster)
            
            # 방송기 초기화
            if not notification_manager.initialize_broadcaster():
                system_logger.warning("방송기 초기화 실패 - 알림 없이 계속 진행")
                notification_manager = None
        
        # 스크래퍼 시작
        with ParkingScraper() as scraper:
            # 로그인
            if not scraper.login():
                system_logger.error("로그인 실패")
                return 1
            
            # 포인트 정보 조회
            points = scraper.get_points_info()
            system_logger.info(f"[포인트 정보] 기본: {points['basic']}P / 구매: {points['purchase']}P")
            
            # 입출차 조회 페이지 이동
            if not scraper.navigate_to_inout_list():
                system_logger.error("입출차 조회 페이지 이동 실패")
                return 1
            
            # 오늘 데이터 조회
            system_logger.info("오늘의 입출차 데이터 조회 중...")
            records = scraper.get_today_data()
            
            # 결과 출력
            display_records(records)
            
            # 포인트 정보 출력
            print(f"\n{'='*100}")
            print(f"💰 포인트 정보")
            print(f"{'='*100}")
            print(f"  기본 선입 포인트: {points['basic']:,}P")
            print(f"  구매 선입 포인트: {points['purchase']:,}P")
            print(f"  총 포인트: {points['basic'] + points['purchase']:,}P")
            print(f"{'='*100}\n")
            
            # 알림 처리
            if notification_manager and records:
                system_logger.info("변경 감지 및 알림 전송 중...")
                # 현재 포인트를 notification_manager에 전달
                notification_manager.set_current_points(points['basic'])
                stats = notification_manager.process_new_records(records)
                
                print("\n[알림 처리 결과]")
                print(f"  새로운 입차: {stats['entries']}건")
                print(f"  새로운 출차: {stats['exits']}건")
                print(f"  전송된 알림: {stats['notifications']}건")
                print()
            
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

