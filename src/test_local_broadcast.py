"""
로컬에서 Google Home Mini 방송 테스트 스크립트
GitHub Secrets 정보를 사용하여 실제 방송이 되는지 테스트합니다.
"""
import sys
import os
import json
from pathlib import Path

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent))

try:
    from google_assistant import GoogleAssistantBroadcaster, GoogleHomeCastBroadcaster
    from logger import system_logger
    import config
except ImportError as e:
    print(f"❌ 모듈 import 실패: {e}")
    print("\n필요한 패키지를 설치하세요:")
    print("pip install -r ../requirements.txt")
    sys.exit(1)


def load_github_secrets():
    """
    GitHub Secrets에서 정보 로드
    실제로는 .env 파일이나 환경 변수에서 로드해야 합니다.
    """
    secrets = {}
    
    # .env 파일에서 로드 시도
    env_file = Path(__file__).parent.parent / '.env'
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv(env_file)
        print(f"✅ .env 파일에서 환경 변수 로드: {env_file}")
    
    # 환경 변수에서 로드
    secrets['GOOGLE_HOME_DEVICE_NAME'] = os.getenv('GOOGLE_HOME_DEVICE_NAME', config.GOOGLE_HOME_DEVICE_NAME)
    secrets['GOOGLE_BROADCASTER_TYPE'] = os.getenv('GOOGLE_BROADCASTER_TYPE', config.GOOGLE_BROADCASTER_TYPE)
    
    # token.json 파일 확인
    token_file = Path(__file__).parent.parent / 'data' / 'token.json'
    if token_file.exists():
        secrets['HAS_TOKEN'] = True
        print(f"✅ 토큰 파일 발견: {token_file}")
    else:
        secrets['HAS_TOKEN'] = False
        print(f"⚠️ 토큰 파일 없음: {token_file}")
    
    return secrets


def test_broadcast_cast(device_name: str, message: str):
    """Chromecast 방식 테스트"""
    print("\n" + "="*60)
    print("Chromecast 방식 테스트")
    print("="*60)
    print(f"기기 이름: {device_name}")
    print(f"메시지: {message}")
    print()
    
    broadcaster = GoogleHomeCastBroadcaster(device_name=device_name)
    
    # 기기 연결
    print("🔍 Google Home 기기 검색 중...")
    if not broadcaster.connect():
        print("❌ 기기 연결 실패")
        print("\n확인 사항:")
        print("1. Google Home Mini가 같은 Wi-Fi 네트워크에 연결되어 있는지 확인")
        print("2. 방화벽이 mDNS 포트(5353)를 차단하지 않는지 확인")
        print("3. 기기 이름이 정확한지 확인 (Google Home 앱에서 확인)")
        return False
    
    print(f"✅ 기기 연결 성공: {broadcaster.device.name}")
    
    # 방송 테스트
    print("\n🔊 방송 시작...")
    success = broadcaster.speak(message)
    
    if success:
        print("✅ 방송 성공!")
        print("\n💡 Google Home Mini에서 소리가 들렸나요?")
        return True
    else:
        print("❌ 방송 실패")
        return False


def test_broadcast_assistant(device_name: str, message: str):
    """Google Assistant SDK 방식 테스트"""
    print("\n" + "="*60)
    print("Google Assistant SDK 방식 테스트")
    print("="*60)
    print(f"기기 이름: {device_name}")
    print(f"메시지: {message}")
    print()
    
    broadcaster = GoogleAssistantBroadcaster()
    
    # 인증
    print("🔐 Google OAuth 인증 중...")
    if not broadcaster.authenticate():
        print("❌ 인증 실패")
        print("\n확인 사항:")
        print("1. client_secret.json 파일이 프로젝트 루트에 있는지 확인")
        print("2. data/token.json 파일이 있는지 확인")
        return False
    
    print("✅ 인증 성공")
    
    # 방송 테스트
    print("\n🔊 방송 시작...")
    success = broadcaster.broadcast(message, device_name=device_name)
    
    if success:
        print("✅ 방송 성공!")
        print("\n💡 Google Home Mini에서 소리가 들렸나요?")
        return True
    else:
        print("❌ 방송 실패")
        return False


def list_devices():
    """사용 가능한 Chromecast 기기 목록"""
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
    
    parser = argparse.ArgumentParser(
        description='로컬에서 Google Home Mini 방송 테스트',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예제:
  # 기기 목록 확인
  python test_local_broadcast.py --list
  
  # Chromecast 방식 테스트
  python test_local_broadcast.py --method cast --device "거실" --message "테스트입니다"
  
  # Google Assistant SDK 방식 테스트
  python test_local_broadcast.py --method assistant --device "거실" --message "테스트입니다"
        """
    )
    
    parser.add_argument('--list', action='store_true', help='사용 가능한 기기 목록 확인')
    parser.add_argument('--method', choices=['cast', 'assistant'], 
                       default='cast', help='테스트 방법 선택 (기본값: cast)')
    parser.add_argument('--device', type=str, help='Google Home 기기 이름')
    parser.add_argument('--message', type=str, 
                       default='안녕하세요. Google Home Mini 방송 테스트입니다.',
                       help='테스트할 메시지')
    
    args = parser.parse_args()
    
    # 기기 목록 확인
    if args.list:
        list_devices()
        return
    
    # GitHub Secrets 정보 로드
    secrets = load_github_secrets()
    
    # 기기 이름 설정
    device_name = args.device or secrets.get('GOOGLE_HOME_DEVICE_NAME', '홈')
    broadcaster_type = secrets.get('GOOGLE_BROADCASTER_TYPE', 'cast')
    
    print("\n" + "="*60)
    print("로컬 방송 테스트")
    print("="*60)
    print(f"기기 이름: {device_name}")
    print(f"방송 타입: {broadcaster_type}")
    print(f"메시지: {args.message}")
    print("="*60)
    
    # 테스트 실행
    if args.method == 'cast' or broadcaster_type == 'cast':
        success = test_broadcast_cast(device_name, args.message)
    else:
        success = test_broadcast_assistant(device_name, args.message)
    
    if success:
        print("\n" + "="*60)
        print("✅ 테스트 완료!")
        print("="*60)
        print("\n💡 Google Home Mini에서 소리가 들렸다면 성공입니다!")
    else:
        print("\n" + "="*60)
        print("❌ 테스트 실패")
        print("="*60)
        print("\n문제 해결:")
        print("1. .env 파일에 GOOGLE_HOME_DEVICE_NAME 설정 확인")
        print("2. Google Home Mini가 같은 네트워크에 있는지 확인")
        print("3. --list 옵션으로 기기 이름 확인")
    
    return 0 if success else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n테스트가 중단되었습니다.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

