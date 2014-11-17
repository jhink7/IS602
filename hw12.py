def computeVaRParallel(mu, sigma, numSimDays, numSims, last):
    def SimAppleFuture(mu, sigma, numSimDays, numSims, last):
        import numpy as np
        simFinalPrices = []

        #  generate 20 random price movements as a percentage
        for i in range(numSims):
            s = np.random.normal(mu, sigma, numSimDays)

            simCurrPrice = last
            # simulate 20 days
            for j in range(numSimDays):
                simCurrPrice = simCurrPrice * (1+s[j])

            simFinalPrices.append(simCurrPrice)
        return simFinalPrices

    ar = dview.apply_async(SimAppleFuture, mu, sigma, numSimDays, numSims, last)

    dview.wait(ar)
    result = ar.get()
    numEngs =  len(result)

    #gather all results
    allsims = []
    for i in range(numEngs):
        for j in range(len(result[i])):
            allsims.append(result[i][j])

    #find the 1st percentile on the aggregated results
    allsims.sort()
    p = np.percentile(allsims, 1)
    print "VaR (parallel calc): " +str(p)

def computeVaRSerial(mu, sigma, numSimDays, numSims, last):
    simFinalPrices = []

    numSims = numSims * 4

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
    print "VaR (serial calc): " +str(p)

if __name__ == "__main__":
    import numpy as np
    import pandas as pd
    import timeit
    from IPython.parallel import Client
    c = Client()
    dview = c[:]

    apl = pd.read_csv('C:/CUNY/IS602/Python Code/apple.2011.csv', header=0, error_bad_lines=False)

    # since we're sampling from a normal distribution, we need to know the mean and
    # standard deviation of the stock.  Note that this relies on the assumption that
    # past, measured std is a good predictor of future std. It probably is not.
    mu = apl.PctChange.mean()
    sigma = apl.PctChange.std()

    # set to 25000 per engine. 4 engines = 100000 sims (what I used in hw11)
    numSims = 25000
    numSimDays = 20

    last = float(apl.Last.tail(1))

    t1 = timeit.Timer(stmt="computeVaRParallel(mu, sigma, numSimDays, numSims, last)",
                      setup="from __main__ import computeVaRParallel, mu, sigma, numSimDays, numSims, last")
    t2 = timeit.Timer(stmt="computeVaRSerial(mu, sigma, numSimDays, numSims, last)",
                      setup="from __main__ import computeVaRSerial, mu, sigma, numSimDays, numSims, last")

    print "Parallel exec time: " + str(t1.timeit(number=1)) +" s"
    print "Serial exec time: " + str(t2.timeit(number=1)) +" s"


