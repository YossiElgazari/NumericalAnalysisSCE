from math import isclose


def checkPivotMax(matrix, elmatlist):
    """
    Moving the maximum number in each column to the right spot

    :param matrix: matrix
    :param elmatlist: elementary list
    :return: new matrix
    """
    for row in range(len(matrix)):
        max = abs(matrix[row][row])
        """index = row
        indexmax = index"""
        indexmax = row
        for index in range(row + 1, len(matrix)):
            if max < abs(matrix[index][row]):
                max = abs(matrix[index][row])
                indexmax = index
        if indexmax != row:
            matrix = switchRows(matrix, row, indexmax, elmatlist)
    return matrix


def zeroUnderPivot(matrix, elmatlist):
    """
    Making the numbers below the pivot zero by multiplication of elementary matrices

     :param matrix: matrix
    :param elmatlist: elementary list
    :return: new matrix
    """
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
    """
    Making the numbers above the pivot zero by multiplication of elementary matrices

    :param matrix: matrix
    :param elmatlist: elementary list
    :return: new matrix
    """
    for col in range(1, len(matrix[0]) - 1):
        for row in range(0, col):
            resetnum = (matrix[row][col] / matrix[col][col]) * -1
            elmat = createElMat(matrix)
            elmat[row][col] = resetnum
            elmatlist.append(elmat)
            matrix = matrixMul(elmat, matrix)
    return matrix


def buildZeroMatrix(matrix, numOfPops):
    """
    Create's zero matrix with the same size as matrix and pops the numbers from the end by the number of numOfPops

    :param matrix: matrix
    :param numOfPops: number of pops
    :return new matrix
    """
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
    """
    Multiplication of 2 matrices (mat1 x mat2)

    :param mat1: matrix 1
    :param mat2: matrix 2
    :return: new matrix after multiplication
    """

    newmat = eval(repr(mat2))
    newmat = buildZeroMatrix(newmat, 0)
    for i in range(len(newmat)):
        for j in range(len(newmat[0])):
            for k in range(len(newmat)):
                newmat[i][j] = newmat[i][j] + mat1[i][k] * mat2[k][j]
            if isclose(newmat[i][j] + 1, round(newmat[i][j]) + 1) or isclose(newmat[i][j], round(newmat[i][j])):
                newmat[i][j] = round(newmat[i][j])
    return newmat


def createElMat(matrix):
    """
    Create matrix at the same size as matrix param

    :param matrix: martix
    :return: new matrix
    """
    newmat = buildZeroMatrix(matrix, 0)
    for i in range(0, len(matrix)):
        newmat[i][i] = 1
    return newmat


def makePivotOne(matrix, elmatlist):
    """
    makes the pivot in each row to num 1

    :param matrix: matrix
    :param elmatlist: elementary list
    :return: matrix after multiplication
    """
    for row in range(len(matrix)):
        if matrix[row][row] != 1:
            elmat = createElMat(matrix)
            elmat[row][row] = pow(matrix[row][row], -1)
            elmatlist.append(elmat)
            matrix = matrixMul(elmat, matrix)
    return matrix


def switchRows(mat, row1, row2, elmatlist):
    """
    Switching rows in the matrix by multiplying elementary matrix

    :param mat: matrix
    :param row1: number of row
    :param row2: number of row
    :param elmatlist: elementary list
    :return: matrix after multiplication
    """
    print("row to switch 1: " + str(row1))
    print("row to switch 2: " + str(row2))
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
    """
    change every matrix in the elementary list to nxn form
    :param eList: elementary list
    """
    for mat in eList:
        for row in mat:
            row.pop()


def gaussElimination(mat):
    """
    algorithm for solving systems of linear equations

    :param mat: matrix
    """
    try:
        with open('solution.txt', 'w') as f:
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
            f.write('The original matrix:\n\n')
            print_matrix(originalMatrix, f)
            print('the solution:\n')
            f.write('the solution:\n\n')
            print_matrix(currMat, f)
            print('Deep dive into the solution')
            f.write('Deep dive into the solution\n\n')
            printElementaryMatrices(reversedElist, f)
            print('every multiplication step:')
            f.write('every multiplication step:\n\n')
            elementaryMatricesList.reverse()
            printEveryStepOfSolution(elementaryMatricesList, mat, f)
    except IOError:
        print('Error, problem with the output file')




def print_matrix(matrix, f):
    """
    prints matrix

    :param matrix: matrix
    :param f: file object
    """
    for row in matrix:
        rowString = ''
        for element in row:
            rowString += f'{str(element)} '
        print(rowString)
        f.write(rowString + '\n')
    print('')
    f.write('\n')


def printElementaryMatrices(elementaryMatricesList, f):
    """
    find the longest integer part size of the number which his integer part is the longest from all the matrices

    :param elementaryMatricesList: List of elementary matrices
    :param f: file object
    """
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
    f.write(result)


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


def printEveryStepOfSolution(elementaryMatricesList, matrix, f):
    """
    prints all the multiplication with elementary matrices used in order to reach the solution
    :param elementaryMatricesList: all the elementary matrices list
    :param matrix: the original matrix
    """
    currMatrix = eval(repr(matrix))  # copy the last matrix
    while(elementaryMatricesList):  # as long as the list is not empty
        # currMatrix = eval(repr(matrix))  # copy the last matrix
        currElementaryMatrix = elementaryMatricesList.pop()  # pop the next elementary matrix fom the list
        for row in currElementaryMatrix:  # for every row in the elementary matrix
            row.pop()  # remove the redundant 0 in the end
        currList = []  # will include [[elementary matrix], [current matrix], [result of the multiplication]]
        currList.append(currElementaryMatrix)
        currList.append(currMatrix)
        # matrix = elementaryMatrix * matrix
        currMatrix = matrixMul(currElementaryMatrix, currMatrix)
        currList.append(currMatrix)
        printElementaryMatrices(currList, f)


"""R = int(input("Enter the number of rows:"))
C = int(input("Enter the number of columns:"))

# Initialize matrix
matrix = []
print("Enter the entries rowwise ( indexes [0,0] [0,1] [0,2] [1,1] ... :")

# For user input
for i in range(R):  # A for loop for row entries
    a = []
    for j in range(C):  # A for loop for column entries
        a.append(float(input()))
    matrix.append(a)"""
"""
0  1 -1  -1     3 -1  2  4
3 -1  2   4     1  2 -1 -3
1  2 -1  -3     0  1 -1 -1
"""

matrix = [[0, 1, -1, -1], [3, -1, 1, 4], [1, 1, -2, -3]]
matrix2 = [[0, 1, -1, -1], [3, -1, 2, 4], [1, 2, -1, -3]]
gaussElimination(matrix)
