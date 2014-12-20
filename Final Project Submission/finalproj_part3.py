# filter the signal with simple high pass filter
def filter_rule(x,freq):
    buff = 0.05
    highCut = 0.5
    if abs(freq)> (highCut+buff):
        return 0
    else:
        return x

# method that generates our filtered signal
def getfilteredsignal(yf_noise, f):
    filteredSignal = []
    for x in range(0, len(f)):
        temp = filter_rule(yf_noise[x],f[x])
        filteredSignal.append(temp)

    return filteredSignal

if __name__ == "__main__":
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.fftpack import fft
    from scipy.fftpack import ifft
    from scipy.fftpack import fftfreq
    from zipline.utils.factory import load_from_yahoo

    symbl = 'GE'
    data = load_from_yahoo(stocks=[symbl]);

    s = data[symbl].values

    currPrice = s[-1]

    # Add Tail buffer to stock signal
    # set a number of days to our last closing price
    # we will remove these later
    for x in range(0,1000):
        s = np.append(s, currPrice)

    # get frequency domain of our time series of closing prices
    F = fft(s)

    # we sample once per trading day or 1 in a 252nd of a trading year
    dt = 1/252.0
    f = fftfreq(len(F),dt)  # get sample frequency in samples per year

    # filter out higher frequencies.  Might de-noise the signal, ie make
    # useful information more readily apparent
    Ffilt = getfilteredsignal(F,f)
    Ffilt = np.array(Ffilt)

    # reconstruct time series (now filtered)
    s_filt = ifft(Ffilt)

    # Remove Tail buffer from stock signal
    for x in range(0,1000):
        s = np.delete(s, len(s)-1)
        s_filt = np.delete(s_filt, len(s_filt)-1)

    #plot our filtered signal and our original signal for comparison purposes
    plt.plot(s_filt)
    plt.plot(s)
    plt.title("Part 3 Fourier Analysis of Sample Stock)")
    plt.xlabel('Time[days]')
    plt.ylabel('Price ($)')
    plt.legend(['Filtered Signal','Original Signal'])
    plt.show()



