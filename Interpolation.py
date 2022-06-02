import math
from gaussElimination import *


# Solal Ohana
# Lior Shilon
# Yossi Elgazari

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


def printcolored(message):
    if has_numbers(message):
        print("\033[32m{}\033[00m".format(message))
    else:
        print("\033[91m{}\033[00m".format(message))


def bygaussElimination(mat):
    """
    algorithm for solving systems of linear equations

    :param mat: matrix
    """
    currMat = checkPivotMax(mat, [])
    currMat = zeroUnderPivot(currMat, [])
    currMat = zeroAbovePivot(currMat, [])
    currMat = makePivotOne(currMat, [])
    return currMat


def createZeroMatrixInSize(numOfRows, numOfCols):
    """
    returns a zero matrix of size numOfRows x numOfCols represented y a list.

    @param numOfRows: number of rows the matrix has
    @param numOfCols: number of columns the matrix has
    @return: a list of lists representing a 0 matrix of size: numOfRows x numOfCols
    """
    matrix = []
    for i in range(numOfRows):
        tempMatrix = []
        for j in range(numOfCols):
            tempMatrix.append(0)
        matrix.append(tempMatrix)
    return matrix


def extractSolutionColumn(matrix):
    """

    @param matrix: matrix of size N x N+1.
    @return: list representing the solution vector of the matrix
    """
    solutionVector = []
    # indicate also last column of the matrix
    numOfRows = len(matrix)
    for row in range(numOfRows):
        solutionVector.append([matrix[row][numOfRows]])
    return solutionVector


def activateNevilleMethod(xList, yList, x):
    def nevilleMethod(m, n):
        if (m, n) not in resultsDictionary.keys():
            res = (((x - xList[m]) * nevilleMethod(m + 1, n)) - ((x - xList[n]) * nevilleMethod(m, n - 1))) / (
                    xList[n] - xList[m])
            resultsDictionary[(m, n)] = res
        return resultsDictionary[(m, n)]

    printcolored("Activating Neville Interpolation:")
    valuesListSize = len(xList)
    if x in xList:
        print(yList[xList.index(x)])
        return
    firstIndex, secondIndex = getBoundariesIndexOfX(x, xList, valuesListSize)
    if firstIndex is None or secondIndex is None:
        print('The x to approximate its value is not between the range of the given x values')
        return None
    resultsDictionary = createValuesDictionary(valuesListSize, yList)
    for diff in range(1, valuesListSize):
        for index in range(valuesListSize - diff):  # 4  0,1  1,1  2,3
            result = nevilleMethod(index, index + diff)
    printcolored('result: {}'.format(result))
    printcolored("Terminating Neville Interpolation\n")


def getBoundariesIndexOfX(x, xList, size):
    if x < xList[0] or x > xList[size - 1]:
        return None, None
    for i in range(size - 1):
        if xList[i] < x < xList[i + 1]:
            return i, i + 1


"""
def getValue(message, variableType):
    while True:
        try:
            x = variableType(input(message + '\n'))
            break
        except ValueError:
            print('invalid input, please try again.')
    return x


def getListOfValues(size, sign):
    values = []
    for i in range(size):
        val = getValue(f'Please enter {sign}{i + 1}: ', float)
        values.append(val)
    return values
    
def getYAndXLists(size):
    xList = getListOfValues(size, 'x')
    yList = getListOfValues(size, 'y')
    # sorts both lists based on the xList
    xList, yList = zip(*sorted(zip(xList, yList)))
    return xList, yList
"""


def createValuesDictionary(size, yList):
    indexes = list(range(0, size))
    xyDictionary = {}
    for key, val in zip(indexes, yList):
        xyDictionary[(key, key)] = val
    return xyDictionary


def activateLinearInterpolation(xList, yList, x):
    printcolored("Activating Linear Interpolation:")
    valuesListSize = len(xList)
    if x in xList:
        return yList[xList.index(x)]
    index1, index2 = getBoundariesIndexOfX(x, xList, valuesListSize)
    if index1 is None or index2 is None:
        print('The x to approximate its value is not between the range of the given x values')
        return None
    m = (yList[index1] - yList[index2]) / (xList[index1] - xList[index2])
    n = ((yList[index2] * xList[index1]) - (yList[index1] * xList[index2])) / (xList[index1] - xList[index2])
    approximation = round(m * x + n, 9)
    printcolored('result: {}'.format(approximation))
    printcolored("Terminating Linear Interpolation\n")


def activatePolynomialInterpolation(xList, yList, x):
    def initMatrix(mat, size):
        for i in range(size):
            for j in range(size):
                mat[i][j] = pow(xList[i], j)
            mat[i].append(yList[i])
        return mat

    printcolored("Activating Polynomial Interpolation:")
    valuesListSize = len(xList)
    if x in xList:
        return yList[xList.index(x)]
    index1, index2 = getBoundariesIndexOfX(x, xList, valuesListSize)
    if index1 is None or index2 is None:
        print('The x to approximate its value is not between the range of the given x values')
        return None
    matrix = createZeroMatrixInSize(valuesListSize, valuesListSize)
    matrix = initMatrix(matrix, valuesListSize)
    rankedMatrix = bygaussElimination(matrix)
    solutionVector = extractSolutionColumn(rankedMatrix)

    result = 0
    for i in range(valuesListSize):
        result += solutionVector[i][0] * pow(x, i)
    printcolored('result: {}'.format(round(result, 9)))
    printcolored("Terminating Polynomial Interpolation\n")


def activateLagrangeInterpolation(xList, yList, x):
    def Li_x(index):
        res = 1
        for j in range(valuesListSize):
            if j != index:
                res *= (x - xList[j]) / (xList[index] - xList[j])
        return res

    printcolored("Activating Lagrange Interpolation:")
    valuesListSize = len(xList)
    if x in xList:
        return yList[xList.index(x)]
    index1, index2 = getBoundariesIndexOfX(x, xList, valuesListSize)
    if index1 is None or index2 is None:
        print('The x to approximate its value is not between the range of the given x values')
        return None
    result = 0
    for i in range(valuesListSize):
        result += Li_x(i) * yList[i]
    printcolored('result: {}'.format(result))
    printcolored("Terminating Lagrange Interpolation\n")


def activateSplineQubic(xList, yList, x, fTag0, fTagN):
    def createHList():
        res = []
        for i in range(valuesListSize - 1):
            res.append(xList[i + 1] - xList[i])
        print('H: ', res)
        return res

    def createLambdaList():
        res = []
        for i in range(1, len(hList)):
            res.append(hList[i] / (hList[i] + hList[i - 1]))
        print('lambda: ', res)
        return res

    def createMiuList():
        res = []
        for i in range(len(lamdaList)):
            res.append(1 - lamdaList[i])
        print('miu: ', res)
        return res

    def createDList():
        res = []
        for i in range(1, len(hList)):
            di = (6 / (hList[i - 1] + hList[i])) * (
                    ((yList[i + 1] - yList[i]) / hList[i]) - ((yList[i] - yList[i - 1]) / hList[i - 1]))
            res.append(di)
        print('D: ', res)
        return res

    def createNaturalSplineMatrix():
        matrix = createZeroMatrixInSize(valuesListSize, valuesListSize + 1)
        numOfRows = len(matrix)
        matrix[0][0] = 2
        for index in range(1, numOfRows - 1):
            matrix[index][index] = 2
            matrix[index][index - 1] = miuList[index - 1]
            matrix[index][index + 1] = lamdaList[index - 1]
        matrix[numOfRows - 1][numOfRows - 1] = 2
        for index in range(1, numOfRows - 1):
            # last column of every row
            matrix[index][numOfRows] = dList[index - 1]
        return matrix

    printcolored("Activating Natural Spline Cubic Interpolation:")
    valuesListSize = len(xList)
    if x in xList:
        return yList[xList.index(x)]
    hList = createHList()
    lamdaList = createLambdaList()
    miuList = createMiuList()
    dList = createDList()
    # Natural Spline Cubic
    naturalSplineMatrix = createNaturalSplineMatrix()
    solutionVector = extractSolutionColumn(bygaussElimination(naturalSplineMatrix))
    index1, index2 = getBoundariesIndexOfX(x, xList, valuesListSize)
    res1 = ((pow(xList[index2] - x, 3) * solutionVector[index1][0]) + (
            pow(x - xList[index1], 3) * solutionVector[index1][0])) / (6.0 * hList[index1])
    res2 = (((xList[index2] - x) * yList[index1]) + ((x - xList[index1]) * yList[index2])) / hList[index1]
    res3 = (((xList[index2] - x) * solutionVector[index1][0]) + ((x - xList[index1]) * solutionVector[index2][0])) * \
           hList[
               index1] / 6.0
    printcolored('result: {}'.format(res1 + res2 - res3))
    printcolored("Terminating Natural Spline Cubic Interpolation\n")
    # Full Spline Cubic
    printcolored("Activating Full Spline Cubic Interpolation:")
    fullSplineMatrix = eval(repr(naturalSplineMatrix))
    d0 = 6.0 / hList[0] * (((yList[1] - yList[0]) / hList[0]) - fTag0)
    dn = 6.0 / hList[valuesListSize - 2] * (
            fTagN - ((yList[valuesListSize - 1] - yList[valuesListSize - 2]) / hList[0]))
    print('d0: ', d0)
    print('dn: ', dn)
    fullSplineMatrix[0][1] = 1
    fullSplineMatrix[0][valuesListSize] = d0
    fullSplineMatrix[valuesListSize - 1][valuesListSize - 2] = 1
    fullSplineMatrix[valuesListSize - 1][valuesListSize] = dn
    solutionVector = extractSolutionColumn(bygaussElimination(fullSplineMatrix))
    res1 = ((pow(xList[index2] - x, 3) * solutionVector[index1][0]) + (
            pow(x - xList[index1], 3) * solutionVector[index1][0])) / (6.0 * hList[index1])
    res2 = (((xList[index2] - x) * yList[index1]) + ((x - xList[index1]) * yList[index2])) / hList[index1]
    res3 = (((xList[index2] - x) * solutionVector[index1][0]) + ((x - xList[index1]) * solutionVector[index2][0])) * \
           hList[
               index1] / 6.0
    printcolored('result: {}'.format(res1 + res2 - res3))
    printcolored("Terminating Full Spline Cubic Interpolation\n")


"""matrix[0][0] = 2
matrix[0][1] = lamdaList[0]"""

"""
d0: -0.51647
dn = -4.27202533
pi/3: 1.04719755
X: [0, 0.523598776, 0.785398163, 1.57079633]
Y: [0, 0.5, 0.7072, 1]

H: [0.523598776, 0.261799388, 0.785398163] 
lambda: [0.33333333, 0.75]
miu: [0.66666667, 0.25]
D: [-1.2518, -2.3152]

f'(0) = 1
f'(pi/2) = 0
"""

# TODO Parameters for the interpolation functions, change them by choice!
xList = [0, math.pi / 6, math.pi / 4, math.pi / 2]
yList = [0, 0.5, 0.7072, 1]
x = math.pi / 3
# Parameters only for full spline cubic
ftagzero = 0
ftagn = 1


def main(xList, yList, x):
    activateLinearInterpolation(xList, yList, x)
    activatePolynomialInterpolation(xList, yList, x)
    activateLagrangeInterpolation(xList, yList, x)
    activateNevilleMethod(xList, yList, x)
    activateSplineQubic(xList, yList, x, ftagzero, ftagn)


main(xList, yList, x)
