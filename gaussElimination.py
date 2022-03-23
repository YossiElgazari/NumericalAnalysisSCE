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


"""def solveMatrix(mat, sol):
    pass"""

"""def checkDiagonal(elmatlist, mat):
    def findValidRow(mat, row):
        for i in range(row + 1, len(mat)):
            if mat[i][row] != 0:
                return i
        return -1

    for row in range(len(mat)):
        if mat[row][row] == 0:
            rowNum = findValidRow(mat, row)
            if rowNum == -1:
                for i in range(0, row):
                    if mat[i][row] != 0 and mat[row][i] != 0:
                        rowNum = i
                        break
            mat = switchRows(mat, row, rowNum, elmatlist)
    return mat"""


def gaussElimination(mat):
    originalMatrix = eval(repr(mat))  # copy the original matrix
    elementaryMatricesList = []  # create the elementary matrices list
    currMat = checkPivotMax(mat, elementaryMatricesList)
    currMat = zeroUnderPivot(currMat, elementaryMatricesList)
    print_matrix(currMat)
    currMat = zeroAbovePivot(currMat, elementaryMatricesList)
    currMat = makePivotOne(currMat, elementaryMatricesList)
    print_matrix(currMat)

    ##########################


def print_matrix(matrix):
    for row in matrix:
        rowString = ''
        for element in row:
            rowString += f'{str(element)} '
        print(rowString)
    print('')


"""[[3, 15, 3, 7, 37], [11, 9, 2, 8, 55], [2, 5, 3, 7, 1235], [3, 15, 2, 5, 40]]"""
mat1 = [[0, 1, -1, -1], [3, -1, 1, 4], [1, 1, -2, -3]]
print_matrix(mat1)
gaussElimination(mat1)
