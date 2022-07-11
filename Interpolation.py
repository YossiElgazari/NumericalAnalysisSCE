from gaussElimination import *


# Solal Ohana 336410055
# Lior Shilon 316126143
# Yossi Elgazari 319068920

def print_matrix(matrix):
    """
    prints a matrix so every element will be on the same printing column with all the elements that are on the same
    column with it in the matrix.
    it does so by calculating the longest integer part of a number on the matrix and determine
    the number of spaces before an element with consideration to the element's integer part length

    @param matrix: list representing the matrix to print
    """
    newMatrix = []
    newMatrix.append(matrix)
    maxIntNumberLength = findMaxLengthNumberInElementaryList(newMatrix)
    # print every row of the reverse matrix so numbers in the same col will be on the same col also in the printing
    # determine how many spaces to add before an element by: maxIntNumberLength - currIntNumberLength
    numOfRows = len(matrix)
    numOfCols = len(matrix[0])
    # for each row
    for row in range(0, numOfRows):
        rowStr = '|'
        # for each column
        for col in range(0, numOfCols):
            # calculate the integer part length of the current number
            currIntNumberLength = len(str(matrix[row][col]).split('.')[0])
            # add spaces before the element according to max integer length anf the current number integer length
            for _ in range(maxIntNumberLength - currIntNumberLength, 0, -1):
                rowStr += ' '
            rowStr += f'{matrix[row][col]:.4f} '
            # if it's the last col
            if col == numOfCols - 1:
                rowStr += '|'
        print(rowStr)
    print('\n')


def findMaxLengthNumberInElementaryList(elementaryMatricesList):
    """
    finds the longest integer part size of all the numbers in a list of matrices

    @param elementaryMatricesList: all the elementary matrices used to reach the solution
    @return: the size of the longest integer part
    """
    maxLength = 0
    for matrix in elementaryMatricesList:  # for every matrix
        for row in matrix:  # for every row in the matrix
            for element in row:  # for every element in the row
                currLength = len(str(element).split('.')[0])  # calculates the number of digits before the decimal point
                if currLength > maxLength:
                    maxLength = currLength
    return maxLength


def has_numbers(inputString):
    """
    Checking if there is any digits in the string

    :param inputString: string
    :return: if there digit
    """
    return any(char.isdigit() for char in inputString)


def printcolored(message):
    """
    gets a message to print, if the message contains digits prints the message in Green, otherwise prints in Red.

    :param message: string, the message to print
    """
    if has_numbers(message):
        print("\033[32m{}\033[00m".format(message))
    else:
        print("\033[91m{}\033[00m".format(message))


def bygaussElimination(mat):
    """
    algorithm for solving systems of linear equations

    :param mat: matrix
    """
    # make the matrix a dominant diagonal matrix
    currMat = checkPivotMax(mat, [])
    # rank the matrix
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
    """
    given n points(x,y) build a polynom of rising degree and find an approximation p(x).

    :param xList: list containing float values in ascending order that represent x-axis coordinates
    :param yList: list containing float values of y's so f(xi) = yi
    :param x: float, the value to find its solution.
    """

    def nevilleMethod(m, n):
        """
        fins the result of the polynom(p) that was built from points m to n when assigning x.

        :param m: the smaller index
        :param n: the bigger index
        :return: the result of the polynomial that was built from points small index to bigger index when assigned with x.
        """
        # if we don't have the answer saved in the memo
        if (m, n) not in resultsDictionary.keys():
            # calculate the result of Pm-n.
            res = (((x - xList[m]) * nevilleMethod(m + 1, n)) - ((x - xList[n]) * nevilleMethod(m, n - 1))) / (
                    xList[n] - xList[m])
            # store the result in the memo
            resultsDictionary[(m, n)] = res
        return resultsDictionary[(m, n)]

    printcolored("Activating Neville Interpolation:")
    valuesListSize = len(xList)
    # if the x appears in the xList return the matching y value in yList
    if x in xList:
        print(yList[xList.index(x)])
        return
    # find the points indexes that bound x
    firstIndex, secondIndex = getBoundariesIndexOfX(x, xList, valuesListSize)
    # if x is out of the xList boundaries(extrapolation)
    if firstIndex is None or secondIndex is None:
        print('The x to approximate its value is not between the range of the given x values')
        return None
    # create the memo to store the results in
    resultsDictionary = createValuesDictionary(valuesListSize, yList)
    # runs on all the xList with jumps of 'diff'
    # i.e: diff = 1: (0,1), (1,2), ..., (n-1, n), diff = 2: (0,2), (1,3)...(n-2,n),..., diff = n-1: (0,n-1)
    for diff in range(1, valuesListSize):
        for index in range(valuesListSize - diff):  # 4  0,1  1,1  2,3
            result = nevilleMethod(index, index + diff)
    for key, val in resultsDictionary.items():
        print(f'P{key[0], key[1]} = {val}')
    printcolored('result: {}'.format(result))
    printcolored("Terminating Neville Interpolation\n")


def getBoundariesIndexOfX(x, xList, size):
    """
    find the indexes of the float values in xList that x is between them and returns them.

    :param x: the x to find its boundaries indexes
    :param xList: list containing float values in ascending order to search the boundaries of x in.
    :param size: the size of xList
    :return: indexes of the boundaries of x in the xList.
    """
    # if x is out of boundaries
    if x < xList[0] or x > xList[size - 1]:
        return None, None
    # run on every 2 x values
    for i in range(size - 1):
        # if x value is between them
        if xList[i] < x < xList[i + 1]:
            return i, i + 1


def createValuesDictionary(size, yList):
    """
    returns a dictionary for memoization with the base cases results stored in it.
    i.e: p(0,0) = p(xList[0]) = yList[0]

    :param size: yList size
    :param yList: list containing float values representing experiments results.
    :return: dictionary for memoization with initialized base cases.
    """
    # create a list [0,1,...., yList.size - 1]
    indexes = list(range(0, size))
    xyDictionary = {}
    # initialize base cases, i.e: dict[(0,0)] = yList[0]]
    for key, val in zip(indexes, yList):
        xyDictionary[(key, key)] = val
    return xyDictionary


def activateLinearInterpolation(xList, yList, x):
    """
    approximates p(x) by building a linear equation with the 2 points that are the boundaries of x.

    :param xList: list containing float values in ascending order that represent x-axis coordinates
    :param yList: list containing float values of y's so f(xi) = yi
    :param x: float, the value to find its solution.
    """
    printcolored("Activating Linear Interpolation:")
    valuesListSize = len(xList)
    # if the x appears in the xList return the matching y value in yList
    if x in xList:
        return yList[xList.index(x)]
    # find the points indexes that bound x
    index1, index2 = getBoundariesIndexOfX(x, xList, valuesListSize)
    # if x is out of the xList boundaries(extrapolation)
    if index1 is None or index2 is None:
        print('The x to approximate its value is not between the range of the given x values')
        return None
    # creates linear equation y = m*x + n
    m = (yList[index1] - yList[index2]) / (xList[index1] - xList[index2])
    print('m:', m)
    n = ((yList[index2] * xList[index1]) - (yList[index1] * xList[index2])) / (xList[index1] - xList[index2])
    print('n:', n)
    print(f'linear equation: y = {m}x+{n}')
    approximation = round(m * x + n, 9)
    printcolored('result: {}'.format(approximation))
    printcolored("Terminating Linear Interpolation\n")


def activatePolynomialInterpolation(xList, yList, x):
    """
    given n+1 points, build a polynomila of degree n and finds p(x)

    :param xList: list containing float values in ascending order that represent x-axis coordinates
    :param yList: list containing float values of y's so f(xi) = yi
    :param x: float, the value to find its solution.
    """

    def initMatrix(mat, size):
        """
        gets a list representing a matrix of size: sizeXsize, build the matrix used the polynomial interpolation method
        returns a matrix of size: sizeXsize+1 containing the solution column.

        :param mat: list of lists, the matrix to initialize.
        :param size: the size of cols and rows
        :return: a matrix of size: sizeXsize+1 used in the polynomial interpolation.
        """
        # for every row
        for i in range(size):
            # for every column
            for j in range(size):
                mat[i][j] = pow(xList[i], j)
            # add the solution column to the end of every row
            mat[i].append(yList[i])
        return mat

    printcolored("Activating Polynomial Interpolation:")
    valuesListSize = len(xList)
    # if the x appears in the xList return the matching y value in yList
    if x in xList:
        return yList[xList.index(x)]
    # find the points indexes that bound x
    index1, index2 = getBoundariesIndexOfX(x, xList, valuesListSize)
    # if x is out of the xList boundaries(extrapolation)
    if index1 is None or index2 is None:
        print('The x to approximate its value is not between the range of the given x values')
        return None
    # creates the 0 matrix of size NxN
    matrix = createZeroMatrixInSize(valuesListSize, valuesListSize)
    # initialize the matrix for finding the answer for p(x)
    matrix = initMatrix(matrix, valuesListSize)
    print('matrix for calculations:')
    print_matrix(matrix)
    # rank the matrix
    rankedMatrix = bygaussElimination(matrix)
    print('ranked matrix:')
    print_matrix(rankedMatrix)
    # extract the solution column of the ranked matrix
    solutionVector = extractSolutionColumn(rankedMatrix)
    # calculate the answer
    result = 0
    for i in range(valuesListSize):
        print('current result:', result)
        result += solutionVector[i][0] * pow(x, i)
    printcolored('final result: {}'.format(round(result, 9)))
    printcolored("Terminating Polynomial Interpolation\n")


def activateLagrangeInterpolation(xList, yList, x):
    """
    finds an approximation for the y value of x by creating a polynomial that goes through a single point but
    is zero for every other point.
    Pn(x) = i=1...n(Li(x) * Yi)

    :param xList: list containing float values in ascending order that represent x-axis coordinates
    :param yList: list containing float values of y's so f(xi) = yi
    :param x: float, the value to find its solution.
    """

    def Li_x(index):
        """
        calculates Li(x).
        Li(x) = j= 0...n(i != j) ((X - Xj) / (Xi - Xj))

        :param index:the index of the x value we are iterating on in the xList
        :return: Li(x)
        """
        res = 1
        for j in range(valuesListSize):
            if j != index:
                res *= (x - xList[j]) / (xList[index] - xList[j])
        return res

    printcolored("Activating Lagrange Interpolation:")
    valuesListSize = len(xList)
    # if the x appears in the xList return the matching y value in yList
    if x in xList:
        return yList[xList.index(x)]
    # find the points indexes that bound x
    index1, index2 = getBoundariesIndexOfX(x, xList, valuesListSize)
    # if x is out of the xList boundaries(extrapolation)
    if index1 is None or index2 is None:
        print('The x to approximate its value is not between the range of the given x values')
        return None
    result = 0
    # Pn(x) = i=1...n(Li(x) * Yi)
    for i in range(valuesListSize):
        result += Li_x(i) * yList[i]
        print('temp result:', result)
    printcolored('final result: {}'.format(result))
    printcolored("Terminating Lagrange Interpolation\n")


def activateSplineQubic(xList, yList, x, fTag0, fTagN):
    """
    calculates an approximation for p(x) based on the given points values by using both natural and full cubic spline

    :param xList: list containing float values in ascending order that represent x-axis coordinates
    :param yList: list containing float values of y's so f(xi) = yi
    :param x: float, the value to find its solution.
    :param fTag0: float value, representing f'(xList[0]), used for full spline cubic.
    :param fTagN: float value, representing f'(xList[n]), used for full spline cubic.
    """

    def createHList():
        """
        creates a list of flaot values representing distances between every 2 adjacent points.
        Hi = Xi+1 - Xi

        :return: a list containing the distances between every 2 adjacent points.
        """
        res = []
        for i in range(valuesListSize - 1):
            res.append(xList[i + 1] - xList[i])
        print('H: ', res)
        return res

    def createLambdaList():
        """
        uses equation: lamda_i = hList_i / (hList_i-1 + hList_i).

        :return:list containing all the lamda values.
        """
        res = []
        for i in range(1, len(hList)):
            res.append(hList[i] / (hList[i] + hList[i - 1]))
        print('lambda: ', res)
        return res

    def createMiuList():
        """
        uses equation: miu_i = 1 - lamdaList[i].

        :return: list of all the miu values.
        """
        res = []
        for i in range(len(lamdaList)):
            res.append(1 - lamdaList[i])
        print('miu: ', res)
        return res

    def createDList():
        """
        uses equation: Di = (6 / (hList_i-1 + hList_i)) * ( ( (Fi+1 - Fi) / Hi ) - ( (Fi - Fi-1) / Hi-1 ) )

        :return:
        """
        res = []
        for i in range(1, len(hList)):
            di = (6 / (hList[i - 1] + hList[i])) * (
                    ((yList[i + 1] - yList[i]) / hList[i]) - ((yList[i] - yList[i - 1]) / hList[i - 1]))
            res.append(di)
        print('D: ', res)
        return res

    def createNaturalSplineMatrix():
        """
        creates matrix for natural spline cubic.

        :return: the matrix.
        """
        # creates 0 matrix of size NxN+1
        matrix = createZeroMatrixInSize(valuesListSize, valuesListSize + 1)
        numOfRows = len(matrix)
        matrix[0][0] = 2
        # for every row in the matrix starting from the second row
        for index in range(1, numOfRows - 1):
            # initialize diagonal value
            matrix[index][index] = 2
            # initialize the value that is left to the diagonal
            matrix[index][index - 1] = miuList[index - 1]
            # initialize the value that is right to the diagonal
            matrix[index][index + 1] = lamdaList[index - 1]
            # initialize the last column (solution column) value
            matrix[index][numOfRows] = dList[index - 1]
        matrix[numOfRows - 1][numOfRows - 1] = 2
        """for index in range(1, numOfRows - 1):
            # last column of every row
            matrix[index][numOfRows] = dList[index - 1]"""
        return matrix

    printcolored("Activating Natural Spline Cubic Interpolation:")
    valuesListSize = len(xList)
    # if the x appears in the xList return the matching y value in yList
    if x in xList:
        return yList[xList.index(x)]
    # preprocessing
    hList = createHList()
    lamdaList = createLambdaList()
    miuList = createMiuList()
    dList = createDList()
    """Natural Spline Cubic"""
    # initialize matrix for natural spline cubic
    naturalSplineMatrix = createNaturalSplineMatrix()
    print("natural spline matrix:")
    print_matrix(naturalSplineMatrix)
    # extract the solution column from the ranked matrix
    solutionVector = extractSolutionColumn(bygaussElimination(naturalSplineMatrix))
    # find the points indexes that bound x
    index1, index2 = getBoundariesIndexOfX(x, xList, valuesListSize)
    # calculate result
    res1 = ((pow(xList[index2] - x, 3) * solutionVector[index1][0]) + (
            pow(x - xList[index1], 3) * solutionVector[index1][0])) / (6.0 * hList[index1])
    res2 = (((xList[index2] - x) * yList[index1]) + ((x - xList[index1]) * yList[index2])) / hList[index1]
    res3 = (((xList[index2] - x) * solutionVector[index1][0]) + ((x - xList[index1]) * solutionVector[index2][0])) * \
           hList[
               index1] / 6.0
    printcolored('result: {}'.format(res1 + res2 - res3))
    printcolored("Terminating Natural Spline Cubic Interpolation\n")
    """Full Spline Cubic"""
    printcolored("Activating Full Spline Cubic Interpolation:")
    fullSplineMatrix = eval(repr(naturalSplineMatrix))
    # calculate d0, dn
    d0 = 6.0 / hList[0] * (((yList[1] - yList[0]) / hList[0]) - fTag0)
    dn = 6.0 / hList[valuesListSize - 2] * (
            fTagN - ((yList[valuesListSize - 1] - yList[valuesListSize - 2]) / hList[0]))
    print('d0: ', d0)
    print('dn: ', dn)
    # lambda[0]
    fullSplineMatrix[0][1] = 1
    fullSplineMatrix[0][valuesListSize] = d0
    # miu[n]
    fullSplineMatrix[valuesListSize - 1][valuesListSize - 2] = 1
    fullSplineMatrix[valuesListSize - 1][valuesListSize] = dn
    print("full spline matrix:")
    print_matrix(fullSplineMatrix)
    # extract the solution column from the ranked matrix
    solutionVector = extractSolutionColumn(bygaussElimination(fullSplineMatrix))
    # calculate result
    res1 = ((pow(xList[index2] - x, 3) * solutionVector[index1][0]) + (
            pow(x - xList[index1], 3) * solutionVector[index1][0])) / (6.0 * hList[index1])
    res2 = (((xList[index2] - x) * yList[index1]) + ((x - xList[index1]) * yList[index2])) / hList[index1]
    res3 = (((xList[index2] - x) * solutionVector[index1][0]) + ((x - xList[index1]) * solutionVector[index2][0])) * \
           hList[
               index1] / 6.0
    printcolored('result: {}'.format(res1 + res2 - res3))
    printcolored("Terminating Full Spline Cubic Interpolation\n")


def main():
    # TODO Parameters for the interpolation functions, change them by choice!
    xList = [1, 2, 3, 4, 5]
    yList = [1, 2, 1, 1.5, 1]
    x = 1.5
    # Parameters only for full spline cubic
    ftagzero = 0
    ftagn = 1

    activateLinearInterpolation(xList, yList, x)
    activatePolynomialInterpolation(xList, yList, x)
    activateLagrangeInterpolation(xList, yList, x)
    activateNevilleMethod(xList, yList, x)
    activateSplineQubic(xList, yList, x, ftagzero, ftagn)


# main
if __name__ == '__main__':
    main()
