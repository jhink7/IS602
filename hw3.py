class CarEvaluation:
    def __init__(self, buying, maint, doors, persons, lug_boot, safety, ovrClass):
        self.Buying = buying
        self.Maintenance = maint
        self.Doors = doors
        self.Persons = persons
        self.Lug_Boot = lug_boot
        self.Safety = safety
        self.Class = ovrClass

        if(safety == "high"):
            self.SafetyBucket = 2
        elif (safety == "med"):
            self.SafetyBucket = 1
        else:
            self.SafetyBucket = 0

        CarEvaluation.carCount += 1


    carCount = 0


def sortbysafety(L, order):  #you fill in the rest
    if (order == "asc"):
        sortedList = sorted(L, key=lambda car: car.SafetyBucket)
    else:
        sortedList = sorted(L, key=lambda car: car.SafetyBucket, reverse=True)
    results = [t.Safety for t in sortedList]
    return sortedList

# This is the main of the program.
if __name__ == "__main__":
    import csv
    import Tkinter, tkFileDialog
    try:
        root = Tkinter.Tk()
        root.withdraw()

        file_path = tkFileDialog.askopenfilename(filetypes=(("CSV files","*.csv"), ("Mac CSV files","*.csv")))
        with open(file_path) as f:
            reader = csv.reader(f)
            evalList = []
            for row in reader:
                #eval = CarEvaluation(row[0], row[1], row[2], row[3], row[4], row[5])
                evalList.append(CarEvaluation(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

            print len(sortbysafety(evalList, "des")[:5])
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
