import pyupbit
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import time
import warnings

# 경고 메시지 숨기기
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# 현재 비트코인 가격 조회
current_price = pyupbit.get_current_price(['KRW-BTC'])
# ['KRW-WAXP', 'KRW-CARV', 'KRW-LSK', 'KRW-0G', 'KRW-BORA', 'KRW-PUNDIX', 'KRW-USD1', 'KRW-BAT'
# , 'KRW-HUNT', 'KRW-PENGU', 'KRW-FIL', 'KRW-BEAM', 'KRW-DOOD', 'KRW-WAVES', 'KRW-USDC', 'KRW-MOVE'
# , 'KRW-TREE', 'KRW-AERGO', 'KRW-USDT', 'KRW-2Z', 'KRW-BOUNTY', 'KRW-KAITO', 'KRW-LPT', 'KRW-BLAST'
# , 'KRW-DKA', 'KRW-ANKR', 'KRW-ALGO', 'KRW-SHIB', 'KRW-UNI', 'KRW-BIO', 'KRW-WLFI', 'KRW-TOKAMAK', 'KRW-CYBER'
# , 'KRW-DOGE', 'KRW-WLD', 'KRW-PEPE', 'KRW-HBAR', 'KRW-BCH', 'KRW-NEWT', 'KRW-SEI', 'KRW-BONK', 'KRW-JST', 'KRW-AAVE'
# , 'KRW-JTO', 'KRW-JUP', 'KRW-FLOW', 'KRW-ALT', 'KRW-LAYER', 'KRW-TRX', 'KRW-POWR', 'KRW-ATOM', 'KRW-ARKM', 'KRW-CRO'
# , 'KRW-NXPC', 'KRW-A', 'KRW-TRUMP', 'KRW-F', 'KRW-G', 'KRW-CELO', 'KRW-AERO', 'KRW-CTC', 'KRW-ANIME', 'KRW-APT', 'KRW-MOCA'
# , 'KRW-API3', 'KRW-AHT', 'KRW-EGLD', 'KRW-ERA', 'KRW-FF', 'KRW-PLUME', 'KRW-NEO', 'KRW-ETC', 'KRW-IOTA', 'KRW-IOST', 'KRW-AKT'
# , 'KRW-COW', 'KRW-VIRTUAL', 'KRW-ETH', 'KRW-IQ', 'KRW-IP', 'KRW-NEAR', 'KRW-RVN', 'KRW-AGLD', 'KRW-ID', 'KRW-IN', 'KRW-NOM'
# , 'KRW-WAL', 'KRW-PENDLE', 'KRW-BLUR', 'KRW-AWE', 'KRW-THETA', 'KRW-AXL', 'KRW-HP', 'KRW-SAND', 'KRW-WCT', 'KRW-YGG', 'KRW-AXS'
# , 'KRW-MIRA', 'KRW-SUN', 'KRW-ZBT', 'KRW-ONG', 'KRW-BTT', 'KRW-ENSO', 'KRW-ONT', 'KRW-SOMI', 'KRW-DEEP', 'KRW-STRAX', 'KRW-ICX', 'KRW-POLYX']
class UpbitDataCollector:
    """Upbit API를 활용한 데이터 수집 클래스"""
    
    def __init__(self):
        self.supported_tickers = None  

    def get_krw_tickers(self)->list[str]:
        """KRW 마켓의 모든 티커 조회"""
        try:
            self.supported_tickers = pyupbit.get_tickers(fiat="KRW")
            return self.supported_tickers
        except Exception as e:
            print(f"티커 조회 오류 : {e}")
            return []

    def get_current_prices(self,tickers):
        """현재가 조회"""
        try:
            if (isinstance(tickers,str)):
                return pyupbit.get_current_price(tickers)
            else:
                return pyupbit.get_current_price(tickers)
        except Exception as e:
            print(f"현재가 조회 오류 : {e}")
            return None

    def get_ohlcv_data(self,ticker,interval="day",count=30):
        """OHLCV 데이터 조회"""
        try:
            df = pyupbit.get_ohlcv(ticker,interval=interval,count=count)
            
            if df is not None:
                df["ticker"] = ticker
                # df["ma5"] = 0.0
                df.reset_index(inplace=True) 

                df = self.preprocess_data(df)
                
            return df
        except Exception as e:
            print(f"{ticker} OHLCV 데이터 조회 오류 : {e} ")
            return None

    def preprocess_data(self,df):       
        """데이터 전처리 함수"""
        print("=== 데이터 전처리 시작 ===")
        
        # 데이터 복사
        processed_df = df.copy()
        
        # 날짜 컬럼 처리        
        if 'index' in processed_df.columns:
            processed_df['date'] = processed_df['index']
            processed_df.drop('index', axis=1, inplace=True)
        
        # 날짜를 문자열로 변환 (DB 저장용)        
        processed_df['date_str'] = processed_df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # 기술적 지표 계산        
        ##############################################################
        #### 문제1) 종가와 시가의 차이 계산의 답안을 작성해주세요####
        processed_df["price_change"] = processed_df["close"] - processed_df["open"]
        processed_df["price_change_pct"] = ( processed_df["price_change"] / processed_df["open"] )* 100       
        processed_df["high_low_diff"] = processed_df["high"] - processed_df["low"]        


        #### 문제2) 5일 이동평균선 계산 및 결측치 처리의 답안을 작성해주세
        datas = processed_df.groupby("ticker")        
        for key,each_df in datas:
            processed_df["ma5"] = each_df["close"].rolling(window=5).mean()
            processed_df["ma5"] = processed_df["ma5"].fillna(each_df["close"])
        ##############################################################

        # 컬럼 순서 정리
        columns_order = ['date_str', 'ticker', 'open', 'high', 'low', 'close', 'volume',
                        'price_change', 'price_change_pct', 'high_low_diff', 'ma5']
        processed_df = processed_df[columns_order]

        print(f"전처리 완료 - 행 수: {len(processed_df)}")
        print(f"추가된 컬럼: price_change, price_change_pct, high_low_diff, ma5")
        
        return processed_df
    
    def get_multiple_ohlcv(self,tickers,interval="day",count=30,delay=0.1):
        """여러 티커의 OHLCV 데이터 일괄 조회"""
        all_data = []
        for ticker in tickers:
            print(f"{ticker} 데이터 수집중 ...")            
            data = self.get_ohlcv_data(ticker,interval,count)            
            if data is not None:
                all_data.append(data)
            time.sleep(delay)
        
        if all_data:
            # 반환형은 pandas.core.frame.DataFrame 인것으로 보임
            return pd.concat(all_data)
        return pd.DataFrame()

    def display(self,groupby="ticker",count=100):
        line_with = len(self.ohlcv_data.columns) * 13
        for key,each_df in self.ohlcv_data.groupby(groupby):
            print("="*line_with)
            print(each_df.head(count))
        print("="*line_with)  
        return self.ohlcv_data,self.current_pricea

    def print_datafram(self,print_datafram)->None:
        # print_datafram["date"] = pd.to_datetime(print_datafram['date'])
        print(print_datafram)
        # for index, row in print_datafram.iterrows():            
        #     print(f"{row["date"].strftime('%Y-%m-%d %H:%M:%S')} {row["ticker"]} {row["open"]} {row["high"]} {row["low"]} {row["close"]} {row["price_change"]} {row["price_change_pct"]} {row["high_low_diff"]} {row["ma5"]}")
            

    def collect_market_data(self,count=30):
        """시장 데이터 수집 함수"""
        major_tickers = ['KRW-PUNDIX', 'KRW-USD1', 'KRW-BAT']
        
        print(f"\n분석 대상 티커 : {major_tickers}")

        self.current_pricea = self.get_current_prices(major_tickers)
        print(f"\n현재가 정보:")
        for ticker,price in self.current_pricea.items():
            print(f"{ticker}: {price:,}원")
        
        print(f"\nOHLCV 데이터 수집 중...")
        self.ohlcv_data = self.get_multiple_ohlcv(tickers=major_tickers,count=count)
        
        print(f"수집된 데이터 행 수 : {len(self.ohlcv_data)}")
        print(f"데이터 컬럼 : {list(self.ohlcv_data.columns)}")

        return self.ohlcv_data,self.current_pricea

    def collect_market(self,count=30):
        """self를 반환해서 collect_market_data().display() 처럼 chain을 가능하게 하기 위함"""
        self.collect_market_data(count)
        return self

def create_database():
    """SQLite 데이터베이스 생성 함수"""
    conn = sqlite3.connect("crypto_data.db")
    cursor = conn.cursor()
    return conn
def save_to_database(df):
    """데이터베이스에 데이터 저장 함수"""
    print("=== 데이터베이스 저장 시작 ===")
    conn = create_database()

    db_df = df[['date_str', 'ticker', 'open', 'high', 'low', 'close', 'volume',
               'price_change', 'price_change_pct', 'high_low_diff', 'ma5']].copy()
    
    db_df.to_sql("crypto_ohlcv",conn,if_exists="replace",index=False)

    cursor = conn.cursor()
    cursor.execute("select count(*) from crypto_ohlcv")
    count  = cursor.fetchone()[0]

    print(f"데이터베이스에 {count}개 레코드 저장 완료")
    conn.close()
    return count 

def plot_price_trends(df):
    """가격 트렌드 시각화 함수"""
    print("=== 가격 트렌드 시각화 ===")
    # 날짜 컬럼을 datetime으로 변환
    df['date'] = pd.to_datetime(df['date_str'])

    # 고유 티커 목록
    tickers = df['ticker'].unique()
    
    # 서브플롯 생성(가로1 , 새로 3 크기로 배치하고 차트 사이즈는 가로 18인치 세로 6인치)
    fig, axes = plt.subplots(3,1,figsize=(15,8))
    axes = axes.flatten()
    
    colors = ['red','blue','green']
    for i,ticker in enumerate(tickers):
        ticker_data = df[df["ticker"]==ticker].sort_values("date")
        ticker_data['date'] = ticker_data['date'].dt.strftime('%m-%d')
        ax = axes[i]
        ax.plot(ticker_data["date"],ticker_data['close'],color=colors[0])
        ax.plot(ticker_data["date"],ticker_data['ma5'],color=colors[1])
        ax.set_title(f"{tickers} close / ma5 visualization ")
        ax.set_xlabel("date")
        ax.set_ylabel("price")
        # print(ticker_data)
    
    plt.show()

def load_from_database(table,where,orderby):
    """데이터베이스에서 데이터 로드 함수"""
    conn = sqlite3.connect("crypto_data.db")
    query = f"select * from {table} where {where} order by {orderby}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

if __name__ == "__main__":

    upbit_collector = UpbitDataCollector()
    # ohlcv_data,current_pricea = upbit_collector.collect_market(30).display(groupby="ticker",count=30)
    ohlcv_data,current_pricea = upbit_collector.collect_market_data(30)

    
    
    save_to_database(ohlcv_data)
    selectedRow = load_from_database("crypto_ohlcv","1=1"," date_str DESC ")
    upbit_collector.print_datafram(selectedRow)
    plot_price_trends(selectedRow)