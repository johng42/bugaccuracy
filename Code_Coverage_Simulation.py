import random,pylab, csv
random.seed(75961)  #Nacogdoches!
#random.seed(100)

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


def CCGoalHit(velGoal, currentCC, meanAboveGoal = 0.05):
    #assumption: that the checkin will be about meanAboveGoal above the velocity goal
    r = random.normalvariate(velGoal + meanAboveGoal*velGoal,.04)

    #small chance the number will be below goal
    if r<velGoal:
        r=max(velGoal, currentCC)
        #r=velGoal
    if r>1.0:
        r=1.0
    #print(velocityGoal,currentCC,r)
    return r

def RunTheSim(totalLOC = 10000,
              initialCC = .70,
              velGoal = 0.70 ,
              avgNewLinesPerWeek = 100,
              existingCodeChangeRatio = 0.6,
              yearsToRun=10,
              velWeeklyHitRate = 0.995,
              pctBoneheadChance = 0.0):
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
            pctHitThisWeek = CCGoalHit(velGoal, linesCurrentlyHit/totalLOC, meanAboveGoal=0.05)
            assert (pctHitThisWeek<=1.0)
            deltaOfLinesHit = int(pctHitThisWeek* sizeOfChange + 0.5)
            #but 1-existingcodechangeratio * currentCC is already assumed hit, so subtract that amount
            deltaOfLinesHit = deltaOfLinesHit - int((1-existingCodeChangeRatio) * deltaOfLinesHit)
        else: #this checkin did not hit velocity metrics
            pctHitThisWeek = random.uniform(0.0,velGoal) # TODO: better distribution here
            #- 0.5 when rounding here, round down to punish not meeting goal
            deltaOfLinesHit = int(sizeOfChange* actualNewLines - 0.5)
            deltaOfLinesHit = deltaOfLinesHit - int((1-existingCodeChangeRatio) * deltaOfLinesHit)
            #now to really punish - big checkin with no code hit
            #if the checkin was rushed or just (frankly) boneheaded
            if random.uniform(0,1)<pctBoneheadChance:
                #add between 1 and 30% new code to your codebase
                #this really punishes large codebases - should there be an upper limit?
                #the largest checkin I have seen is 118K LOC and that was a rare event
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


#initialLOC = 13715
#startingCC = .4488
#velocityGoal = max(.75, startingCC)
#meanLinesAddedPerWeek = 93

data=simpleStats('h:\\')

resDict={}


for i in range(1,len(data)):
    name=data[i][0]
    initialLOC = int(data[i][2])    #measured
    startingCC = float(data[i][-1])
    velocityGoal=max(.75, startingCC)
    meanLinesAddedPerWeek = int(data[i][1])/19   #note the magic number based on week 19 data
    existingCodeModifiedPerCent = 0.6 # 60% of a change is to existing code, 1- this number is new code
    yearsToRun=3
    velWeeklyHitRate=1.0
    pctBoneheadCheckin=0.0

    meanLinesAddedPerWeek=int(meanLinesAddedPerWeek)

    resDict[name]=(RunTheSim(initialLOC,
                    startingCC,
                    velocityGoal,
                    meanLinesAddedPerWeek,
                    existingCodeModifiedPerCent,
                    yearsToRun,
                    velWeeklyHitRate,
                    pctBoneheadCheckin))

for key in resDict:
    print(key, round(resDict[key][0][52]*100,1),round(resDict[key][0][-1]*100,1))


'''

wDiff, totalLOC, wLOC = RunTheSim(initialLOC,
                                  startingCC,
                                  velocityGoal,
                                  meanLinesAddedPerWeek,
                                  yearsToRun=3,
                                  velWeeklyHitRate=1,
                                  pctBoneheadChance=0.00)
#plotResults(wDiff,totalLOC, wLOC)
'''
#print("1 year = ", round(wDiff[52]*100,1), " 3 year = ", round(wDiff[-1]*100,1))









