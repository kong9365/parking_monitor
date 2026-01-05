"""
Google Assistant OAuth 토큰 생성 스크립트
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google_assistant import GoogleAssistantBroadcaster

def main():
    print("\n" + "="*50)
    print("Google Assistant OAuth 토큰 생성")
    print("="*50 + "\n")
    
    print("브라우저가 자동으로 열립니다.")
    print("Google 계정으로 로그인하고 권한을 허용해주세요.\n")
    
    broadcaster = GoogleAssistantBroadcaster()
    
    if broadcaster.authenticate():
        print("\n" + "="*50)
        print("[성공] 인증 완료!")
        print("="*50)
        print(f"\n토큰 파일 생성됨: {broadcaster.token_path}")
        print("\n다음 단계:")
        print("1. data/token.json 파일 내용을 복사하세요")
        print("2. GitHub Secrets에 GOOGLE_TOKEN_JSON으로 저장하세요")
        print("\n")
        return 0
    else:
        print("\n[실패] 인증에 실패했습니다.")
        return 1

if __name__ == '__main__':
    sys.exit(main())

