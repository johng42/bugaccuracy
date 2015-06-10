import random
import pylab, matplotlib.pyplot as plt

#global, needed for plotting
numActualBugs=0

def RunTheSim(testAccy = 0.9,
              pctChanceofRegression = .005,
              linesOfCode = int(3.6*10**6),
              linesOfCodeTestedByAutomation = 10000,
              fullOutput = False,
              fixedSeed = True):
    '''
    Runs a simulation of an automation run
    returns a tuple of truePos,trueNeg,falsePos,falseNeg
    fixedSeed should be left at False, otherwise the number of bugs in each run
    differs so the graphs may show erroneous results
    '''
    if fixedSeed:
        random.seed(75961)
    totalPop=[]
    global numActualBugs
    totalBugsInCode = 0
    cleanLinesOfCode = 0

    print 'creating sim with these values:'
    print 'Test Accuracy =         ',str(testAccy*100.0)+"%"
    if fullOutput:
        print 'Chance of regression =  ',str(pctChanceofRegression*100.0)+"%"
        print 'Lines of Code =         ', linesOfCode
        print 'Lines Test by Scripts = ',linesOfCodeTestedByAutomation

    for i in range(linesOfCode):
        if random.random()<pctChanceofRegression:
            totalPop.append("Real Bug")
            totalBugsInCode+=1
        else:
            totalPop.append("No Bug In Code")
            cleanLinesOfCode+=1
    assert totalBugsInCode + cleanLinesOfCode == len(totalPop)
    if fullOutput:

        print "Regressions   ", totalBugsInCode
        print "Clean lines of code ",cleanLinesOfCode
        print "----------------------"
        print "Total        ", len(totalPop)

    print 'Running tests of subset of codebase'
    numActualBugs = 0.0         #how many bugs there are in the code
    truePositiveCount = 0.0     #this is a valid bug found by the test
    falsePositiveCount = 0.0 #this is a bug labeled as clean code
    trueNegativeCount = 0.0     #count of clean lines of code identified as clean
    falseNegativeCount = 0.0    #this is a clean line of code identified as a bug

    for i in range(linesOfCodeTestedByAutomation):
        thisLineOfCode = totalPop.pop(random.randint(0,len(totalPop)))
        if thisLineOfCode=="Real Bug":
            numActualBugs+=1

        r = random.random()
        if r<=testAccy:
            if thisLineOfCode == "Real Bug":
                truePositiveCount+=1.0
            else:
                trueNegativeCount+=1.0
        else: #the test does the opposite of what we want
            if thisLineOfCode == 'Real Bug':
                #there was a bug but we missed it
                #this should be == actualBugs - truePositiveCount
                falseNegativeCount+=1.0
            else:
                #there is no bug but we tag it as a bug
                falsePositiveCount+=1.0

    print 'Testing Complete\n'

    print "Final Report"
    print "Number of actual Bugs in code is ",numActualBugs
    print "Number of bugs caught was ", truePositiveCount
    print "Number of false positives ", falsePositiveCount
    print '***************************************************\n\n'
    return (truePositiveCount,trueNegativeCount,falsePositiveCount,falseNegativeCount)



accValues = [0.5, 0.667, 0.8, 0.9, 0.95, 0.99, 0.995, 0.999, 0.9999, 0.99999374]
results = []
for i in accValues:
    results.append(RunTheSim(testAccy=i, pctChanceofRegression=0.01))
print results
print accValues

#build 4 charts
plt.xkcd()
plt.subplot(2,2,1)
plt.plot(accValues, [x[0] for x in results],'g')
plt.plot([accValues[0],accValues[-1]], [numActualBugs, numActualBugs],color='k', linewidth = 2, label="Num Bugs")
plt.xlabel('Test Accuracy')
plt.ylabel('True Positives')
plt.title("Actual Bugs Found (True Positive)")
plt.legend(loc=2)

plt.subplot(2,2,3)
plt.plot(accValues,[x[1] for x in results],'g-')
plt.xlabel('Test Accuracy')
plt.ylabel('True Negatives')
plt.title("Working Code Lines Identified (True Negative)")

plt.subplot(2,2,2)
plt.plot(accValues, [x[2] for x in results],'k')
plt.plot([accValues[0],accValues[-1]], [numActualBugs, numActualBugs],color='r', linewidth = 2, label="Num Bugs")
plt.xlabel('Test Accuracy')
plt.ylabel('False Positives')
plt.title("Bogus Failures (False Positives) ")
plt.legend(loc=3)

plt.subplot(2,2,4)
plt.plot(accValues, [x[3] for x in results],'r')
plt.xlabel('Test Accuracy')
plt.ylabel('False Negatives')
plt.title("Bugs Missed (False Negatives)")

plt.show()