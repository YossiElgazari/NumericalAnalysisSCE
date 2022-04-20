from math import isclose


def makePivotMax(matrix):
    """
    Moving the maximum number in each column to the right spot

    :param matrix: matrix
    :return: new matrix
    """
    for row in range(len(matrix)):
        max = matrix[row][row]
        index = row
        indexmax = index
        for index in range(row, len(matrix)):
            if max < matrix[index][row]:
                max = matrix[index][row]
                indexmax = index
        if indexmax != row:
            matrix = switchRows(matrix, row, indexmax)
    return matrix


def checkPivotMax(matrix):
    """
    Checking if diagonal in matrix is max

    :param matrix: matrix
    :return: if diagonal is max
    """
    for row in range(len(matrix)):
        currentSum = 0
        for col in range(len(matrix[0])):
            if row != col:
                currentSum += abs(matrix[row][col])
        if abs(matrix[row][row]) < currentSum:
            return False
    return True


def switchRows(mat, row1, row2):
    """
    Switching rows in the matrix by multiplying elementary matrix

    :param mat: matrix
    :param row1: number of row
    :param row2: number of row
    :return: matrix after multiplication
    """
    newmat = empty_matrix(len(mat), len(mat[0]))
    for i in range(0, len(mat)):
        if i == row1:
            newmat[i][row2] = 1
        elif i == row2:
            newmat[i][row1] = 1
        else:
            newmat[i][i] = 1
    return multiply_matrices(newmat, mat)


def print_matrix(matrix):
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
    print('')


def empty_matrix(row, col):
    matrix = [[0 for _ in range(col)] for _ in range(row)]
    return matrix


def putZeroInDiagonal(matrix):
    newMatrix = eval(repr(matrix))
    for row in range(len(matrix)):
        newMatrix[row][row] = 0
    return newMatrix


def putZeroExceptDiagonal(matrix):
    newMatrix = eval(repr(matrix))
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if row != col:
                newMatrix[row][col] = 0
    return newMatrix


def multiply_matrices(matrix1, matrix2):
    row1, col1 = len(matrix1), len(matrix1[0])
    row2, col2 = len(matrix2), len(matrix2[0])
    if col1 == row2:
        result = empty_matrix(row1, col2)
        for i in range(len(matrix1)):
            # iterates through rows of matrix1
            for j in range(len(matrix2[0])):
                # iterates through columns of matrix2
                for k in range(len(matrix2)):
                    # iterates through rows of matrix2
                    result[i][j] += matrix1[i][k] * matrix2[k][j]
        return result
    else:
        print("The operation cannot be performed.\n")


def add_matrices(matrix1, matrix2):
    row1, col1 = len(matrix1), len(matrix1[0])
    row2, col2 = len(matrix2), len(matrix2[0])
    if row1 == row2 and col1 == col2:
        result = [[a + b for a, b in zip(j, l)] for j, l in zip(matrix1, matrix2)]
        return result
    else:
        print("The operation cannot be performed.\n")


def sub_matrices(matrix1, matrix2):
    row1, col1 = len(matrix1), len(matrix1[0])
    row2, col2 = len(matrix2), len(matrix2[0])
    if row1 == row2 and col1 == col2:
        result = [[a - b for a, b in zip(j, l)] for j, l in zip(matrix1, matrix2)]
        return result
    else:
        print("The operation cannot be performed.\n")


def checkclose(mat1, mat2):
    for i in range(len(mat1)):
        if abs(mat1[i][0] - mat2[i][0]) > 0.00001:
            return False
    return True


def yaacobi(matrixA, vectorB):
    pivotmaxmat = makePivotMax(matrixA)
    ismaxdiagonal = checkPivotMax(pivotmaxmat)
    if not ismaxdiagonal:
        print("No dominant diagonal")
    maxiteration = 1000
    notdiagmat = putZeroInDiagonal(pivotmaxmat)
    diagmat = putZeroExceptDiagonal(pivotmaxmat)
    guessvec = empty_matrix(len(matrixA), 1)
    solutionvec = eval(repr(guessvec))
    solutionvec[0][0] = 1
    prevGuessVector = eval(repr(solutionvec))
    count = 0
    while not checkclose(guessvec, prevGuessVector) and (ismaxdiagonal or count < maxiteration):
        prevGuessVector = eval(repr(guessvec))
        count = count + 1
        solutionvec = sub_matrices(vectorB, multiply_matrices(notdiagmat, guessvec))
        for i in range(len(solutionvec)):
            solutionvec[i][0] = solutionvec[i][0] / diagmat[i][i]
        guessvec = eval(repr(solutionvec))
    if count >= maxiteration:
        print("The matrix isn't converging")
    else:
        if not ismaxdiagonal:
            print("Although the matrix isn't a max diagonal matrix it does converge")
        print(f'number of iterations:{count}')
        print_matrix(solutionvec)


def zaidel(matrixA, vectorB):
    pivotmaxmat = makePivotMax(matrixA)
    ismaxdiagonal = checkPivotMax(pivotmaxmat)
    if not ismaxdiagonal:
        print("No dominant diagonal")
    maxiteration = 1000
    notdiagmat = putZeroInDiagonal(pivotmaxmat)
    diagmat = putZeroExceptDiagonal(pivotmaxmat)
    guessvec = empty_matrix(len(matrixA), 1)
    solutionvec = eval(repr(guessvec))
    solutionvec[0][0] = 1
    prevGuessVector = eval(repr(solutionvec))
    count = 0
    while not checkclose(guessvec, prevGuessVector) and (ismaxdiagonal or count < maxiteration):
        prevGuessVector = eval(repr(guessvec))
        count += 1
        for i in range(len(guessvec)):
            guessvec[i][0] = vectorB[i][0]
            for y in range(len(matrixA)):
                guessvec[i][0] = guessvec[i][0] - notdiagmat[i][y] * guessvec[y][0]
            guessvec[i][0] = guessvec[i][0] / diagmat[i][i]
    if count >= maxiteration:
        print("The matrix isn't converging")
    else:
        if not ismaxdiagonal:
            print("Although the matrix isn't a max diagonal matrix it does converge")
        print(f'number of iterations:{count}')
        print_matrix(guessvec)


matrixA = [[4, 2, 0], [2, 10, 4], [0, 4, 5]]
vectorB = [[2], [6], [5]]


def userMenuForJacobiAndGauss(matrix, vector_b):
    while True:
        print('1. Gauss Seidel Method')
        print('2. Jacobi Method')
        print('3. Exit')
        userChoice = input('Please choose which method to use:')
        if userChoice == '1':
            zaidel(matrix, vector_b)
        elif userChoice == '2':
            yaacobi(matrix, vector_b)
        elif userChoice == '3':
            break
        else:
            print('Error, Unknown input')


userMenuForJacobiAndGauss(matrixA, vectorB)

# https://github.com/cullena20/matrix_calculator/blob/main/matrix_calculator.py
