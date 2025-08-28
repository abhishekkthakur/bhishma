## Image extractor

timestep = 1000     # Enter the timestep at which image has to be extracted

datafile = open('compiled_MoV.txt', 'r')
datalines = datafile.readlines()

counter = 0
for i in datalines[timestep:timestep+1]:
    counter = counter + 1
    a = i.strip()
    b = a.split()
    print ('Time: {}'.format(b[0]))
    print ('Alpha ppt: {}'.format(b[1]))
    print ('Beta ppt: {}'.format(b[2]))
    print ('Total energy: {}'.format(b[3]))
    print ('X_alpha: {}'.format(b[4]))
    print ('X_beta: {}'.format(b[5]))
    datafile1 = open('extractedFile.txt', 'w')
    j = 6
    while (j < 65542):
        datafile1.write(str(b[j]) + '\t')
        j = j + 1
    datafile1.close()

datafile.close()

