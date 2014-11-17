if __name__ == "__main__":
    import csv;
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib import gridspec

    import pylab
    import mahotas
    from scipy import ndimage

    #Q1
    cars = pd.read_csv('cars.data.csv', header=None, error_bad_lines=False)
    cars.columns = ['buying','maint','doors','persons', 'lug_boot', 'safety', 'ovr']

    #group car data by persons
    x1 = []
    y1 = []
    for key, grp in cars.groupby(['buying']):
        x = key
        y = grp['persons'].count()
        x1.append(key)
        y1.append(y)

    #group car data by maint
    x2 = []
    y2 = []
    for key, grp in cars.groupby(['maint']):
        x = key
        y = grp['persons'].count()
        x2.append(key)
        y2.append(y)

    #group car data by safety
    x3 = []
    y3 = []
    for key, grp in cars.groupby(['safety']):
        x = key
        y = grp['persons'].count()
        x3.append(key)
        y3.append(y)

    #group car data by doors
    x4 = []
    y4 = []
    for key, grp in cars.groupby(['doors']):
        x = key
        y = grp['persons'].count()
        x4.append(key)
        y4.append(y)

    #plot the 4 bar charts as subplots
    fig = plt.figure()
    gs = gridspec.GridSpec(2, 2)

    ax1 = plt.subplot(gs[0])
    N1 = len(y1)
    ind1 = np.arange(N1)
    width = 0.35
    rects1 = plt.bar(ind1, y1, width, color='r')
    xTickMarks1 = x1
    ax1.set_xticks(ind1)
    xtickNames1 = ax1.set_xticklabels(xTickMarks1)
    plt.setp(xtickNames1, rotation=45, fontsize=10)
    ax1.set_title('Cars Grouped by Buying')

    ax2 = plt.subplot(gs[1])
    N2 = len(y2)
    ind2 = np.arange(N2)
    width = 0.35
    rects2 = plt.bar(ind2, y2, width, color='r')
    xTickMarks2 = x2
    ax2.set_xticks(ind2)
    xtickNames2 = ax2.set_xticklabels(xTickMarks2)
    plt.setp(xtickNames2, rotation=45, fontsize=10)
    ax2.set_title('Cars Grouped by Maint')

    ax3 = plt.subplot(gs[2])
    N3 = len(y3)
    ind3 = np.arange(N3)
    width = 0.35
    rects3 = plt.bar(ind3, y3, width, color='r')
    xTickMarks3 = x3
    ax3.set_xticks(ind3)
    xtickNames3 = ax3.set_xticklabels(xTickMarks3)
    plt.setp(xtickNames3, rotation=45, fontsize=10)
    ax3.set_title('Cars Grouped by Safety')

    ax4 = plt.subplot(gs[3])
    N4 = len(y4)
    ind4 = np.arange(N4)
    width = 0.35
    rects4 = plt.bar(ind4, y4, width, color='r')
    xTickMarks4 = x4
    ax4.set_xticks(ind4)
    xtickNames4 = ax4.set_xticklabels(xTickMarks4)
    plt.setp(xtickNames4, rotation=45, fontsize=10)
    ax4.set_title('Cars Grouped by Doors')

    fig.tight_layout()
    plt.show()

    # Q2
    file_path = "brainandbody.csv";

    # read in brains and bodies data
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
            rowcount +=1

        plt.scatter(brains, bodies)

        npBrains = np.array(brains)
        npBodies = np.array(bodies)

        #define our function.  Hard coded for this assignment's purposes
        def f(br):
            return 0.620169627392*br + 1682.58594375

        plt.plot(npBrains, f(npBrains))
        plt.title("Brains vs Bodies")
        plt.xlabel('Brains')
        plt.ylabel('Bodies')
        plt.text(60, 5000, r'bo = 0.620*br + 1682.6')
        plt.show()



    #Q3
    im = plt.imread('objects.png')
    implot = plt.imshow(im, extent=[0, 585, 0, 512])
    plt.scatter(x=[90, 145, 200, 190, 270, 428, 400, 510], y=[110,75, 180, 350, 220, 138, 375, 435], c='r')
    plt.show()

    #Q4
    epa = pd.read_csv('epa-http.txt', header=None, sep="\t", error_bad_lines=False)
    epa.columns = ['host','date','request','reply', 'bytes']
    epa.date = epa.date.astype('string')
    epa.date = epa.date.str.replace('[','')
    epa.date = epa.date.str.replace(']','')
    epa.date = epa.date.str[:-6]

    busiestHour = epa.groupby('date')

    x5 = []
    y5 = []
    for key, grp in epa.groupby(['date']):
        x = key
        y = grp['bytes'].count()
        x5.append(key)
        y5.append(y)

    time = np.array(x5)
    requests = np.array(y5)
    plt.plot(requests)

    plt.title("Server Requests vs Time")
    plt.xlabel('Hour Index (Starting at 11pm on the 29th)')
    plt.ylabel('Server Requests')

    plt.show()



