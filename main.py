from pycoingecko import CoinGeckoAPI
from pprint import pprint
import time
import json

cg = CoinGeckoAPI()


def get_all_coin_ids(input_data):
    coin_ids = []
    for elem in input_data:
        if "-long-" not in elem["id"] and "-short-" not in elem["id"]:
            coin_ids.append(elem["id"])
    return coin_ids

def beautify_json(input_json):
    json.dumps(json.loads(input_json), sort_keys=True, indent=4)

    
"""
Candle’s body:
#1 - 2 days: 30 minutes
#3 - 30 days: 4 hours
#31 and before: 4 days
"""
"""Arguments: Coin - the crypto currency we want the candles from
              Currency - COIN/CURRENCY candles
              Time Range - 1 - 30 minutes
                           2 - 4 hours
                           3 - 4 days"""
def get_candles(coin, currency, time_range):
    time_range_real = 0
    if time_range == 1:
        time_range_real = 1
    if time_range == 2:
        time_range_real = 30
    if time_range == 3:
        time_range_real = 90
                
    api_result = cg.get_coin_ohlc_by_id(coin, currency, time_range_real)
    pprint(api_result)
    
    
def calculate_rsi(rsi_range, market_values):
    """
    Step 1: Calculating Up Moves and Down Moves
    First, calculate the bar-to-bar changes for each bar: Chng = Closet – Closet-1

    For each bar, up move (U) equals:

    Closet – Closet-1 if the price change is positive
    Zero if the price change is negative or zero
    Down move (D) equals:

    The absolute value of Closet – Closet-1 if the price change is negative
    Zero if the price change is positive or zero"""
    print(len(market_values))
    up_values = []
    down_values = []
    for index in range(1, len(market_values)):
        change = market_values[index][1] - market_values[index - 1][1]
        #print(str(change))
        up_values.append(0.0)
        down_values.append(0.0)
        if change > 0:
            up_values[index-1] = abs(float(change))
        else:
            down_values[index-1] = abs(float(change))
    
    
    """Simple Moving Average
    Under this method, which is the most straightforward, AvgU and AvgD are calculated as simple moving averages:

    AvgU = sum of all up moves (U) in the last N bars divided by N

    AvgD = sum of all down moves (D) in the last N bars divided by N

    N = RSI period"""
    avg_up = []
    avg_down = []
    for index in range(rsi_range, len(market_values)):
        avg_up.append(sum(up_values[index - rsi_range:index + 1]) / float(rsi_range))
        avg_down.append(sum(down_values[index - rsi_range:index + 1]) / float(rsi_range))
    
    """RS = AvgU / AvgD -> This is how we calculate the relative strength"""
    relative_strength = []
    for index in range(0, len(avg_up)):
        relative_strength.append(avg_up[index] / (avg_down[index] + 0.001))
        print("The relative strength is: " + str(relative_strength[index]) + "  avg_up " + str(avg_up[index]) + "  avg_down " + str(avg_down[index]))
    #print(relative_strength)
    """Finally, we know the Relative Strength and we can apply the whole RSI formula:

       RSI = 100 – 100 / ( 1 + RS)"""
    rsi_values = []
    for elem in relative_strength:
        rsi_values.append(100.0 - (100.0 / (1.0+elem)))
    
    with open("test2.csv", "w") as f:
        for elem in rsi_values:
            f.write(str(elem) + "\n")
            print(elem)

    return rsi_values
    
def print_all_coins():
    input_data = cg.get_coins_list()
    coin_ids = get_all_coin_ids(input_data)
    #for elem in coin_ids:
       # print(coin_ids)
    pprint(coin_ids)
"""
    coin_markets = []
    for coin in coin_ids:
        try:
            current_coin = cg.get_coin_market_chart_by_id(coin, "usd", 7)
            print("Added info for " + coin + " in usd for " + str(7) + " days")
            print("Coin index for " + coin)
            pprint(cg.get_indexes_by_id(coin))
            #pprint(current_coin)
            coin_markets.append(current_coin)
        except:
            print("Couldn't execute for coin: " + coin)
            
    pprint(coin_markets)
"""
if __name__ == "__main__":
    print(cg.ping())
    #print_all_coins()
    candles = get_candles("bitcoin", "usd", 1)
    #rsi = calculate_rsi(14, candles)
   ###current_daytime = int(time.time())
   ###previous_daytime = current_daytime - 30000
   ###print(previous_daytime, current_daytime)
   ###bitcoin_chart_range = cg.get_coin_market_chart_range_by_id("bitcoin", "usd", previous_daytime, current_daytime)
   ###pprint(bitcoin_chart_range)
   ###print(calculate_rsi(14, bitcoin_chart_range["prices"]))
    #cg.get_coin_market_chart_range_by_id
    #input_data = cg.get_coins_list()
    #coin_markets = cg.get_coins_markets(vs_currency="usd")
    #print("Total coins markets: " + str(len(coin_markets)))
    #pprint(coin_markets)
    #pprint(input_data)
    #print("Total coins: " + str(len(input_data)))

    wait = input("Press Enter to continue.")






























































































