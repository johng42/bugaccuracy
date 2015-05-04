import pylab, matplotlib.pyplot as plt

results = [(16.0, 4953.0, 5008.0, 23.0), (21.0, 6652.0, 3309.0, 18.0), (27.0, 7955.0, 2006.0, 12.0), (34.0, 9017.0, 944.0, 5.0), (37.0, 9443.0, 518.0, 2.0), (38.0, 9867.0, 94.0, 1.0), (39.0, 9901.0, 60.0, 0.0), (39.0, 9947.0, 14.0, 0.0), (39.0, 9960.0, 1.0, 0.0), (39.0, 9961.0, 0.0, 0.0)]
[0.5, 0.667, 0.8, 0.9, 0.95, 0.99, 0.995, 0.999, 0.9999, 0.99999374]
accValues = [0.5, 0.667, 0.8, 0.9, 0.95, 0.99, 0.995, 0.999, 0.9999, 0.99999374]
numActualBugs=39.0


#build 4 charts
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
plt.title("Bogus Failures (False Positives)")
plt.legend(loc=3)

plt.subplot(2,2,4)
plt.plot(accValues, [x[3] for x in results],'r')
plt.xlabel('Test Accuracy')
plt.ylabel('False Negatives')
plt.title("Bugs Missed (False Negatives)")

plt.show()