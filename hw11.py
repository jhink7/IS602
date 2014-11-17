if __name__ == "__main__":
    import csv;
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib import gridspec

    # import data
    # pre-processing note:  I named the 3rd column "PctChange" and changed the first
    # value from XXXX to 0 manually in the csv before import
    apl = pd.read_csv('apple.2011.csv', header=0, error_bad_lines=False)

    # since we're sampling from a normal distribution, we need to know the mean and
    # standard deviation of the stock.  Note that this relies on the assumption that
    # past, measured std is a good predictor of future std. It probably is not.

    mu = apl.PctChange.mean()
    sigma = apl.PctChange.std()

    numSims = 100000;
    numSimDays = 20

    last = float(apl.Last.tail(1))

    simFinalPrices = []
    #generate 20 random price movements as a percentage
    for i in range(numSims):
        s = np.random.normal(mu, sigma, numSimDays)

        simCurrPrice = last
        # simulate 20 days
        for j in range(numSimDays):
            simCurrPrice = simCurrPrice * (1+s[j])

        simFinalPrices.append(simCurrPrice)

    simFinalPrices.sort()
    p = np.percentile(simFinalPrices, 1)
    print "VaR: " +str(p)


