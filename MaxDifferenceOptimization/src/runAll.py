from IGModelConformanceTesting import processIGFile

M1_network = '../../BGNetworks/M1_Regular_APNN'
M2_network = '../../BGNetworks/M2_SplitLayer_APNN'
M3_network = '../../BGNetworks/M3_WeightCons_APNN'
outputDir = '../outputs'

def runForFigure4():
    print('Generating Data for Figure 4. ')
    processIGFile(M1_network, outputDir+'/'+'M1_40_400_5_25', 400, 40, 5.0, 25)
    processIGFile(M2_network, outputDir+'/'+'M2_40_400_5_25', 400, 40, 5.0, 25)
    processIGFile(M3_network, outputDir+'/'+'M3_40_400_5_25', 400, 40, 5.0, 25)
    print('Figure 4 Data can be found in %s / M1_40_400_5_25_plot.png, M2_40_400_5_25_plot.png, M3_40_400_5_25_plot.png ' % outputDir)

def runForFigure6():
    print('Generating Data for Figure 6. ')
    processIGFile(M1_network, outputDir+'/'+'M1_40_70_5_15', 70, 40, 5.0, 15)
    processIGFile(M2_network, outputDir+'/'+'M2_40_70_5_15', 70, 40, 5.0, 15)
    processIGFile(M3_network, outputDir+'/'+'M3_40_70_5_15', 70, 40, 5.0, 15)
    processIGFile(M1_network, outputDir+'/'+'M1_70_180_5_15', 180, 70, 5.0, 15)
    processIGFile(M2_network, outputDir+'/'+'M2_70_180_5_15', 180, 70, 5.0, 15)
    processIGFile(M3_network, outputDir+'/'+'M3_70_180_5_15', 180, 70, 5.0, 15)
    processIGFile(M1_network, outputDir+'/'+'M1_180_300_5_15', 300, 180, 5.0, 15)
    processIGFile(M2_network, outputDir+'/'+'M2_180_300_5_15', 300, 180, 5.0, 15)
    processIGFile(M3_network, outputDir+'/'+'M3_180_300_5_15', 300, 180, 5.0, 15)
    print('Figure 6 Data can be found in %s / M*_40_70_5_15_plot.png, M*_70_180_5_15_plot.png,M*_180_300_5_15_plot.png' % outputDir)


def runForFigure7():
     print('Generating Data for Figure 7. ')
     processIGFile(M1_network, outputDir+'/'+'M1_70_180_5_25', 180, 70, 5.0, 25)
     processIGFile(M2_network, outputDir+'/'+'M2_70_180_5_25', 180, 70, 5.0, 25)
     processIGFile(M3_network, outputDir+'/'+'M3_70_180_5_25', 180, 70, 5.0, 25)
     print('Done')

if __name__=='__main__':
    runForFigure4()
    runForFigure6()
    runForFigure7()
    
