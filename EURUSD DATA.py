import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

if not mt5.initialize():
    print("MT5 Initilisation failed: ", mt5.last_error() )
    quit()


#EURUSD  

h1_data = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_H1, datetime.now(), 50_000)
h4_data = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_H4, datetime.now(), 50_000)

"""
Output: ('time', 'open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume')

"""
mt5.shutdown()


h1_df = pd.DataFrame(h1_data)
h1_df["time"] = pd.to_datetime(h1_df["time"], unit = "s")
h1_df.to_csv("EURUSD_H1.csv", index = False)
print("Saved EURUSD 1H tf data to EURUSD_H1_df.csv")

h4_df = pd.DataFrame(h4_data)
h4_df["time"] = pd.to_datetime(h4_df["time"], unit = "s")
h4_df.to_csv("EURUSD_H4.csv", index = False)
print("Saved EURUSD 4H tf data to EURUSD_H4_df.csv")