import time
import pyupbit
import datetime
import requests

access = "Ml3AeEDbl8OnRBrCp9yj2ybigDUg4vMaqjxz9e16"
secret = "YIerDg2gQCQHnrxgxNVtULH9SxtNtc2rf0fOcRVe"
myToken = "xoxb-3051121950740-3048854151139-beSwXjjKFXq169mjbIecuzFT"
coinlist = {'KRW-BTC', 'KRW-ETH', 'KRW-NEO', 'KRW-MTL', 'KRW-LTC', 'KRW-XRP',
 'KRW-ETC', 'KRW-OMG', 'KRW-SNT', 'KRW-WAVES', 'KRW-XEM', 'KRW-QTUM', 'KRW-LSK',
  'KRW-STEEM', 'KRW-XLM', 'KRW-ARDR', 'KRW-ARK', 'KRW-STORJ', 'KRW-GRS', 'KRW-REP',
   'KRW-ADA', 'KRW-SBD', 'KRW-POWR', 'KRW-BTG', 'KRW-ICX', 'KRW-EOS', 'KRW-TRX', 'KRW-SC',
    'KRW-ONT', 'KRW-ZIL', 'KRW-POLY', 'KRW-ZRX', 'KRW-LOOM', 'KRW-BCH', 'KRW-BAT', 'KRW-IOST', 'KRW-RFR', 'KRW-CVC', 'KRW-IQ', 
    'KRW-IOTA', 'KRW-MFT', 'KRW-ONG', 'KRW-GAS', 'KRW-UPP', 'KRW-ELF', 'KRW-KNC', 'KRW-BSV', 'KRW-THETA', 'KRW-QKC', 'KRW-BTT',
     'KRW-MOC', 'KRW-ENJ', 'KRW-TFUEL', 'KRW-MANA', 'KRW-ANKR', 'KRW-AERGO', 'KRW-ATOM', 'KRW-TT', 'KRW-CRE', 'KRW-MBL',
      'KRW-WAXP', 'KRW-HBAR', 'KRW-MED', 'KRW-MLK', 'KRW-STPT', 'KRW-ORBS', 'KRW-VET', 'KRW-CHZ', 'KRW-STMX', 'KRW-DKA',
       'KRW-HIVE', 'KRW-KAVA', 'KRW-AHT', 'KRW-LINK', 'KRW-XTZ', 'KRW-BORA', 'KRW-JST', 'KRW-CRO', 'KRW-TON', 'KRW-SXP',
        'KRW-HUNT', 'KRW-PLA', 'KRW-DOT', 'KRW-SRM', 'KRW-MVL', 'KRW-STRAX', 'KRW-AQT', 'KRW-GLM', 'KRW-SSX', 'KRW-META',
         'KRW-FCT2', 'KRW-CBK', 'KRW-SAND', 'KRW-HUM', 'KRW-DOGE', 'KRW-STRK', 'KRW-PUNDIX', 'KRW-FLOW', 'KRW-DAWN', 'KRW-AXS',
          'KRW-STX', 'KRW-XEC', 'KRW-SOL', 'KRW-MATIC', 'KRW-NU', 'KRW-AAVE', 'KRW-1INCH', 'KRW-ALGO', 'KRW-NEAR', 'KRW-WEMIX'}

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma20(ticker):
    """20일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=20)
    ma20 = df['close'].rolling(20).mean().iloc[-1]
    return ma20

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
# 시작 메세지 슬랙 전송
post_message(myToken,"#maslack", "autotrade start")

while True:
    for i in coinlist:
        try:
            now = datetime.datetime.now()
            start_time = get_start_time(i)
            end_time = start_time + datetime.timedelta(days=1)

            if  start_time < now < end_time - datetime.timedelta(seconds=10):
                target_price = get_target_price(i, 0.6)
                ma20 = get_ma20(i)
                current_price = get_current_price(i)
                if target_price < current_price and ma20 < current_price:
                    
                    krw = get_balance("KRW")
                    if krw > 5000:
                        buy_result = upbit.buy_market_order(i, krw*0.9995)
                        post_message(myToken,"#maslack", " 매수 : " +str(buy_result))
            else:
                btc = get_balance("BTC")
                if btc > 0.00008:
                    pass
                        #sell_result = upbit.sell_market_order(i, btc*0.9995)
                        #post_message(myToken,"#maslack", " buy : " +str(sell_result))
            time.sleep(1)
        except Exception as e:
            print(e)
            post_message(myToken,"#maslack", e)
            time.sleep(1)