## Loading and reading the extracted image file
datafile = open('extractedFile.txt', 'r')
datalines = datafile.readlines()
colors = []
for i in datalines:
    a = i.strip()
    b = a.split()  # This is the color
    for j in b:
        colors.append(float(j))
datafile.close()

print (colors)
print (len(colors))
print (type(colors))
