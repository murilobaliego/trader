from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse

import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.utils.flushfile


class St(bt.SignalStrategy):
    params = (('usepp1', False),
              ('plot_on_daily', False))

    def __init__(self):
        autoplot = self.p.plot_on_daily
        self.pp = pp = bt.ind.PivotPoint(self.data1, _autoplot=autoplot)


        ## Here is here I am trying to buy when the daily close is less than the
        ## pivot on the Xth day and sell whenever it crosses r1
        pp1 = self.pp()  # couple the entire indicators
        self.buysignal = self.data0.close < pp1.p
        self.sellsignal = self.data0.close > pp1.r1

        self.signal_add(bt.SIGNAL_LONG, self.buysignal)
        self.signal_add(bt.SIGNAL_LONGEXIT, self.sellsignal)


    def next(self):
        txt = ','.join(
            ['%04d' % len(self),
             '%04d' % len(self.data0),
             '%04d' % len(self.data1),
             self.data.datetime.date(0).isoformat(),
             '%04d' % len(self.pp),
             '%.2f' % self.pp[0]])

        print(txt)


def runstrat():
    args = parse_args()

    cerebro = bt.Cerebro()
    data = btfeeds.BacktraderCSVData(dataname=args.data)
    cerebro.adddata(data)
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Months)

    cerebro.addstrategy(St,
                        plot_on_daily=args.plot_on_daily)
    cerebro.run(runonce=False)
    if args.plot:
        cerebro.plot(style='bar')


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Sample for pivot point and cross plotting')

    parser.add_argument('--data', required=False,
                        default='data/PETR4.SA.csv',
                        help='Data to be read in')

    parser.add_argument('--plot', required=False, action='store_true',
                        help=('Plot the result'))

    parser.add_argument('--plot-on-daily', required=False, action='store_true',
                        help=('Plot the indicator on the daily data'))

    return parser.parse_args()


if __name__ == '__main__':
    runstrat()