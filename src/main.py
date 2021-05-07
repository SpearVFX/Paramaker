import cryptowatch as cw
from pprint import pprint
from utils import cprint, ranked_color
import time, json
from candles import Candle, CandleChart
from ui import ParaMakerWindow, ParaMakerApplication, plot_candlechart
import os
clear = lambda: os.system('cls')

with open("../credentials.txt", 'r') as f:
    cw.api_key = f.readline()


def beautify_json(input_json):
    json.dumps(json.loads(input_json), sort_keys=True, indent=4)


def calculate_rsi(rsi_range, market_values):
    """
    Step 1: Calculating Up Moves and Down Moves
    First, calculate the bar-to-bar changes for each bar: Chng = Closed – Closed-1

    For each bar, up move (U) equals:

    Closed – Closed-1 if the price change is positive
    Zero if the price change is negative or zero
    Down move (D) equals:

    The absolute value of Closed – Closed-1 if the price change is negative
    Zero if the price change is positive or zero"""
    #print(len(market_values))
    up_values = []
    down_values = []
    """
    for index in range(1, len(market_values)):
        change = market_values[index] - market_values[index - 1]
        #print(str(change))
        up_values.append(0.0)
        down_values.append(0.0)
        if change >= 0:
            up_values[index-1] = abs(float(change))
        else:
            down_values[index-1] = abs(float(change))"""
    for index in range(1, len(market_values)):
        change = 0.0
        if(market_values[index] > 0):
            change = (100*((market_values[index] - market_values[index - 1]) / market_values[index]))
        #print(str(change))
        up_values.append(0.0)
        down_values.append(0.0)
        if change >= 0:
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
    ema_up = []
    ema_down = []
    a_ema = 2 / (rsi_range + 1)
    for index in range(1, len(market_values) - 1):
        ema_up.append(a_ema*up_values[index]+(1-a_ema)*up_values[index-1])
        ema_down.append(a_ema*down_values[index]+(1-a_ema)*down_values[index-1])

    for index in range(rsi_range, len(market_values) - 1):
        avg_up.append(sum(up_values[index - rsi_range:index + 1]) / float(rsi_range))
        avg_down.append(sum(down_values[index - rsi_range:index + 1]) / float(rsi_range))

    """RS = AvgU / AvgD -> This is how we calculate the relative strength"""
    relative_strength = []
    for index in range(0, len(avg_up)):
        if(avg_down[index] > 0):
            relative_strength.append(avg_up[index] / (avg_down[index]))
        else:
            relative_strength.append(1)
        #print("The relative strength is: " + str(relative_strength[index]) + "  avg_up " + str(avg_up[index]) + "  avg_down " + str(avg_down[index]))
    #print(relative_strength)
    """Finally, we know the Relative Strength and we can apply the whole RSI formula:

       RSI = 100 – 100 / ( 1 + RS)"""
    rsi_values = []
    for elem in relative_strength:
        rsi_values.append(100.0 - (100.0 / (1.0+elem)))

    with open("test2.csv", "w") as f:
        for elem in rsi_values:
            f.write(str(elem) + "\n")
            #print(elem)

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
    with open('../candledata.json', 'r') as dump:
        candles = json.load(dump)

    candlechart = CandleChart("BINANCE", "btcusdt", "15m")
    print(type(candlechart.data))
    plot_candlechart(candlechart.data)
    quit()
    #for candle in candlechart:
        #cprint(candle)
    #quit()




    #print(cg.ping())
    binance = cw.markets.list("BINANCE")
    #for pair in binance.pair:
    all_last_rsi_values = []
    for market in binance.markets:
        pair = market.pair
        if(pair.startswith("") and pair.endswith("usdt")):
            candle_chart = CandleChart("BINANCE", pair, "1h")
            #for candle in candle_chart:
            #    cprint(candle)
            #break
            #closed_prices_result = []
            #for candle in candles.of_1h:
                #closed_prices_result.append(candle[3])
            #pprint(closed_prices_result)
            rsi_values = calculate_rsi(14, candle_chart.closed_values())
            all_last_rsi_values.append((pair, rsi_values[-1]))
            all_last_rsi_values = sorted(all_last_rsi_values, key=lambda x: x[1], reverse=True)
            clear()
            for item in all_last_rsi_values:
                print(item[0], ranked_color(item[1]))


            #print("RSI VALUE FOR PAIR {} IS {}".format(str(pair), str(rsi_values[-1])))
            #for rsi in rsi_values:
                #print(rsi)
            #break
            #rsi_values_average = sum(rsi_values) / len(rsi_values)
            #rsi_diff = 50.0 - rsi_values_average

                #break



            #######with open("test3.csv", "w") as f:
                #######for elem in rsi_values:
                    #######f.write(str(elem) + "\n")
            #print(elem)

            #print(candles._allowance.remaining)
            #if(rsi_values[-1] < 20.0):
            #print("{}:{}".format(market.exchange, pair).upper())
            #print(rsi_values[-1])
            #break
                #print(rsi_values)
            #else:
                #print("Nothing on {}:{}".format(market.exchange, pair).upper())

    #print(binance)
    "https://github.com/cryptowatch/cw-sdk-python"
    "https://github.com/uoshvis/python-cryptowatch - unofficial, but seems easier to use."
    "https://www.alphavantage.co/documentation/ - check this one out tomorrow."
    #print_all_coins()
    #candles = get_candles("bitcoin", "usd", 1)
    #rsi = calculate_rsi(14, candles)
    #current_daytime = int(time.time())
    #previous_daytime = current_daytime - 86400
   ###print(previous_daytime, current_daytime)
    #bitcoin_chart_range = cg.get_coin_market_chart_range_by_id("bitcoin", "usd", previous_daytime, current_daytime)
   ###pprint(bitcoin_chart_range)
    #print(calculate_rsi(14, bitcoin_chart_range["prices"]))
    #cg.get_coin_market_chart_range_by_id
    #input_data = cg.get_coins_list()
    #coin_markets = cg.get_coins_markets(vs_currency="usd")
    #print("Total coins markets: " + str(len(coin_markets)))
    #pprint(coin_markets)
    #pprint(input_data)
    #print("Total coins: " + str(len(input_data)))

    #wait = input("Press Enter to continue.")
