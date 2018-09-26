from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt


# Create a Stratey

class TheStrategy(bt.Strategy):
    '''
    This strategy is loosely based on some of the examples from the Van
    K. Tharp book: *Trade Your Way To Financial Freedom*. The logic:

      - Enter the market if:
        - The MACD.macd line crosses the MACD.signal line to the upside
        - The Simple Moving Average has a negative direction in the last x
          periods (actual value below value x periods ago)

     - Set a stop price x times the ATR value away from the close

     - If in the market:

       - Check if the current close has gone below the stop price. If yes,
         exit.
       - If not, update the stop price if the new stop price would be higher
         than the current
    '''

    params = (
        # Standard MACD Parameters
        ('macd1', 12),#12
        ('macd2', 26),#26
        ('macdsig', 9),#9
        ('atrperiod', 7),  # ATR Period (standard)
        ('atrdist', 3.0),   # ATR distance for stop price
        ('smaperiod', 30),  # SMA Period (pretty standard)
        ('dirperiod', 10),  # Lookback period to consider SMA trend direction
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status == order.Completed:
            pass

        if not order.alive():
            self.order = None  # indicate no order is pending

    def __init__(self):
        self.dataclose = self.datas[0].close

        self.macd = bt.indicators.MACD(self.data,
                                       period_me1=self.p.macd1,
                                       period_me2=self.p.macd2,
                                       period_signal=self.p.macdsig)

        # Cross of macd.macd and macd.signal
        self.mcross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)
        self.histo = self.macd.macd - self.macd.signal
        bt.LinePlotterIndicator(self.histo, name='macd_histo')
        # To set the stop price
        self.atr = bt.indicators.ATR(self.data, period=self.p.atrperiod)

        # Control market trend
        self.sma = bt.indicators.SMA(self.data, period=self.p.smaperiod)
        self.smadir = self.sma - self.sma(-self.p.dirperiod)

        #self.emuriba_cross = bt.indicators.CrossOver(self.dataclose, self.sma)

        self.macdhis = bt.indicators.MACDHisto(self.data)

        self.rsi = bt.indicators.RSI(self.datas[0])

        #bt.indicators.Highest(period=self.p.atrperiod)
        self.kst = bt.indicators.KnowSureThing()

        #self.kst_signal = bt.indicators.MovAv(self.kst, period=self.p.macdsig)
        self.kst_cross = bt.indicators.CrossOver(self.kst.kst, self.kst.signal)


        bt.indicators.BollingerBands()
        #bt.ind.CrossOver(bt.ind.RSI(), 50)
        #bt.ind.CrossOver(self.macdhis, 0)
        #self.mcrosshist = bt.indicators.CrossOver(self.macdhis, 0.0)
        #bt.ind.MaxN(self.macdhis, period=self.p.macd2)
        #bt.LinePlotterIndicator(self.clsmax, name='max_macd')

        #sma1 = bt.indicators.SimpleMovingAverage(self.data)
        #ema1 = bt.indicators.ExponentialMovingAverage()

        #close_over_sma = self.data.close > sma1
        #close_over_ema = self.data.close > ema1
        #sma_ema_diff = sma1 - ema1

        #self.buy_sig = bt.And(close_over_sma, close_over_ema, sma_ema_diff > 0)
        #bt.LinePlotterIndicator(self.smadir, name='smadir')

        #self.pp = pp = bt.ind.PivotPoint(self.data)

        ## Here is here I am trying to buy when the daily close is less than the
        ## pivot on the Xth day and sell whenever it crosses r1
        #pp1 = self.pp()  # couple the entire indicators
        #self.buysignal = self.data0.close < pp1.p
        #self.sellsignal = self.data0.close > pp1.r1

        #self.signal_add(bt.SIGNAL_LONG, self.buysignal)
        #self.signal_add(bt.SIGNAL_LONGEXIT, self.sellsignal)

        # ----- new strategy -----
        #A classic Fast EMA crosses over a Slow EMA approach will be used. But:

        #Only the up-cross will be taken into account to issue a buy order
        #Exiting the market, i.e.: sell will be done via a Stop
        # ------------------------
        # omitting a data implies self.datas[0] (aka self.data and self.data0)
        #fast_ma = bt.ind.EMA(period=self.p.fast_ma)
        #slow_ma = bt.ind.EMA(period=self.p.slow_ma)
        # our entry point
        #self.crossup = bt.ind.CrossUp(fast_ma, slow_ma)


    def start(self):
        self.order = None  # sentinel to avoid operrations on pending order

    def next(self):

        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return  # pending order execution

        if not self.position:  # not in the market

            if self.kst_cross[0] > 0.0:
            #if self.macdcrossup[0] > 0.0 and self.smadir[0] > 0.0:
            #if self.rsi[0] < 30.0:# and self.smadir[0] > 0.0:
            #if self.emuriba_cross > 0.0:
            #if self.buysignal:
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy()
                    self.bought = self.data.close[0]
                    self.pricetosell = self.data.close[0] * 1.10
                    self.pricetostop = self.data.close[0] * 0.95
                    #pdist = self.atr[0] * self.p.atrdist
                    #self.pstop = self.data.close[0] - pdist

        else:  # in the market
            #pclose = self.data.close[0]
            #pstop = self.pstop

            #if pclose < pstop:
            #    self.close()  # stop met - get out
            #    self.log('Sell CREATE, %.2f' % self.dataclose[0])
            #else:
            #    pdist = self.atr[0] * self.p.atrdist
                # Update only if greater than
            #    self.pstop = max(pstop, pclose - pdist)

            #if self.macddir[0] > 0.0 and self.mcross[0] > 0.0:
            if self.kst_cross[0] < 0.0:
            #if (self.mcross < 0.0) or (self.data.close[0] > self.pricetosell):
            #if self.data.close[0] >= self.pricetosell:# or self.data.close[0] <= self.pricetostop:
            #if self.rsi[0] > 70.0:
            #if self.sellsignal:
            #if self.histo[0] < 0.0 and self.histo[-1] > 0.0 and self.histo[-2] > 0.0:
                    self.log('Sell CREATE, %.2f' % self.dataclose[0])
                    self.pstop = self.data.close[0]
                    self.close()  # stop met - get out

if __name__ == '__main__':
    startcash = 20000
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(TheStrategy)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, 'data/PETR4.SA.csv')
    #datapath = os.path.join(modpath, 'data/ABEV3.SA.csv')

    # Create a Data Feed
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        # Do not pass values before this date
        fromdate=datetime.datetime(2018, 1, 1),
        # Do not pass values before this date
        todate=datetime.datetime(2018, 9, 13),
        # Do not pass values after this date
        reverse=False)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(startcash)

    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)

    # Set the commission
    cerebro.broker.setcommission(commission=0.01)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Plot the result
    cerebro.plot()
