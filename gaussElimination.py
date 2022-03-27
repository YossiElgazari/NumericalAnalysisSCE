from math import isclose


def checkPivotMax(matrix, elmatlist):
    for row in range(len(matrix)):  # run on every row of the matrix
        max = matrix[row][row]
        index = row
        indexmax = index
        for index in range(row, len(matrix)):
            if max < matrix[index][row]:
                max = matrix[index][row]
                indexmax = index
        if indexmax != row:
            matrix = switchRows(matrix, row, indexmax, elmatlist)
    return matrix


def zeroUnderPivot(matrix, elmatlist):
    for row in range(len(matrix)):
        pivot = matrix[row][row]
        for col in range(row + 1, len(matrix)):
            if matrix[col][row] != 0:
                resetnum = (matrix[col][row] / pivot) * -1
                elmat = createElMat(matrix)
                elmat[col][row] = resetnum
                elmatlist.append(elmat)
                matrix = matrixMul(elmat, matrix)
    return matrix


def zeroAbovePivot(matrix, elmatlist):
    for col in range(1, len(matrix[0]) - 1):
        for row in range(0, col):
            resetnum = (matrix[row][col] / matrix[col][col]) * -1
            elmat = createElMat(matrix)
            elmat[row][col] = resetnum
            elmatlist.append(elmat)
            matrix = matrixMul(elmat, matrix)
    return matrix


def buildZeroMatrix(matrix, numOfPops):
    temp = eval(repr(matrix))
    zeroMatrix = []
    for row in temp:
        for _ in range(0, numOfPops):
            row.pop()
        zeroMatrix.append(row)
    for i in range(0, len(zeroMatrix)):
        for j in range(0, len(zeroMatrix[0])):
            zeroMatrix[i][j] = 0
    return zeroMatrix


def matrixMul(mat1, mat2):
    newmat = eval(repr(mat1))
    newmat = buildZeroMatrix(newmat, 0)
    for i in range(len(newmat)):
        for j in range(len(newmat[0])):
            for k in range(len(newmat)):
                newmat[i][j] = newmat[i][j] + mat1[i][k] * mat2[k][j]
            if isclose(newmat[i][j] + 1, round(newmat[i][j]) + 1):
                newmat[i][j] = round(newmat[i][j])
    return newmat


def createElMat(matrix):
    newmat = buildZeroMatrix(matrix, 0)
    for i in range(0, len(matrix)):
        newmat[i][i] = 1
    return newmat


def makePivotOne(matrix, elmatlist):
    for row in range(len(matrix)):
        if matrix[row][row] != 1:
            elmat = createElMat(matrix)
            elmat[row][row] = pow(matrix[row][row], -1)
            elmatlist.append(elmat)
            matrix = matrixMul(elmat, matrix)
    return matrix


def switchRows(mat, row1, row2, elmatlist):
    newmat = buildZeroMatrix(mat, 0)
    for i in range(0, len(mat)):
        if i == row1:
            newmat[i][row2] = 1
        elif i == row2:
            newmat[i][row1] = 1
        else:
            newmat[i][i] = 1
    elmatlist.append(newmat)
    return matrixMul(newmat, mat)


def restructureElList(eList):
    for mat in eList:
        for row in mat:
            row.pop()


def gaussElimination(mat):
    originalMatrix = eval(repr(mat))  # copy the original matrix
    elementaryMatricesList = []  # create the elementary matrices list
    currMat = checkPivotMax(mat, elementaryMatricesList)
    currMat = zeroUnderPivot(currMat, elementaryMatricesList)
    currMat = zeroAbovePivot(currMat, elementaryMatricesList)
    currMat = makePivotOne(currMat, elementaryMatricesList)
    reversedElist = eval(repr(elementaryMatricesList))
    reversedElist.reverse()
    restructureElList(reversedElist)
    reversedElist.append(originalMatrix)
    reversedElist.append(currMat)
    print('The original matrix\n')
    print_matrix(originalMatrix)
    print('the solution:\n')
    print_matrix(currMat)
    print('Deep dive into the solution')
    printElementaryMatrices(reversedElist)
    print('every multiplication step:')
    elementaryMatricesList.reverse()
    printEveryStepOfSolution(elementaryMatricesList, mat)


    ##########################


def print_matrix(matrix):
    for row in matrix:
        rowString = ''
        for element in row:
            rowString += f'{str(element)} '
        print(rowString)
    print('')


def printElementaryMatrices(elementaryMatricesList):
    # find the longest integer part size of the number which his integer part is the longest from all the matrices
    maxNumberOfIntegerDigits = findMaxLengthNumberInElementaryList(elementaryMatricesList)
    result = ''
    for currentRow in range(0, len(elementaryMatricesList[0])):  # for every row
        result += '\n'
        for currentMatrix in range(0, len(elementaryMatricesList)):  # for every matrix
            for currCol in range(0, len(elementaryMatricesList[currentMatrix][0])):  # for every element
                # calculate the current element integer part length
                currNumOfIntegerDigits = len(str(elementaryMatricesList[currentMatrix][currentRow][currCol]).split('.')[0])
                if currCol == len(elementaryMatricesList[currentMatrix][0]) - 1:  # if in the last col of a matrix
                    for _ in range(maxNumberOfIntegerDigits - currNumOfIntegerDigits, 0, -1):
                        result += ' '
                    if currentRow == len(elementaryMatricesList[0]) // 2:  # if in the row that is the middle row
                        if currentMatrix == len(elementaryMatricesList) - 1:  # if in the last matrix of the array
                            result += f'{elementaryMatricesList[currentMatrix][currentRow][currCol]:.3f}|'
                        elif currentMatrix == len(elementaryMatricesList) - 2:  # if in the previous to the last matrix
                            result += f'{elementaryMatricesList[currentMatrix][currentRow][currCol]:.3f}|   =   |'
                        else:  # another matrix in the array that is not the last or the one before the last
                            result += f'{elementaryMatricesList[currentMatrix][currentRow][currCol]:.3f}|   X   |'
                    else:  # if we are in every row that is not the middle row
                        if currentMatrix == len(elementaryMatricesList) - 1:  # if in the last matrix of the array
                            result += f'{elementaryMatricesList[currentMatrix][currentRow][currCol]:.3f}|'
                        else:  # if not the last matrix of the array
                            result += f'{elementaryMatricesList[currentMatrix][currentRow][currCol]:.3f}|       |'
                else:  # if it's not the last col of a matrix
                    if currentMatrix == 0 and currCol == 0:  # if in the first col of the first matrix
                        result += '|'
                    for _ in range(maxNumberOfIntegerDigits - currNumOfIntegerDigits, 0, -1):
                        result += ' '
                    result += f'{elementaryMatricesList[currentMatrix][currentRow][currCol]:.3f} '

    result += '\n\n'
    print(result)


def findMaxLengthNumberInElementaryList(elementaryMatricesList):
    """
    finds the longest integer part size of all the numbers in a list of matrices
    :param elementaryMatricesList: all the elementary matrices used to reach the solution
    :return: the size of the longest integer part
    """
    maxLength = 0
    for matrix in elementaryMatricesList:  # for every matrix
        for row in matrix:  # for every row in the matrix
            for element in row:  # for every element in the row
                currLength = len(str(element).split('.')[0])  # calculates the number of digits before the decimal point
                if currLength > maxLength:
                    maxLength = currLength
    return maxLength


def printEveryStepOfSolution(elementaryMatricesList, matrix):
    """
    prints all the multiplication with elementary matrices used in order to reach the solution
    :param elementaryMatricesList: all the elementary matrices list
    :param matrix: the original matrix
    """
    currMatrix = eval(repr(matrix))  # copy the last matrix
    while(elementaryMatricesList):  # as long as the list is not empty
        # currMatrix = eval(repr(matrix))  # copy the last matrix
        currElementaryMatrix = elementaryMatricesList.pop()  # pop the next elementary matrix fom the list
        currList = []  # will include [[elementary matrix], [current matrix], [result of the multiplication]]
        currList.append(currElementaryMatrix)
        currList.append(currMatrix)
        # matrix = elementaryMatrix * matrix
        currMatrix = matrixMul(currElementaryMatrix, currMatrix)
        currList.append(currMatrix)
        """for i in range(0, len(matrix)):
            for j in range(0, len(matrix[0])):
                matrix[i][j] = calculate_matrix_index(currMatrix, i, j, currElementaryMatrix)
        currList.append(matrix)  # add the result of the multiplication"""
        printElementaryMatrices(currList)


"""[[3, 15, 3, 7, 37], [11, 9, 2, 8, 55], [2, 5, 3, 7, 1235], [3, 15, 2, 5, 40]]"""
mat1 = [[0, 1, -1, -1], [3, -1, 1, 4], [1, 1, -2, -3]]
gaussElimination(mat1)
