'''

fonte: https://backtest-rookies.com/2018/04/20/replacing-quandl-wiki-data-with-alpha-vantage/

Author: www.backtest-rookies.com

MIT License

Copyright (c) 2018 backtest-rookies.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from alpha_vantage.timeseries import TimeSeries
import argparse
import pandas as pd


#def parse_args():
#    parser = argparse.ArgumentParser(description='CCXT Market Data Downloader')


#    parser.add_argument('-s','--symbol',
#                        type=str,
#                        required=True,
#                        help='The Symbol of the Instrument/Currency Pair To Download')

#    parser.add_argument('-o', '--outfile',
#                        type=str,
#                        required=True,
#                        help='The output directory and file name to save the data')

#    return parser.parse_args()

# Get our arguments
#args = parse_args()

#print(args)

# Submit our API and create a session
alpha_ts = TimeSeries(key='X2YNJWH7QSF0OY2C', output_format='pandas')

# Get the data
#data, meta_data = alpha_ts.get_daily(symbol=args.symbol, outputsize='compact')
data, meta_data = alpha_ts.get_daily(symbol="PETR4.SA", outputsize='compact')

# Save the data
data.to_csv("test_alpha")