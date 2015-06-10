import random,pylab, csv
random.seed(75961)  #Nacogdoches!

def readCSV(path):
    rowList = []
    print("Looking in " , path, ' for ' ,path+'cc.csv')
    with open(path+'cc.csv','r', encoding='ascii')  as csvfile:
        myReader = csv.reader(csvfile, delimiter=',')
        for row in myReader:
            rowList.append(row)
    return rowList

def getStats(data):
    '''
    returns teamData : a dictionary of these values
    keyName is team Name
    values are   newLinesofCodeforYear, measuredLOC, yearlyCC
    {teamName:[ newLinesofCodeforYear, measuredLOC, yearlyCC] }
    '''
    numRows = len(data)
    numCols = len(data[8]) #cheating a little here

    #there is probably a better data structure to use here...
    teamData={}

    #get the dictionary keys (team names)
    for i in range(0,19):
        if data[i][0]:
            teamData[data[i][0]]=[]


    #first, get the new lines of code for the year for each team
    newLinesColIndex = 0
    currentIndex=0
    for colName in data[0]:
        if colName=='Yearly Delta':
            newLinesColIndex=currentIndex
        currentIndex+=1
    #now append the new lines of code for each team to list in dictionary
    for name in teamData.keys():
        for row in (0,19):
            if data[0]==name:
                teamData[name]




    print(teamData)

def simpleStats(path):
    '''
    return a dictionary of teamName : (yearlyDelta, measuredLines, coveredLines, currentCC)
    '''
    rowList = []
    retVals={}
    print("Looking in " , path, ' for ' ,path+'cc.csv')
    with open(path+'cc.csv','r', encoding='ascii')  as csvfile:
        myReader = csv.reader(csvfile, delimiter=',')
        for row in myReader:
            rowList.append(row)
    return rowList

def getDeltaLinesHit(deltaOfLinesHit, existingCodeChangeRatio):
    """return the number of lines of code hit this week
    this would normally just be deltaoflineshit but there is some amount of
    existing code that changes and that code is (possibly) already hit
    so don't count it twice
    """
    retVal = deltaOfLinesHit - int((1-existingCodeChangeRatio) * deltaOfLinesHit)
    if retVal <0:
        retVal = 0
    return retVal

def CCGoalHit(velGoal, currentCC, meanAboveGoal, useMaxofCurrentCCOrVel):
    #assumption: that the checkin will be about meanAboveGoal above the velocity goal
    r = random.normalvariate(velGoal + meanAboveGoal*velGoal,.04)

    #small chance the number will be below goal
    if r<velGoal and useMaxofCurrentCCOrVel==True:
        r=max(velGoal, currentCC)
    else:
        r=velGoal
    if r>1.0:
        r=1.0
    return r

def RunTheSim(totalLOC,
              initialCC,
              velGoal,
              avgNewLinesPerWeek,
              existingCodeChangeRatio,
              yearsToRun,
              velWeeklyHitRate,
              pctBoneheadChance,
              useMaxCCorVelGoal):
    #to do: make totalLOC global since this will always revert to original cc
    linesCurrentlyHit = int(totalLOC*initialCC)

    #for graphing, stores weekly values of code coverage velocity, Total Lines and overall coverage
    wCC=[]
    wTL=[]
    wDiff=[]
    weeklyLOC=[]

    for i in range(yearsToRun*52):
        sizeOfChange = abs(random.normalvariate(avgNewLinesPerWeek,avgNewLinesPerWeek*.1))
        actualNewLines=int(existingCodeChangeRatio*sizeOfChange)
        r=random.uniform(0,1)
        if r < velWeeklyHitRate: #then the checkin hits the velocity metrics
            pctHitThisWeek = CCGoalHit(velGoal, linesCurrentlyHit/totalLOC,0.02,useMaxCCorVelGoal)
            assert (pctHitThisWeek<=1.0)
            deltaOfLinesHit = int(pctHitThisWeek* sizeOfChange + 0.5)
            deltaOfLinesHit = getDeltaLinesHit(deltaOfLinesHit, existingCodeChangeRatio)
        else: #this checkin did not hit velocity metrics
            maxHitThisWeek = random.uniform(0.0,velGoal) # TODO: better distribution here
            #- 0.5 when rounding here, round down to punish not meeting goal
            deltaOfLinesHit = int(sizeOfChange* actualNewLines*maxHitThisWeek - 0.5)
            deltaOfLinesHit = getDeltaLinesHit(deltaOfLinesHit, existingCodeChangeRatio)

            #now to really punish - big checkin with no code hit
            #if the checkin was rushed or just (frankly) boneheaded
            if random.uniform(0,1)<pctBoneheadChance:
                #add between 1 and 30% new code to your codebase
                #this really punishes large codebases with low churn - should there be an upper limit?
                #23-30K seems like a more reasonable upper limit, but is is boneheaded by nature...
                actualNewLines+=totalLOC*random.uniform(.01,.3)
        totalLOC+=actualNewLines
        weeklyLOC.append(totalLOC)
        linesCurrentlyHit+=deltaOfLinesHit
        wCC.append(linesCurrentlyHit)
        wTL.append(totalLOC)
        wDiff.append(linesCurrentlyHit/totalLOC)
    return wDiff, totalLOC, weeklyLOC

def plotResults(wDiff, totalLOC, wLoc):
    #format the output string for lines of coverage at end of sim
    endCC = wDiff[-1]  * totalLOC
    endCC=endCC/totalLOC*1000
    endCC=int(endCC+0.5)
    #now plot the weekly total coverage and show
    pylab.subplot(2,1,1)
    #pylab.figure(1)
    pylab.plot(wDiff)
    pylab.xlabel("Weeks")
    pylab.ylabel("Total CC")
    pylab.title('Code Coverage over time\n'+"Start: "+ str(startingCC*100) +'% End: '+ str(endCC/10)+'%' )
    #pylab.figure(2)
    pylab.subplot(2,1,2)
    pylab.plot(wLoc, color='red')
    pylab.xlabel('Weeks')
    pylab.ylabel('Total Lines of Code')
    pylab.title('Total Lines of Code over time')
    pylab.show()



data=simpleStats('h:\\')

resDict={}


for i in range(1,len(data)):
    name=data[i][0]
    initialLOC = int(data[i][2])    #measured
    startingCC = float(data[i][-1])
    velocityGoal=.75
    meanLinesAddedPerWeek = int(data[i][1])/19   #note the magic number based on week 19 data
    existingCodeModifiedPerCent = 0.6 # 60% of a change is to existing code, 1- this number is new code
    yearsToRun=3
    velWeeklyHitRate=1.0
    pctBoneheadCheckin=0.0
    useMaxOfCurrentCCovOrVelGoal=True

    meanLinesAddedPerWeek=int(meanLinesAddedPerWeek)

    resDict[name]=(RunTheSim(initialLOC,
                    startingCC,
                    velocityGoal,
                    meanLinesAddedPerWeek,
                    existingCodeModifiedPerCent,
                    yearsToRun,
                    velWeeklyHitRate,
                    pctBoneheadCheckin,
                    useMaxOfCurrentCCovOrVelGoal))

for key in resDict:
    print(key, round(resDict[key][0][52]*100,1),round(resDict[key][0][-1]*100,1))
