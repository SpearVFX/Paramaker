import sys
from PyQt5 import QtChart
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtChart import (QCandlestickSeries, QCandlestickSet, QChart, QChartView, QValueAxis)
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QPointF, QFile, QTextStream
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5 import QtChart as qc

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

class ParaMakerApplication(QApplication):
    pass


class ParaMakerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: black;")
        self.setWindowTitle("Paramaker")
        self.setGeometry(200,200,1000,400)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.red)

        painter.drawLine(10,10,100,140)

        painter.setPen(Qt.blue)
        painter.drawRect(120,10,80,80)

        rectf = QRectF(230.0,10.0,80.0,80.0)
        painter.drawRoundedRect(rectf,20,20)

        p1 = [QPoint(10,100),QPoint(220,110),QPoint(220,190)]
        painter.drawPolyline(QPolygon(p1))

        p2 = [QPoint(120,110),QPoint(220,110),QPoint(220,190)]
        painter.drawPolygon(QPolygon(p2))



def plot_candlechart(ohlc_data):
        app = ParaMakerApplication([])
        #app.setStyleSheet("background-color:black;")

        series = QCandlestickSeries()
        series.setBodyOutlineVisible(False)
        series.setDecreasingColor(Qt.red)
        series.setIncreasingColor(Qt.green)

        rsi = qc.QLineSeries()  # 5-days average data line
        rsi.append(QPointF(ohlc_data[300].timestamp, ohlc_data[300].closed))
        rsi.append(QPointF(ohlc_data[700].timestamp, ohlc_data[700].closed))
        #rsi.append(QPointF(ohlc_data[150].timestamp, ohlc_data[100].closed))
        tm = []  # stores str type data
        # in a loop,  series and rsi append corresponding data
        for candle in ohlc_data:
            series.append(QCandlestickSet(candle.opened,
                                          candle.high,
                                          candle.low,
                                          candle.closed))
            #rsi.append(QPointF(num, m))
            tm.append(str(candle.timestamp))
            #rsi.append(str(candle.timestamp))

        #rsi_values = calculate_rsi(14, ohlc_data)

        chart = QChart()
        chart.setBackgroundVisible(False)
        chart.setPlotAreaBackgroundVisible(False)
        chart.addSeries(series)  # candle
        chart.addSeries(rsi)  # rsi line



        #chart.axisX(rsi).setRange(ohlc_data[0].timestamp, ohlc_data[-1].timestamp)

        chart.createDefaultAxes()

        axisXRSI = QValueAxis()
        axisYRSI = QValueAxis()
        axisXRSI.setRange(ohlc_data[0].timestamp, ohlc_data[-1].timestamp)
        axisYRSI.setRange(ohlc_data[0].closed, ohlc_data[-1].closed)
        axisXRSI.setGridLineVisible(False)
        axisYRSI.setGridLineVisible(False)

        chart.setAxisX(axisXRSI, rsi)
        chart.setAxisY(axisYRSI, rsi)

        chart.legend().hide()

        chart.axisX(series).setCategories(tm)
        #chart.axisX(series).setGridLineVisible(False)
        #chart.axisY(series).setGridLineVisible(False)
        ###chart.axisX(rsi).setVisible(False)

        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)
        ui = ParaMakerWindow()
        ui.setCentralWidget(chartview)
        sys.exit(app.exec_())
