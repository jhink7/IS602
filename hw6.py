#1. fill in this function
#   it takes a list for input and return a sorted version
#   do this with a loop, don't use the built in list functions
def sortwithloops(input):
    return qsort(input, 0,len(input)-1)
	
#2. fill in this function
#   it takes a list for input and return a sorted version
#   do this with the built in list functions, don't us a loop
def sortwithoutloops(input):
    input.sort()
    return input

def sortwithnumpy(input):
    ret = np.array(input)
    return ret

#3. fill in this function
#   it takes a list for input and a value to search for
#	it returns true if the value is in the list, otherwise false
#   do this with a loop, don't use the built in list functions
def searchwithloops(input, value):
    for i in range(0, len(input) - 1):
        if(input[i] == value):
            return True
    return False

#4. fill in this function
#   it takes a list for input and a value to search for
#	it returns true if the value is in the list, otherwise false
#   do this with the built in list functions, don't use a loop
def searchwithoutloops(input, value):
    return 	value in input

def searchwithnumpy(l, value):
    ret = len(np.where(np.array(l) == value)[0])
    return ret > 0

# parition funciton used in quick sort
def splitfn(input, start, end):
    pivot = input[start]
    left = start+1

    right = end
    done = False
    while not done:
        while left <= right and input[left] <= pivot:
            left = left + 1
        while input[right] >= pivot and right >=left:
            right = right -1
        if right < left:
            done= True
        else:

            temp=input[left]
            input[left]=input[right]
            input[right]=temp

    temp=input[start]
    input[start]=input[right]
    input[right]=temp
    return right

# quick sort algo entry point
def qsort(myList, startindex, endindex):
    if startindex < endindex:
        # split list into 2 partitions
        split = splitfn(myList, startindex, endindex)
        # do both halves
        qsort(myList, startindex, split-1)
        qsort(myList, split+1, endindex)
    return myList

if __name__ == "__main__":
    import timeit
    import numpy as np

    L = [5,3,6,3,13,5,6]

    print sortwithloops(L) # [3, 3, 5, 5, 6, 6, 13]
    print sortwithoutloops(L) # [3, 3, 5, 5, 6, 6, 13]
    print sortwithnumpy(L)
    print searchwithloops(L, 5) #true
    print searchwithloops(L, 11) #false
    print searchwithoutloops(L, 5) #true
    print searchwithoutloops(L, 11) #false
    print searchwithnumpy(L, 5)
    print searchwithnumpy(L, 11)

    #run each test 100000 times
    numiterations = 100000

    #setup a timer for each function
    t1 = timeit.Timer(stmt="sortwithnumpy(L)", setup="from __main__ import sortwithnumpy, L")
    t2 = timeit.Timer(stmt="sortwithoutloops(L)", setup="from __main__ import sortwithoutloops, L")
    t3 = timeit.Timer(stmt="sortwithloops(L)", setup="from __main__ import sortwithloops, L")
    t4 = timeit.Timer(stmt="searchwithnumpy(L,5)", setup="from __main__ import searchwithnumpy, L")
    t5 = timeit.Timer(stmt="searchwithoutloops(L,5)", setup="from __main__ import searchwithoutloops, L")
    t6 = timeit.Timer(stmt="searchwithloops(L,5)", setup="from __main__ import searchwithloops, L")

    #print out the results
    print "Sort using numpy: "+str(numiterations) +" loops = " + str(t1.timeit(number=numiterations)) +"s"
    print "Sort using built in python: "+str(numiterations) +" loops = " + str(t2.timeit(number=numiterations)) +"s"
    print "Sort using iteration: "+str(numiterations) +" loops = " + str(t3.timeit(number=numiterations)) +"s"
    print "Search using numpy: "+str(numiterations) +" loops = " + str(t4.timeit(number=numiterations)) +"s"
    print "Search using built in python: "+str(numiterations) +" loops = " + str(t5.timeit(number=numiterations)) +"s"
    print "Search using iterations: "+str(numiterations) +" loops = " + str(t6.timeit(number=numiterations)) +"s"
