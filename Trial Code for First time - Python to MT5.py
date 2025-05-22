import MetaTrader5 as mt5
from datetime import datetime

# === 1. RETCODE DICTIONARY ===
RETCODE_DICT = {
    10009: "TRADE_RETCODE_DONE - Trade executed successfully",
    10008: "TRADE_RETCODE_PLACED - Order placed (e.g. pending order)",
    10010: "TRADE_RETCODE_DONE_PARTIAL - Order partially filled",
    10004: "TRADE_RETCODE_REJECT - Order rejected by the broker",
    10006: "TRADE_RETCODE_INVALID_VOLUME - Invalid lot size",
    10016: "TRADE_RETCODE_INVALID_PRICE - Invalid price",
    10017: "TRADE_RETCODE_INVALID_STOPS - Invalid SL/TP (too close)",
    10018: "TRADE_RETCODE_TRADE_DISABLED - Trading disabled for symbol",
    10019: "TRADE_RETCODE_MARKET_CLOSED - Market is currently closed",
    10020: "TRADE_RETCODE_NO_MONEY - Not enough funds",
    10030: "TRADE_RETCODE_PRICE_CHANGED - Price moved outside deviation",
    10031: "TRADE_RETCODE_PRICE_OFF - No price available (offline?)",
    10032: "TRADE_RETCODE_INVALID_STOPS - SL/TP too close or invalid",
}

# 2. MT5 CONNECTION 
if not mt5.initialize():
    print("Initialization failed. Error:", mt5.last_error())
    quit()

print("MT5 Version:", mt5.version())

symbol = "EURUSD"

if not mt5.symbol_select(symbol, True):
    print(f"Failed to select symbol: {symbol}")
    mt5.shutdown()
    quit()

tick = mt5.symbol_info_tick(symbol)
if tick is None:
    print("Failed to get tick data.")
    mt5.shutdown()
    quit()

# ORDER PARAMETERS
price = tick.ask
lot_size = 0.5
deviation = 50

request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot_size,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    "deviation": deviation,
    "magic": 234000,
    "comment": "MT5 Buy Trial",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC
}

# ORDER REQUEST 
result = mt5.order_send(request)

if result is None:
    print("Order failed: No response. Error:", mt5.last_error())
    mt5.shutdown()
    quit()

#RETCODE DICT
retcode_msg = RETCODE_DICT.get(result.retcode, f"Unknown retcode: {result.retcode}")
print(f"\nTrade Result Code: {result.retcode}")
print(f"Message: {retcode_msg}")

if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("Order was not fully executed. Review details above.")
    mt5.shutdown()
    quit()

#ORDER DETAILS 
print(f" ORDER SUCCESSFUL")
print(f"- Symbol: {symbol}")
print(f"- Entry Price: {result.price}")
print(f"- Lot Size: {lot_size}")
print(f"- Comment: {request['comment']}")

mt5.shutdown()
