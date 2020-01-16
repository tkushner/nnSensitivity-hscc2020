import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

def plotResults(resultLo, resultHi, fStem):
    #plt.xlim(0,8)
    currentAxis = plt.gca()
    (minL, maxU) = (float('infinity'), -float('infinity'));
    for j in range(7):
        assert(j in resultLo)
        assert(j in resultHi)
        (l,u) = resultLo[j], resultHi[j]
        print('%d --> (%f, %f)' %(j, l, u))
        if (u > maxU):
            maxU = u
        if (l < minL):
            minL = l
        if (u > 0):
            currentAxis.add_patch(Rectangle((j-0.3,0), 0.6,u, color='red'))
            currentAxis.add_patch(Rectangle((j-0.3,l), 0.6,-l, color='blue'))
        else:
            currentAxis.add_patch(Rectangle((j-0.3,l), 0.6,u-l, color='blue'))
    
    plt.xlim(-0.5,6.5)
    plt.ylim(minL-0.5,maxU +0.5)
    indices = range(7)
    labels = []
    for j in indices:
        labels.append('t-%d'%(30-5*j))
    plt.xticks(indices, labels)
    plt.ylabel('BG Difference Range (mg/dl)')
    plt.savefig(fStem+'-data.pdf')
    plt.savefig(fStem+'_plot-data.png')
    print('Saving plot to %s-data.pdf'%fStem)
    #plt.show()
    plt.close()
    
