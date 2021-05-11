print ("Solitaire Simulation")

# drawStack = [[2,"D"],[6,"C"],[12,"L"],[9,"L"],[1,"L"],[8,"L"],[2,"s"],[6,"L"],[9,"D"],[9,"s"],[4,"C"],[3,"C"],]

drawCount = 0
drawStackCards = []
ascStackCards = [[0,"L"],[0,"D"],[0,"S"],[0,"C"]]
descStackCards = []
idxActiveDescStackCards = []

def readFileTXT(sourceFile):
    file1 = open(sourceFile,"r+")
    listOfRows = file1.read().splitlines()
    file1.close()
    return listOfRows

def readDrawStackCards(sourceFile):
    global drawStackCards
    drawStackCards = []
    resultRead = readFileTXT(sourceFile)
    for result in resultRead:
        currentResult = result.split(',')
        drawStackCards.append(currentResult)
    for i in range (len(drawStackCards)):
        drawStackCards[i][0] = int(drawStackCards[i][0])

def readDescStackCards():
    global descStackCards
    descStackCards = []
    for i in range (7):
        currentStack = []
        currentNameFile = "desc"+ str(i+1)+ ".txt"
        # print (currentNameFile)
        currentRead = readFileTXT(currentNameFile)
        for result in currentRead:
            currentResult = result.split(',')
            currentStack.append(currentResult)
        for i in range (len(currentStack)):
            currentStack[i][0] = int(currentStack[i][0])
        descStackCards.append(currentStack)
    
    # resultRead1 = readFileTXT(sourceFile1)
    # for result in resultRead1:
    #     currentResult = result.split(',')
    #     drawStackCards.append(currentResult)
    # for i in range (len(drawStackCards)):
    #     drawStackCards[i][0] = int(drawStackCards[i][0])

def setInitialIdxDescStack():
    global idxActiveDescStackCards
    idxActiveDescStackCards = []
    for i in range (len(descStackCards)):
        idxActiveDescStackCards.append(len(descStackCards[i])-1)

def drawCommand():
    global drawCount
    drawCount = drawCount + 1
    currentEl = drawStackCards.pop(0)
    drawStackCards.append(currentEl)
    print("Draw : " + str(drawStackCards[0][0]) +  str(drawStackCards[0][1]))

def showDraw():
    print("Draw : " + str(drawStackCards[0][0]) +  str(drawStackCards[0][1]))

def showAsc():
    for i in range (4):
        print("A"+str(i) + ": ", end="")
        # for j in range (len(ascStackCards[i])):
        print(str(ascStackCards[i][0]) + str(ascStackCards[i][1]) + " ", end = " ")
        print()

def showDesc():
    for i in range (7):
        print("D"+str(i) + ": ", end="")
        for j in range (len(descStackCards[i])):
            if (j == idxActiveDescStackCards[i]):
                print("//", end = " ")
            print(str(descStackCards[i][j][0]) + str(descStackCards[i][j][1]) + " ", end="")
            # if (j < idxActiveDescStackCards[i]):
            #     print(str(descStackCards[i][j][0]) + str(descStackCards[i][j][1]) + " ", end="")
            # else :
            #     print(str(descStackCards[i][j][0]) + str(descStackCards[i][j][1]) + " ", end="")           
        print()

def isColorDifferent(type1, type2):
    if (type1 == type2):
        return False
    if ((type1 == "L" and type2=="D") or (type1 == "D" and type2=="L")):
        return False
    if ((type1 == "S" and type2=="C") or (type1 == "C" and type2=="S")):
        return False
    return True

def createNewList(i):
    resultList = []
    x1 = idxActiveDescStackCards[i]
    x2 = len(descStackCards[i])-1
    for j in range (x1,x2):
        resultList.append(descStackCards[i][j])
    return resultList
    

def greedyAlgo():
    global drawStackCards
    global ascStackCards
    global descStackCards
    global idxActiveDescStackCards
    global drawCount

    # Melakukan pengecekan proses yang memindahkan sebuah kartu ke 
    # sebuah Stack ascending (Menaik)
    for i in range (7):
        for j in range (4):
            if (descStackCards[i][len(descStackCards[i])-1][1] == ascStackCards[j][1] and descStackCards[i][len(descStackCards[i])-1][0] == ascStackCards[j][0]+1):
                ascStackCards[j][0] = descStackCards[i][len(descStackCards[i])-1][0]
                currentEl = descStackCards[i].pop(len(descStackCards[i])-1)
                idxActiveDescStackCards[i] = idxActiveDescStackCards[i] - 1
                print ("Ke atas")
                drawCount = 0
                return
    for j in range (4):
        if (drawStackCards[0][1] == ascStackCards[j][1] and drawStackCards[0][0] == ascStackCards[j][0]+1):
            ascStackCards[j][0] = drawStackCards[0][0]
            currentEl = drawStackCards.pop(0)
            print ("Ke atas")
            drawCount = 0
            return
    
    # Melakukan pengecekan proses yang memindahkan sebuah kartu atau tumpukan kartu ke 
    # sebuah Stack Descending (MEnurun)
    for i in range (7):
        currentStack = descStackCards[i]
        for j in range (7):
            if (j != i):
                type1 = descStackCards[i][idxActiveDescStackCards[i]][1]
                type2 = descStackCards[j][len(descStackCards[j])-1][1]
                if (descStackCards[i][idxActiveDescStackCards[i]][0] == descStackCards[j][len(descStackCards[j])-1][0]-1 and isColorDifferent(type1, type2)==True):
                    # Pindah
                    if (idxActiveDescStackCards[i] == len(descStackCards[i])-1):
                        descStackCards[j].append(descStackCards[i][idxActiveDescStackCards[i]])
                        descStackCards[i].pop(idxActiveDescStackCards[i])
                        idxActiveDescStackCards[i] = idxActiveDescStackCards[i] - 1
                        print ("Pindah stack 1 card")
                        drawCount = 0
                        return
                    else:
                        curList = createNewList(i)
                        descStackCards[j].extend(curList)
                        idxActiveDescStackCards[i] = idxActiveDescStackCards[i] - 1
                        print ("Pindah stack tumpukan cards")
                        drawCount = 0
                        return
    
    for j in range (7):
        type1 = drawStackCards[0][1]
        type2 = descStackCards[j][len(descStackCards[j])-1][1]
        if (drawStackCards[0][0] == descStackCards[j][len(descStackCards[j])-1][0]-1 and isColorDifferent(type1, type2)==True):
            # Pindah
            descStackCards[j].append(drawStackCards[0])
            currentEl = drawStackCards.pop(0)
            print ("Pindah stack 1 card")
            drawCount = 0
            return
    
    for i in range (4):
        for j in range (7):
            type1 = ascStackCards[i][1]
            type2 = descStackCards[j][len(descStackCards[j])-1][1]
            if (ascStackCards[i][0] == descStackCards[j][len(descStackCards[j])-1][0]-1 and isColorDifferent(type1, type2)==True):
                # Pindah
                descStackCards[j].append([ascStackCards[i][0],ascStackCards[i][1]])
                ascStackCards[i][0] = ascStackCards[i][0] - 1
                print ("Pindah stack 1 card")
                drawCount = 0
                return
    
    # Mengecek apakah proses draw sebuah kartu baru sudah dilakukan berulang
    # Atau belum
    if (drawCount >= len(drawStackCards)):
        print("Restart permainan")
        return
    else:
        drawCommand()
        print("Draw kartu baru")
        return




readDrawStackCards("drawStack.txt")
# print(drawStackCards)
readDescStackCards()
# print(descStackCards)
# print (len(descStackCards[1]))
setInitialIdxDescStack()
# print (idxActiveDescStackCards)
# print(ascStackCards)

print("##################################################")
print("Print Draw")
showDraw()
print ("Print Asc")
showAsc()
print("Print desc")
showDesc()
print("##################################################")

commandInput = input("Masukan Input : ")
while (commandInput == "H"):

    greedyAlgo()
    print("##################################################")
    print("Print Draw")
    showDraw()
    print ("Print Asc")
    showAsc()
    print("Print desc")
    showDesc()
    print("##################################################")

    commandInput = input("Masukan Input : ")
    


# print("Print Draw PART 2")
# showDraw()

# print ("Print Asc")
# showAsc()

# print("Print desc")
# showDesc()