"""
Google Assistant SDK 테스트 스크립트
실제 Google Home Mini에서 방송이 되는지 테스트합니다.
"""
import sys
import os
from pathlib import Path

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent))

# 선택적 import
try:
    from google_assistant import GoogleAssistantBroadcaster, GoogleHomeCastBroadcaster
    from logger import system_logger
    import config
except ImportError as e:
    print(f"❌ 모듈 import 실패: {e}")
    print("\n필요한 패키지를 설치하세요:")
    print("pip install -r ../requirements.txt")
    sys.exit(1)


def test_cast_broadcaster():
    """Chromecast 방식 테스트 (더 간단하고 안정적)"""
    print("\n" + "="*60)
    print("Chromecast 방식 테스트 (pychromecast + gTTS)")
    print("="*60)
    
    broadcaster = GoogleHomeCastBroadcaster()
    
    # 기기 연결
    print(f"\nGoogle Home 기기 연결 시도: {broadcaster.device_name}")
    if not broadcaster.connect():
        print("❌ 기기 연결 실패")
        return False
    
    # 테스트 메시지 방송
    test_messages = [
        "안녕하세요. 테스트 메시지입니다.",
        "세대 차량 39가5514가 후문 입구로 입차하였습니다.",
        "방문차량 106누4166, 이소영님이 후문 입구로 입차하셨습니다."
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n[{i}/{len(test_messages)}] 방송 테스트: {message}")
        success = broadcaster.speak(message)
        if success:
            print("✅ 방송 성공")
        else:
            print("❌ 방송 실패")
        
        import time
        time.sleep(2)  # 다음 방송 전 대기
    
    print("\n✅ Chromecast 방식 테스트 완료")
    return True


def test_assistant_broadcaster():
    """Google Assistant SDK 방식 테스트"""
    print("\n" + "="*60)
    print("Google Assistant SDK 방식 테스트")
    print("="*60)
    
    broadcaster = GoogleAssistantBroadcaster()
    
    # 인증
    print("\nGoogle OAuth 인증 시도...")
    if not broadcaster.authenticate():
        print("❌ 인증 실패")
        print("\n인증을 위해서는:")
        print("1. Google Cloud Console에서 프로젝트 생성")
        print("2. Google Assistant API 활성화")
        print("3. OAuth 2.0 클라이언트 ID 생성")
        print("4. client_secret.json 파일을 프로젝트 루트에 배치")
        return False
    
    print("✅ 인증 성공")
    
    # 테스트 메시지 방송
    test_messages = [
        "안녕하세요. Google Assistant SDK 테스트입니다.",
        "세대 차량 39가5514가 후문 입구로 입차하였습니다."
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n[{i}/{len(test_messages)}] 방송 테스트: {message}")
        success = broadcaster.broadcast(message)
        if success:
            print("✅ 방송 성공")
        else:
            print("❌ 방송 실패")
        
        import time
        time.sleep(2)
    
    print("\n✅ Google Assistant SDK 방식 테스트 완료")
    return True


def list_available_devices():
    """사용 가능한 Chromecast 기기 목록 출력"""
    print("\n" + "="*60)
    print("사용 가능한 Chromecast 기기 검색 중...")
    print("="*60)
    
    try:
        import pychromecast
        
        chromecasts, browser = pychromecast.get_listed_chromecasts()
        
        if not chromecasts:
            print("❌ 사용 가능한 Chromecast 기기를 찾을 수 없습니다.")
            print("\n확인 사항:")
            print("1. Google Home Mini가 같은 네트워크에 연결되어 있는지 확인")
            print("2. 방화벽이 mDNS 포트(5353)를 차단하지 않는지 확인")
            return
        
        print(f"\n✅ {len(chromecasts)}개의 기기를 찾았습니다:\n")
        for i, cast in enumerate(chromecasts, 1):
            print(f"[{i}] {cast.device.friendly_name}")
            print(f"    타입: {cast.device.cast_type}")
            print(f"    IP: {cast.host}")
            print()
        
        browser.stop_discovery()
        
    except ImportError:
        print("❌ pychromecast 모듈이 설치되지 않았습니다.")
        print("설치 방법: pip install pychromecast")
    except Exception as e:
        print(f"❌ 기기 검색 중 오류: {str(e)}")


def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Google Assistant SDK 테스트')
    parser.add_argument('--method', choices=['cast', 'assistant', 'list'], 
                       default='cast', help='테스트 방법 선택')
    parser.add_argument('--device', type=str, help='Google Home 기기 이름')
    parser.add_argument('--message', type=str, help='테스트할 메시지')
    
    args = parser.parse_args()
    
    # 기기 이름 설정
    if args.device:
        os.environ['GOOGLE_HOME_DEVICE_NAME'] = args.device
    
    if args.method == 'list':
        list_available_devices()
        return
    
    if args.method == 'cast':
        # Chromecast 방식 (권장)
        if args.message:
            # 단일 메시지 테스트
            broadcaster = GoogleHomeCastBroadcaster()
            if broadcaster.connect():
                broadcaster.speak(args.message)
            else:
                print("❌ 기기 연결 실패")
        else:
            test_cast_broadcaster()
    
    elif args.method == 'assistant':
        # Google Assistant SDK 방식
        if args.message:
            broadcaster = GoogleAssistantBroadcaster()
            if broadcaster.authenticate():
                broadcaster.broadcast(args.message)
            else:
                print("❌ 인증 실패")
        else:
            test_assistant_broadcaster()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n테스트가 중단되었습니다.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

