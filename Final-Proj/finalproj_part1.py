if __name__ == "__main__":
    import numpy as np
    from scipy.optimize import curve_fit
    import matplotlib.pyplot as plt
    from scipy.stats import norm
    from scipy.stats import cauchy
    from scipy.fftpack import fft
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
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.show()

    from zipline.algorithm import TradingAlgorithm
    from zipline.algorithm import TradingAlgorithm
    from zipline.transforms import MovingAverage, batch_transform
    from zipline.utils.factory import load_from_yahoo
    data = load_from_yahoo(stocks=['AAPL', 'PEP', 'KO']); data.save('talk_px.dat')