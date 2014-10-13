# This is the main of the program.
if __name__ == "__main__":
    import csv;
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

        print 'X = {0}'.format(X)
        print 'Y = {0}'.format(Y)
        print 'bo = {0}*br + {1}'.format(X,Y)