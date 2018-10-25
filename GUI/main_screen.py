# #!/usr/bin/python
import tkinter
from Map.map_main import MapMain
from People.person import Person
mapInfo = MapMain()
mapArray = mapInfo.mapExample()

#Difines the size of the squares on the grid
offset = 10
standardSize = 80

#Corddinates for the first square in the grid
X1 = offset
Y1 = offset
X2 = offset + standardSize
Y2 = offset + standardSize

#GRID Generation
# Does the maths to see how big the canvus has to be and how many grids to make
numRows = 0
numCol = 0
workingRows = 0
for i in range(len(mapArray)):
    numCol = numCol + 1
    workingRows = 0
    for j in range(len(mapArray[i])):
        workingRows = workingRows + 1
        if workingRows > numRows:
            numRows = workingRows

#print numRows
#print numCol

canvasWidth = standardSize * numRows + (2 * offset)
canvasHeight = standardSize * numCol + (2 * offset)


# master = Tkinter.Tk()
# mainGrid = Tkinter.Canvas (master, width = canvasWidth, height = canvasHeight, bg="Green")
master = tkinter.Tk()
mainGrid = tkinter.Canvas (master, width = canvasWidth, height = canvasHeight, bg="Green")

# Takes the martix and converts it into a grid patten baced on the size of the arrays
# Creates the rows
colour = ""
for i in range(len(mapArray)):
    #Creates the Columns
    for j in range(len(mapArray[i])):
        colour = "gray"
        if mapArray[i][j] != 0:
            colour = "white"
        mainGrid.create_rectangle(X1, Y1, X2, Y2, fill = colour)
        X1 = X2
        X2 = X2 + standardSize
    X1 = offset
    X2 = standardSize + offset
    Y1 = Y2
    Y2 = Y2 + standardSize

#Person Placement
testPerson = Person()
cordiates = testPerson.startingLoc()
personX1 = (cordiates[0] * standardSize) + offset - standardSize
personY1 = (cordiates[1] * standardSize) + offset - standardSize
personX2 = personX1 + standardSize
personY2 = personY1 + standardSize
print(personX1)
print(personY1)
mainGrid.create_oval(personX1,personY1,personX2,personY2, fill= "red")


#Creates the display
mainGrid.pack()
master.mainloop()
