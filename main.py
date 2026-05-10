import time
from pybit.unified_trading import HTTP

# 1. Твои ключи
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_KEY"

# 2. Инициализация (демо-режим с принудительным доменом)
session = HTTP(
    testnet=False, 
    demo=True, 
    api_key=API_KEY,
    api_secret=API_SECRET,
    domain="bybit" 
)

def get_precision(symbol):
    """Узнает, сколько знаков после запятой разрешает биржа."""
    instr = session.get_instruments_info(category="linear", symbol=symbol)
    qty_step = instr['result']['list'][0]['lotSizeFilter']['qtyStep']
    qty_prec = len(qty_step.split('.')[-1]) if '.' in qty_step else 0
    return qty_prec

def pro_active_hunter(symbol="BTCUSDT", drop_percent=4.5, profit_percent=6.5, usdt_budget=900):
    """
    Активный бот: сам следит за ценой и пробивает любые обрывы связи.
    """
    print("📊 Включаю Pro-анализ рынка...")
    
    # Пытаемся получить начальную цену (с защитой от обрыва связи)
    while True:
        try:
            ticker = session.get_tickers(category="linear", symbol=symbol)
            start_price = float(ticker['result']['list'][0]['lastPrice'])
            break
        except Exception:
            print("⏳ Ищу связь с биржей...")
            time.sleep(2)

    # 1. РАССЧИТЫВАЕМ ИДЕАЛЬНЫЕ ТОЧКИ НА ОСНОВЕ АНАЛИЗА
    buy_price = start_price * (1 - drop_percent / 100)
    qty_prec = get_precision(symbol)
    qty = round(usdt_budget / buy_price, qty_prec)
    
    print(f"📍 Старт: {start_price:.2f} USDT")
    print(f"⬇️ Жду падения до поддержки: {buy_price:.2f} USDT")
    
    # 2. РЕЖИМ ОХОТЫ (Ожидание падения цены)
    while True:
        try:
            ticker = session.get_tickers(category="linear", symbol=symbol)
            current_price = float(ticker['result']['list'][0]['lastPrice'])
            
            if current_price <= buy_price:
                print(f"🚨 ЦЕНА ДОСТИГЛА ДНА ({current_price})! НАЧИНАЮ ПОКУПКУ!")
                
                # 3. НЕПРОБИВАЕМЫЙ ЦИКЛ ПОКУПКИ (Стучим, пока не купим)
                while True:
                    try:
                        response = session.place_order(
                            category="linear",
                            symbol=symbol,
                            side="Buy",
                            orderType="Market",
                            qty=str(qty),
                            timeInForce="GTC"
                        )
                        print(f"✅ ПОКУПКА УСПЕШНА! Монеты в кармане.")
                        break # Выходим из цикла пробивания VPN
                    except Exception as e:
                        print(f"⚠️ Ошибка сети при покупке ({e}). Стучусь снова через 1 сек...")
                        time.sleep(1)
                        
                break # Выходим из режима ожидания дна, идем продавать
                
        except Exception:
             # Если интернет пропал во время слежки, просто ждем и пробуем снова
             time.sleep(2)
             
        time.sleep(3) # Проверяем цену каждые 3 секунды

    # 4. РАССЧИТЫВАЕМ ЦЕЛЬ ДЛЯ ПРОДАЖИ
    sell_price = buy_price * (1 + profit_percent / 100)
    print(f"⬆️ Перехожу в режим фиксации прибыли. Жду роста до: {sell_price:.2f} USDT")

    # 5. РЕЖИМ ОЖИДАНИЯ ПРОФИТА
    while True:
        try:
            ticker = session.get_tickers(category="linear", symbol=symbol)
            current_price = float(ticker['result']['list'][0]['lastPrice'])
            
            if current_price >= sell_price:
                print(f"🔥 ЦЕНА НА ПИКЕ ({current_price})! ФИКСИРУЮ ПРИБЫЛЬ!")
                
                # 6. НЕПРОБИВАЕМЫЙ ЦИКЛ ПРОДАЖИ
                while True:
                    try:
                        session.place_order(
                            category="linear",
                            symbol=symbol,
                            side="Sell", # Продаем наши лонги (закрываем позицию)
                            orderType="Market",
                            qty=str(qty),
                            reduceOnly=True, # Важный флаг: только закрыть текущую
сделку
                            timeInForce="GTC"
                        )
                        print(f"🏆 СДЕЛКА ЗАКРЫТА С ПРОФИТОМ! Охота завершена.")
                        return # Конец программы
                    except Exception as e:
                        print(f"⚠️ Ошибка сети при продаже ({e}). Стучусь снова через 1 сек...")
                        time.sleep(1)
                        
        except Exception:
             time.sleep(2)
             
        time.sleep(3)

if name == "main":
    # Запускаем нашего непробиваемого бота с выверенными процентами
    pro_active_hunter("BTCUSDT", drop_percent=4.5, profit_percent=6.5, usdt_budget=900)