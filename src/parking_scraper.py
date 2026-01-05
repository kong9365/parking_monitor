"""
Real Parking 웹 스크래핑 모듈
Playwright를 사용하여 입출차 정보를 수집합니다.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright, Page, Browser, TimeoutError as PlaywrightTimeout
import config
from logger import scraping_logger


class ParkingScraper:
    """Real Parking 웹사이트 스크래퍼"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.is_logged_in = False
        self.points_info: Dict[str, int] = {}
    
    def start(self):
        """브라우저 시작"""
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=config.HEADLESS)
            self.page = self.browser.new_page()
            self.page.set_default_timeout(config.TIMEOUT)
            scraping_logger.info("브라우저 시작 완료")
        except Exception as e:
            scraping_logger.error(f"브라우저 시작 실패: {str(e)}")
            raise
    
    def stop(self):
        """브라우저 종료"""
        try:
            if self.page:
                self.page.close()
            if self.browser:
                self.browser.close()
            if hasattr(self, 'playwright'):
                self.playwright.stop()
            scraping_logger.info("브라우저 종료 완료")
        except Exception as e:
            scraping_logger.error(f"브라우저 종료 중 오류: {str(e)}")
    
    def get_points_info(self) -> Dict[str, int]:
        """
        포인트 정보 조회
        
        Returns:
            포인트 정보 딕셔너리 {'basic': 기본 포인트, 'purchase': 구매 포인트}
        """
        try:
            # 포인트 정보는 오른쪽 상단에 표시됨
            # 예: "기본 선입 포인트 : 6000" "구매 선입 포인트 : 0"
            
            points_info = self.page.evaluate('''() => {
                const result = {
                    basic: 0,
                    purchase: 0
                };
                
                // Settings 드롭다운 메뉴에서 포인트 정보 찾기
                const dropdownText = document.body.innerText;
                
                // 기본 선입 포인트 추출
                const basicMatch = dropdownText.match(/기본 선입 포인트[\\s:]+([0-9]+)/);
                if (basicMatch) {
                    result.basic = parseInt(basicMatch[1]);
                }
                
                // 구매 선입 포인트 추출
                const purchaseMatch = dropdownText.match(/구매 선입 포인트[\\s:]+([0-9]+)/);
                if (purchaseMatch) {
                    result.purchase = parseInt(purchaseMatch[1]);
                }
                
                return result;
            }''')
            
            self.points_info = points_info
            scraping_logger.info(
                f"포인트 정보 조회 완료 - 기본: {points_info['basic']}, 구매: {points_info['purchase']}"
            )
            return points_info
        
        except Exception as e:
            scraping_logger.error(f"포인트 정보 조회 실패: {str(e)}")
            return {'basic': 0, 'purchase': 0}
    
    def login(self) -> bool:
        """
        Real Parking 로그인
        
        Returns:
            로그인 성공 여부
        """
        try:
            scraping_logger.info("로그인 시도 중...")
            
            # 로그인 페이지 접속
            self.page.goto(config.PARKING_URL)
            scraping_logger.info(f"로그인 페이지 접속: {config.PARKING_URL}")
            
            # jQuery를 사용하여 값 설정 및 로그인
            self.page.evaluate(f'''() => {{
                $('#userid').val('{config.PARKING_USER_ID}');
                $('#userpw').val('{config.PARKING_PASSWORD}');
                $('#autoLogin').prop('checked', true);
            }}''')
            
            scraping_logger.info("로그인 정보 입력 완료")
            
            # 로그인 버튼 클릭
            self.page.evaluate('''() => {
                $('#btn_login').click();
            }''')
            
            scraping_logger.info("로그인 버튼 클릭")
            
            # 페이지 로드 대기 (최대 10초)
            try:
                # 5초 대기
                self.page.wait_for_timeout(5000)
                
                # 로그인 성공 확인 (URL 변경 또는 특정 요소 확인)
                current_url = self.page.url
                
                # 콘솔 메시지 확인
                console_messages = self.page.evaluate('''() => {
                    return window.console_messages || [];
                }''')
                
                # URL이 변경되었거나 로그인 페이지가 아니면 성공
                if current_url != config.PARKING_URL and not current_url.endswith('/'):
                    self.is_logged_in = True
                    scraping_logger.success(f"로그인 성공 - 현재 URL: {current_url}")
                    return True
                
                # 페이지에 로그인 후 요소가 있는지 확인
                try:
                    # 사용자 이름이 표시되는 요소 확인
                    user_element = self.page.query_selector('a[href="#"]:has-text("a01045429365")')
                    if user_element:
                        self.is_logged_in = True
                        scraping_logger.success(f"로그인 성공 - 사용자 요소 확인")
                        return True
                except:
                    pass
                
                scraping_logger.error(f"로그인 실패 - 현재 URL: {current_url}")
                return False
            except Exception as e:
                scraping_logger.error(f"로그인 확인 중 오류: {str(e)}")
                return False
        
        except Exception as e:
            scraping_logger.error(f"로그인 중 오류 발생: {str(e)}")
            return False
    
    def navigate_to_inout_list(self) -> bool:
        """
        입출차 조회 페이지로 이동
        
        Returns:
            이동 성공 여부
        """
        try:
            if not self.is_logged_in:
                scraping_logger.error("로그인이 필요합니다")
                return False
            
            inout_url = f"{config.PARKING_URL.rstrip('/')}/pay/inoutList"
            self.page.goto(inout_url)
            scraping_logger.info("입출차 조회 페이지 이동 완료")
            
            # 페이지 로드 대기
            self.page.wait_for_load_state('networkidle')
            return True
        
        except Exception as e:
            scraping_logger.error(f"페이지 이동 중 오류: {str(e)}")
            return False
    
    def get_parking_data(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        입출차 데이터 조회
        
        Args:
            start_date: 시작 날짜 (YYYY-MM-DD 형식, 기본값: 오늘)
            end_date: 종료 날짜 (YYYY-MM-DD 형식, 기본값: 오늘)
        
        Returns:
            입출차 데이터 리스트
        """
        try:
            if not self.is_logged_in:
                scraping_logger.error("로그인이 필요합니다")
                return []
            
            # 기본값 설정
            if not start_date:
                start_date = datetime.now().strftime(config.DATE_FORMAT)
            if not end_date:
                end_date = start_date
            
            scraping_logger.info(f"입출차 데이터 조회 시작: {start_date} ~ {end_date}")
            
            # 날짜 설정
            self.page.evaluate(f'''() => {{
                const inputs = document.querySelectorAll('input[type="text"]');
                if (inputs.length >= 3) {{
                    inputs[1].value = '{start_date}';
                    inputs[2].value = '{end_date}';
                }}
            }}''')
            
            scraping_logger.info("날짜 설정 완료")
            
            # 검색 버튼 클릭
            search_button = self.page.query_selector('button img[src*="bt_search"]')
            if search_button:
                search_button.click()
                scraping_logger.info("검색 버튼 클릭")
                
                # 결과 로드 대기
                self.page.wait_for_timeout(2000)
            
            # 데이터 파싱
            data = self._parse_table_data()
            scraping_logger.success(f"입출차 데이터 {len(data)}건 조회 완료")
            
            return data
        
        except Exception as e:
            scraping_logger.error(f"데이터 조회 중 오류: {str(e)}")
            return []
    
    def _parse_table_data(self) -> List[Dict[str, Any]]:
        """
        테이블 데이터 파싱
        
        Returns:
            파싱된 데이터 리스트
        """
        try:
            # JavaScript로 테이블 데이터 추출
            data = self.page.evaluate('''() => {
                const rows = document.querySelectorAll('tbody tr');
                const result = [];
                
                for (const row of rows) {
                    const cells = row.querySelectorAll('td');
                    
                    // 11개의 컬럼이 있는 행만 처리 (정상 데이터)
                    if (cells.length === 11) {
                        const carNumber = cells[1]?.innerText?.trim() || '';
                        const entryTime = cells[6]?.innerText?.trim() || '';
                        
                        // 차량번호와 입차시간이 있는 경우만 추가
                        if (carNumber && entryTime) {
                            result.push({
                                no: cells[0]?.innerText?.trim() || '',
                                car_number: carNumber,
                                name: cells[2]?.innerText?.trim() || '',
                                type: cells[3]?.innerText?.trim() || '',
                                phone: cells[4]?.innerText?.trim() || '',
                                entry_location: cells[5]?.innerText?.trim() || '',
                                entry_time: entryTime,
                                exit_location: cells[7]?.innerText?.trim() || '',
                                exit_time: cells[8]?.innerText?.trim() || '',
                                status: cells[9]?.innerText?.trim() || '',
                                note: cells[10]?.innerText?.trim() || ''
                            });
                        }
                    }
                }
                
                return result;
            }''')
            
            scraping_logger.info(f"테이블에서 {len(data)}건의 데이터 파싱 완료")
            return data
        
        except Exception as e:
            scraping_logger.error(f"테이블 파싱 중 오류: {str(e)}")
            return []
    
    def get_today_data(self) -> List[Dict[str, Any]]:
        """
        오늘 입출차 데이터 조회
        
        Returns:
            오늘의 입출차 데이터 리스트
        """
        today = datetime.now().strftime(config.DATE_FORMAT)
        return self.get_parking_data(today, today)
    
    def get_recent_days_data(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        최근 N일간의 입출차 데이터 조회
        
        Args:
            days: 조회할 일수
        
        Returns:
            입출차 데이터 리스트
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days-1)
        
        return self.get_parking_data(
            start_date.strftime(config.DATE_FORMAT),
            end_date.strftime(config.DATE_FORMAT)
        )
    
    def __enter__(self):
        """컨텍스트 매니저 진입"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """컨텍스트 매니저 종료"""
        self.stop()

