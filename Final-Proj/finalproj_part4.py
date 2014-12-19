from zipline.algorithm import TradingAlgorithm
from zipline.transforms import MovingAverage, batch_transform
from zipline.utils.factory import load_from_yahoo

class BuyApple(TradingAlgorithm): # inherit from TradingAlgorithm
    def handle_data(self, data): # overload handle_data() method
        self.order('AAPL', 1) # stock (='AAPL') to order and amount (=1 shares)

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

        self.short_mavg = []
        self.long_mavg = []
        self.buy_orders = []
        self.sell_orders = []

    def handle_data(self, data):
        if (data['AAPL'].short_mavg['price'] > data['AAPL'].long_mavg['price']) and not self.invested:
            self.order('AAPL', 200)
            self.invested = True
            self.buy_orders.append(data['AAPL'].datetime)
            print "{dt}: Buying 100 AAPL shares.".format(dt=data['AAPL'].datetime)
        elif (data['AAPL'].short_mavg['price'] < data['AAPL'].long_mavg['price']) and self.invested:
            self.order('AAPL', -200)
            self.invested = False
            self.sell_orders.append(data['AAPL'].datetime)
            print "{dt}: Selling 100 AAPL shares.".format(dt=data['AAPL'].datetime)

        # Save mavgs for later analysis.
        self.short_mavg.append(data['AAPL'].short_mavg['price'])
        self.long_mavg.append(data['AAPL'].long_mavg['price'])

        test = data['AAPL'].price

if __name__ == "__main__":
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    #plt.figsize(14,8)


    #data = load_from_yahoo(stocks=['AAPL', 'PEP', 'KO']); data.save('talk_px.dat')

    data = pd.load('talk_px.dat')
    data['AAPL'].plot()
    plt.show()

    #print(data['AAPL'])
    #my_algo = BuyApple() # Instantiate our algorithm
    #results_buy_apple = my_algo.run(data) # Backtest algorithm on dataframe.

    #print results_buy_apple

    dma = DualMovingAverage()
    results = dma.run(data)

    ax1 = plt.subplot(211)
    data['short'] = dma.short_mavg
    data['long'] = dma.long_mavg
    data[['AAPL', 'short', 'long']].plot(ax=ax1)
    plt.plot(dma.buy_orders, data['short'].ix[dma.buy_orders], '^', c='m', markersize=10, label='buy')
    plt.plot(dma.sell_orders, data['short'].ix[dma.sell_orders], 'v', c='k', markersize=10, label='sell')
    plt.legend(loc=0)

    ax2 = plt.subplot(212)
    results.portfolio_value.plot(ax=ax2)

    plt.show()
