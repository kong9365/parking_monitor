"""
연결 테스트 스크립트
Real Parking 웹사이트 접속 및 로그인 테스트
"""
import sys
import io
from parking_scraper import ParkingScraper
from logger import system_logger

# Windows 콘솔 인코딩 문제 해결
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def test_connection():
    """연결 테스트"""
    print("\n" + "="*50)
    print("Real Parking 연결 테스트")
    print("="*50 + "\n")
    
    try:
        with ParkingScraper() as scraper:
            # 로그인 테스트
            print("1. 로그인 테스트...")
            if scraper.login():
                print("   [OK] 로그인 성공\n")
            else:
                print("   [FAIL] 로그인 실패\n")
                return False
            
            # 입출차 페이지 이동 테스트
            print("2. 입출차 조회 페이지 이동 테스트...")
            if scraper.navigate_to_inout_list():
                print("   [OK] 페이지 이동 성공\n")
            else:
                print("   [FAIL] 페이지 이동 실패\n")
                return False
            
            # 데이터 조회 테스트
            print("3. 데이터 조회 테스트...")
            records = scraper.get_today_data()
            print(f"   [OK] {len(records)}건의 데이터 조회 성공\n")
            
            if records:
                print("샘플 데이터:")
                sample = records[0]
                print(f"  차량번호: {sample.get('car_number')}")
                print(f"  이름: {sample.get('name')}")
                print(f"  구분: {sample.get('type')}")
                print(f"  입차시간: {sample.get('entry_time')}")
                print()
            
            print("="*50)
            print("[OK] 모든 테스트 통과!")
            print("="*50 + "\n")
            return True
    
    except Exception as e:
        print(f"\n[FAIL] 테스트 실패: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    test_connection()

