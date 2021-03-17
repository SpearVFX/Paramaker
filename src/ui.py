import sys
from PyQt5 import QtChart
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtChart import (QCandlestickSeries, QCandlestickSet, QChart, QChartView)
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QPointF
from PyQt5 import QtChart as qc


class ParaMakerApplication(QApplication):
    pass


class ParaMakerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: black;")
        self.setWindowTitle("Paramaker")
        self.setGeometry(200,200,1000,400)
        self.show()



def plot_candlechart(ohlc_data):
        app = ParaMakerApplication([])
        #
        series = QCandlestickSeries()
        series.setDecreasingColor(Qt.red)
        series.setIncreasingColor(Qt.green)

        ma5 = qc.QLineSeries()  # 5-days average data line
        tm = []  # stores str type data

        # in a loop,  series and ma5 append corresponding data
        for candle in ohlc_data:
            series.append(QCandlestickSet(candle.opened,
                                          candle.high,
                                          candle.low,
                                          candle.closed))
            #ma5.append(QPointF(num, m))
            tm.append(str(candle.timestamp))

        chart = QChart()

        chart.addSeries(series)  # candle
        chart.addSeries(ma5)  # ma5 line

        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.createDefaultAxes()
        chart.legend().hide()

        chart.axisX(series).setCategories(tm)
        chart.axisX(ma5).setVisible(False)

        chartview = QChartView(chart)
        ui = ParaMakerWindow()
        ui.setCentralWidget(chartview)
        sys.exit(app.exec_())
