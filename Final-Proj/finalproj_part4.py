from zipline.algorithm import TradingAlgorithm
from zipline.transforms import MovingAverage, batch_transform
from zipline.utils.factory import load_from_yahoo
from zipline.finance import commission,slippage

class DualMovingAverage(TradingAlgorithm):
    """Dual Moving Average Crossover algorithm.

    This algorithm buys apple once its short moving average crosses
    its long moving average (indicating upwards momentum) and sells
    its shares once the averages cross again (indicating downwards
    momentum).

    """
    def initialize(self):
        # Add 2 mavg transforms, one with a long window, one
        # with a short window.
        self.add_transform(MovingAverage, 'short_mavg', ['price'],
                           window_length=200)

        self.add_transform(MovingAverage, 'long_mavg', ['price'],
                           window_length=400)

        # To keep track of whether we invested in the stock or not
        self.invested = False

        self.set_commission(commission.PerTrade(cost=0))        
        self.set_slippage(slippage.FixedSlippage(spread=0.0))

        self.short_mavg = []
        self.long_mavg = []
        self.buy_orders = []
        self.sell_orders = []

        self.tradingdays = 0;

    def handle_data(self, data):
        # Save mavgs for later analysis.
        self.short_mavg.append(data[symbol].short_mavg['price'])
        self.long_mavg.append(data[symbol].long_mavg['price'])

        runningPrices.append(data[symbol].price)
        s = runningPrices
        if(self.tradingdays > 252):

            # Add Tail buffer to stock signal
            # set a number of days to our last closing price
            # we will remove these later
            for x in range(0,1000):
                s = np.append(s, data[symbol].price)

            F = fft(s)

            #filter

            dt = 1/252.0
            f = fftfreq(len(F),dt)  # get sample frequency in samples per year

            #F_filt = F
            F_filt = self.getfilteredsignal(F,f)
            F_filt = np.array(F_filt)

            s_filt = ifft(F_filt)

            # Remove Tail buffer from stock signal
            for x in range(0,1000):
                s = np.delete(s, len(s)-1)
                s_filt = np.delete(s_filt, len(s_filt)-1)

            currSmoothedPrice = s_filt[-1]
            runningFilteredPrices.append(currSmoothedPrice)

            if (data[symbol].price / 1.2 > currSmoothedPrice):
                self.order(symbol, -200)
                self.invested = False
                self.sell_orders.append(data[symbol].datetime)
                print "{dt}: Selling 200 shares.".format(dt=data[symbol].datetime)
            elif (data[symbol].price * 1.2 < currSmoothedPrice):
                self.order(symbol, 200)
                self.invested = True
                self.buy_orders.append(data[symbol].datetime)
                print "{dt}: Buying 200 shares.".format(dt=data[symbol].datetime)

        else:
            runningFilteredPrices.append(data[symbol].price)

        self.tradingdays = self.tradingdays +1

    # filter the signal with simple high pass filter
    def filter_rule(self, x,freq):
        buff = 0.05
        highCut = 0.3
        if abs(freq)> (highCut+buff):
            return 0
        else:
            return x

    # method that generates our filtered signal
    def getfilteredsignal(self, yf_noise, f):
        filteredSignal = []
        for x in range(0, len(f)):
            temp = self.filter_rule(yf_noise[x],f[x])
            filteredSignal.append(temp)

        return filteredSignal

runningPrices = []
runningFilteredPrices = []
symbol = "SPY"
if __name__ == "__main__":
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.fftpack import fft
    from scipy.fftpack import ifft
    from scipy.fftpack import fftfreq

    data = load_from_yahoo(stocks=[symbol]); #data.save('talk_px.dat')

    dma = DualMovingAverage()
    results = dma.run(data)

    ax1 = plt.subplot(211)
    data['short'] = dma.short_mavg
    data['long'] = dma.long_mavg
    data[[symbol, 'short', 'long']].plot(ax=ax1)
    plt.plot(dma.buy_orders, data['short'].ix[dma.buy_orders], '^', c='m', markersize=10, label='buy')
    plt.plot(dma.sell_orders, data['short'].ix[dma.sell_orders], 'v', c='k', markersize=10, label='sell')
    plt.legend(loc=0)

    ax2 = plt.subplot(212)
    results.portfolio_value.plot(ax=ax2)

    plt.show()

    plt.plot(runningFilteredPrices)
    plt.plot(runningPrices)
    plt.legend(['Filtered Signal','Original Signal'])
    plt.show()


