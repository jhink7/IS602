# filter the Fourier transform with a simple bandpass filter
def filter_rule(x,freq):
    buff = 0.5
    highCut = 16
    lowCut = 8
    if abs(freq)> (highCut+buff) or abs(freq)<(lowCut-buff):
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
    import numpy as np
    from scipy.optimize import curve_fit
    import matplotlib.pyplot as plt
    from array import array
    from scipy.stats import norm
    from scipy.fftpack import fft
    from scipy.fftpack import ifft
    from scipy.fftpack import fftfreq
    from pylab import *
    import math
    pi = math.pi

    # Creating a function to model and create data from normal distribution
    def gaus(x,a,b,c):
        return a*np.exp(-(x-b)**2/(2*c**2))

    # Creating a function to model and create data from cauchy distribution
    def cauch(x, a, b):
        #dist = cauchy()
        #return distC.pdf(x)
        return 1 / (pi * a * (1 + ((x-b)/a)**2))

    # Generating clean data
    x = np.linspace(-10, 10, 100)
    y = gaus(x, 1, 0, 2)

    # Adding (normal, gaussian) noise to the data
    y_noise = y + 0.15 * np.random.normal(size=len(x))

    # Executing curve_fit on noisy data
    popt, pcov = curve_fit(gaus, x, y_noise)

    print("Normal Best Fit Estimate:")
    print(popt)

    plt.scatter(x,y_noise)
    plt.plot(x, y)
    plt.title("Part 1a Curve Fitting (Normal Dist)")
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.show()

    # Generating clean data
    y = cauch(x,1.0,0.0)
    # Adding (normal, gaussian) noise to the data
    y_noise = y + 0.05 * np.random.normal(size=len(x))

    # Executing curve_fit on noisy data
    popt, pcov = curve_fit(cauch, x, y_noise)
    print("Cauchy Best Fit Estimate:")
    print(popt)

    plt.scatter(x,y_noise)
    plt.plot(x, y)
    plt.title("Part 1a Curve Fitting (Cauchy Dist)")
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.show()

    # Fourier Analysis, base skills
    N = 600
    T = 1.0 / 800.0
    x = np.linspace(0.0, N*T, N)
    y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
    yf = fft(y)
    xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
    plt.plot(xf, 2.0/N * np.abs(yf[0:N/2]))
    plt.grid()
    plt.title("Part 1b Fourier Analysis")
    plt.xlabel('F')
    plt.ylabel('g(F)')
    plt.show()

    # Basic filtering of a signal
    numSamples  = 100 # number of samples

    # create pure signal
    f_signal  = 8   # signal frequency  in Hz
    dt = 0.01 # sample timing in seconds
    amp = 1    # signal amplitude
    s = [amp*sin((2*pi)*f_signal*k*dt) + 2*amp*sin((2*pi)*f_signal*2*k*dt) for k in range(0,numSamples)]
    s_time = [k*dt for k in range(0,numSamples)]

    # simulate measurement noise
    from random import gauss
    mu = 0
    sigma = 2
    n = [gauss(mu,sigma) for k in range(0,numSamples)]

    # add noise to our pure signal
    s_noise = [ss+nn for ss,nn in zip(s,n)]

    # Get spectrum of the time domain signal
    F = fft(s_noise)

    # get frequencies for each FFT sample
    f = fftfreq(len(F),dt)  # get sample frequency in Hz

    Ffilt = []

    # apply a filter to the signal to de-noise it
    Ffilt = getfilteredsignal(F,f)
    Ffilt = array(Ffilt)

    # create the time domain signal from our filtered spectrum
    # should be a purer time domain signal
    sFilt = ifft(Ffilt)

    #plot results
    plt.plot(s_time, sFilt)
    plt.plot(s_time, s)
    plt.title("Part 1b Fourier Analysis, Filtering")
    plt.xlabel('Time[s]')
    plt.ylabel('f(x)')
    plt.legend(['Filtered Signal','Original Signal'])
    plt.show()