# #!/usr/bin/python
import Tkinter
from Map.MapMain import MapMain
mapInfo = MapMain()
mapArray = mapInfo.mapExample()
numRows = len(mapArray)

canvasWidth = 1000
canvasHeight = 1000

master = Tkinter.Tk()
mainGrid = Tkinter.Canvas (master, width = canvasWidth, height = canvasHeight, bg="Green")

#Difines the size of the squares on the grid
offset = 10
standardSize = 100

#Corddinates for the first square in the grid
X1 = offset
Y1 = offset
X2 = offset + standardSize
Y2 = offset + standardSize

# Takes the martix and converts it into a grid patten baced on the size of the arrays
# Creates the rows
for i in range(len(mapArray)):
    #Creates the Columns
    for j in range(len(mapArray[i])-1):
        mainGrid.create_rectangle(X1,Y1,X2,Y2)
        X1 = X2
        X2 = X2 + standardSize
    mainGrid.create_rectangle(X1,Y1,X2,Y2)
    X1 = offset
    X2 = standardSize + offset
    Y1 = Y2
    Y2 = Y2 + standardSize

mainGrid.pack()
master.mainloop()
