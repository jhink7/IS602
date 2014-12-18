if __name__ == "__main__":
    import pandas as pd
    import numpy as np
    from scipy.stats import norm
    from scipy.stats import cauchy
    from scipy.stats import pareto
    import matplotlib.pyplot as plt
    #plt.figsize(14,8)

    # read in historical S&P data into a pandas dataframe
    sp500 = pd.read_csv('sp_historical.csv', error_bad_lines=False)

    # convert Date column to actual date type
    sp500['Date'] = pd.to_datetime(sp500['Date'])

    # calculate the standard deviations associated with each price movement
    sp500['zscore'] = abs((sp500.Change - sp500.Change.mean())/sp500.Change.std(ddof=0))

    print('Maximum standard deviation of price movements:')
    print(sp500['zscore'].max())

    #fit normal distribution to data
    mu, std = norm.fit(sp500['Change'].values)
    plt.hist(sp500['Change'].values, bins=25, normed=True, alpha=0.6, color='g')

    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=1)
    title = "Normal Fit results: mu = %.2f,  std = %.2f" % (mu, std)
    plt.title(title)
    plt.show()

    #fit cauchy distribution to data
    plt.hist(sp500['Change'].values, bins=25, normed=True, alpha=0.6, color='g')
    a,b = cauchy.fit(sp500['Change'].values)
    p = cauchy.pdf(x, a, b)
    plt.plot(x, p, 'k', linewidth=1)
    title = "Cauchy Fit results: mu = %.2f,  b = %.2f" % (a, b)
    plt.title(title)
    plt.show()

    #fit pareto distribution to data
    plt.hist(sp500['zscore'], bins=25, normed=True, alpha=0.6, color='g')
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    b,loc,scale = pareto.fit(sp500['zscore'], 2, loc=0,scale=1.5)
    p = pareto.pdf(x, b,loc,scale)
    plt.plot(x, p, 'k', linewidth=1)
    title = "Pareto Fit results: b = %.2f,  loc = %.2f, scale = %.2f" % (b, loc,scale)
    plt.title(title)
    plt.show()

    sp500.plot(x="Date",y="zscore")
    plt.title("Part 2b Non Gaussian Price Movements")
    plt.xlabel('Time')
    plt.ylabel('Daily Price Movements (stds)')
    plt.legend().set_visible(False)
    plt.show()

