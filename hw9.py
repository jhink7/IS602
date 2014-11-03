#########
## Solution for Homework 9
## CUNY IS602
#########

## Justin Hink

if __name__ == "__main__":
    import pandas as pd

    #Q1#
    epa = pd.read_csv('epa-http.txt', header=None, sep="\t", error_bad_lines=False)
    epa.columns = ['host','date','request','reply', 'bytes']

    hostcounts = epa.groupby('host').count().sort('bytes').tail(1).date

    # answer : sandy.rtptok1.epa.gov    294 requests
    print "Q1"
    print "Most requests:"
    print str(hostcounts)
    print ""

    #Q2#
    # create shallow copy as we're going to slice the data frame and we may need the original
    # later
    epa2 = epa.copy()
    epa2 = epa2[epa2['bytes'] != '-']
    epa2['bytes'] = epa2['bytes'].astype('int')

    maxBytes = epa2.groupby('host').sum().sort('bytes').tail(1).bytes
    #answer: piankhi.cs.hamptonu.edu, 7267751 bytes
    print "Q2"
    print "Max bytes received:"
    print maxBytes
    print ""

    #Q3#

    # format the date column into a unique day-hour string
    epa.date = epa.date.astype('string')
    epa.date = epa.date.str.replace('[','')
    epa.date = epa.date.str.replace(']','')
    epa.date = epa.date.str[:-6]

    busiestHour = epa.groupby('date').count().sort('bytes').tail(1).bytes

    #answer 30:14    4716
    print "Q3"
    print "Hour With Most Requests:"
    print busiestHour
    print""

    #Q4#
    # create shallow copy as we're going to slice the data frame and we may need the original
    # later
    epa3 = epa.copy()
    epa3 = epa3[epa3.request.str.contains('.gif')]
    maxGIF = epa3.groupby('request').count().sort('bytes').tail(1).bytes

    #answer circle_logo_small.gif, 3189 GET requests
    print "Q4"
    print "Most Downloaded GIF:"
    print maxGIF
    print""

    #Q5#
    epa = epa[epa['reply'] != 200]
    codes= epa.reply.unique()
    print "Q5"
    print"Response codes other than 200:"
    print codes
    print""
