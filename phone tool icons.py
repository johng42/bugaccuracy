John= .189
Rohith = .137
Henry = .030

import pylab
yj=[]
yr=[]
yh=[]
'''
for x in range(0,220):
    yj.append(40)
    yr.append(59)
    yh.append(75)
'''
for x in range(220,2*365):
    yj.append(42+(x-220)*John)
    yr.append(59+(x-220)*Rohith)
    yh.append(75+ (x-220)*Henry)

pylab.xkcd()
pylab.plot(yj, 'r')
pylab.plot(yr, 'g')
pylab.plot(yh, 'k')
pylab.legend(['John','Rohith','Henry'],loc='upper left')
#pylab.figlegend(("John","Rohith","Henry"),"upper left")
pylab.xlabel("Days From May 15, 2015")
pylab.ylabel("Phone Tool Icons")
pylab.title("Earning icons at current velocity")
pylab.show()