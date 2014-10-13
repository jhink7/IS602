def fitmanually(showoutput):
    file_path = "brainandbody.csv";

    with open(file_path) as f:
        reader = csv.reader(f)
        brains = []
        bodies = []
        n = 0.0
        rowcount = 1

        # follow the method from Wolfram.
        sumX = 0.0
        sumY = 0.0
        sumXX = 0.0
        sumYY = 0.0
        sumXY = 0.0
        for row in reader:
            if(rowcount > 1):
                bodies.append(float(row[1]))
                brains.append(float(row[2]))
                sumX = sumX + float(row[2])
                sumY = sumY + float(row[1])
                sumXX = sumXX + float(row[2])*float(row[2])
                sumYY = sumYY + float(row[1])*float(row[1])
                sumXY = sumXY + float(row[1])*float(row[2])
                n += 1
            rowcount +=1

        xbar = sum(brains) / len(brains)
        ybar = sum(bodies) / len(bodies)

        ssxx = sumXX - n * xbar * xbar
        ssyy = sumYY - n * ybar * ybar
        ssxy = sumXY - n * xbar * ybar

        varx = ssxx / n
        vary = ssyy / n
        covxy = ssxy / n

        X = ssxy/ssxx
        Y = ybar - X*xbar

        #print out each
        if(showoutput):
            print 'Fitting manually'
            print 'X = {0}'.format(X)
            print 'Y = {0}'.format(Y)
            print 'bo = {0}*br + {1}'.format(X,Y)

def fitwithscipy(showoutput):
    file_path = "brainandbody.csv";
    with open(file_path) as f:
        reader = csv.reader(f)
        brains = []
        bodies = []
        n = 0.0
        rowcount = 1

        for row in reader:
            if(rowcount > 1):
                bodies.append(float(row[1]))
                brains.append(float(row[2]))
                n += 1
            rowcount +=1

    from scipy.optimize import curve_fit

    def func(x, a, b):
        return a * x + b

    x = brains
    y = bodies

    popt, pcov = curve_fit(func, x, y)

    if(showoutput):
        print 'Fitting with SciPy'
        print 'X = {0}'.format(popt[0])
        print 'Y = {0}'.format(popt[1])
        print 'bo = {0}*br + {1}'.format(popt[0],popt[1])

# This is the main entry point of the program
if __name__ == "__main__":
    import csv;
    import timeit

    # call the fit functions
    fitmanually(True)
    fitwithscipy(True)

    # Please note that the CSV import is only included in the following benchmarking due to the way
    # I coded up my solution to homework 5. In said solution I calculated intermediate variables while
    # importing the data on the fly hoping to minimize passes through the data.  Refactoring this out now
    # (to isolate the actual fitting portion of the code) would not give a true apples to apples comparison to
    # what I did 2 weeks back.  I fully realize that calling the import function 1000 times is not what we would
    # want in any context outside of the benchmark for this homework.

    numiterations = 100
    t1 = timeit.Timer(stmt="fitmanually(False)", setup="from __main__ import fitmanually")
    t2 = timeit.Timer(stmt="fitwithscipy(False)", setup="from __main__ import fitwithscipy")

    print "Fit manually: "+str(numiterations) +" loops = " + str(t1.timeit(number=numiterations)) +"s"
    print "Fit with SciPy: "+str(numiterations) +" loops = " + str(t2.timeit(number=numiterations)) +"s"




