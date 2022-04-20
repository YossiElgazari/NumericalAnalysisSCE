

def makePivotMax(matrix):
    """
    Moving the maximum number in each column to be on the diagonal

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
    Checks if the matrix is a dominant diagonal matrix

    :param matrix: matrix
    :return: if matrix is dominant diagonal matrix
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
    """
    for row in matrix:
        rowString = ''
        for element in row:
            rowString += f'{str(element)} '
        print(rowString)
    print('')


def empty_matrix(row, col):
    """
    creates a zero matrix of size row x col

    :param row: number of rows
    :param col: number of columns
    :return: zero matrix of size row x col
    """
    matrix = [[0 for _ in range(col)] for _ in range(row)]
    return matrix


def putZeroInDiagonal(matrix):
    """
    creates a matrix similar to 'matrix' except the diagonal is filled with zeroes

    :param matrix: the matrix to copy
    :return: copy of 'matrix' except the diagonal filled with zeroes.
    """
    newMatrix = eval(repr(matrix))
    for row in range(len(matrix)):
        newMatrix[row][row] = 0
    return newMatrix


def putZeroExceptDiagonal(matrix):
    """
    creates a matrix similar to 'matrix' except every element that is not on the diagonal is zero

    :param matrix: the matrix to copy
    :return: copy of 'matrix' except every element that is not on the diagonal is zero
    """
    newMatrix = eval(repr(matrix))
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if row != col:
                newMatrix[row][col] = 0
    return newMatrix


def multiply_matrices(matrix1, matrix2):
    """
    gets 2 matrices of size MxK and KxN, returns a new matrix of size MxN that is the result of the 2 matrices
    multiplication (matrix 1 * matrix 2).

    :param matrix1:matrix of size MxK
    :param matrix2: matrix of size KxN
    :return: new matrix of size MxN
    """
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
    """
    gets 2 matrices of size NxN, returns a new matrix of size NxN that is the result of the 2 matrices
    summation (matrix 1 + matrix 2).

    :param matrix1: matrix of size NxN
    :param matrix2: matrix of size NxN
    :return:
    """
    row1, col1 = len(matrix1), len(matrix1[0])
    row2, col2 = len(matrix2), len(matrix2[0])
    if row1 == row2 and col1 == col2:
        result = [[a + b for a, b in zip(j, l)] for j, l in zip(matrix1, matrix2)]
        return result
    else:
        print("The operation cannot be performed.\n")


def sub_matrices(matrix1, matrix2):
    """
        gets 2 matrices of size NxN, returns a new matrix of size NxN that is the result of the 2 matrices
        subtraction (matrix 1 - matrix 2).

        :param matrix1: matrix of size NxN
        :param matrix2: matrix of size NxN
        :return:
        """
    row1, col1 = len(matrix1), len(matrix1[0])
    row2, col2 = len(matrix2), len(matrix2[0])
    if row1 == row2 and col1 == col2:
        result = [[a - b for a, b in zip(j, l)] for j, l in zip(matrix1, matrix2)]
        return result
    else:
        print("The operation cannot be performed.\n")


def checkclose(mat1, mat2):
    """
    gets 2 col vectors of same size, checks if they are identical with error range of maximum 0.00001

    :param mat1: the first col vector
    :param mat2: the second col vector
    :return: true if the vectors are identical(with error range of 0.00001), false otherwise
    """
    for i in range(len(mat1)):
        if abs(mat1[i][0] - mat2[i][0]) > 0.00001:
            return False
    return True


def yaacobi(matrixA, vectorB):
    """
    finds the solution (if there is one) for a system of equations with n variables and n equations if a form of
    a matrix by Jacobi method (Iterative Methods) calculations

    :param matrixA: the variables coefficients matrix (NxN)
    :param vectorB: the solution column (Nx1)
    :return: the solution if there is one, otherwise informs the user that there is no solution
    """
    # rearranges the matrix so the max element in every column will be on the diagonal
    pivotmaxmat = makePivotMax(matrixA)
    # checks if the matrix is a dominant diagonal matrix
    ismaxdiagonal = checkPivotMax(pivotmaxmat)
    if not ismaxdiagonal:
        print("The matrix is not a dominant diagonal matrix")
    maxiteration = 1000
    # creates a copy of the matrix in size NxN and places 0 in every element that is not on the diagonal
    notdiagmat = putZeroInDiagonal(pivotmaxmat)
    # creates a copy of the matrix in size NxN and places 0 in every element that is on the diagonal
    diagmat = putZeroExceptDiagonal(pivotmaxmat)
    # initialize guess vector to the zero col vector
    guessvec = empty_matrix(len(matrixA), 1)
    # initialize solution vector to be the guess vector except the first element is 1
    solutionvec = eval(repr(guessvec))
    solutionvec[0][0] = 1
    prevGuessVector = eval(repr(solutionvec))
    currNumOfIterations = 0
    # start jacobi method calculation
    while not checkclose(guessvec, prevGuessVector) and (ismaxdiagonal or currNumOfIterations < maxiteration):
        # the guess vector is now our previous guess vector
        prevGuessVector = eval(repr(guessvec))
        currNumOfIterations = currNumOfIterations + 1
        result = f'run number {currNumOfIterations}: '
        # calculate the next guess vector by jacobi method calculation
        solutionvec = sub_matrices(vectorB, multiply_matrices(notdiagmat, guessvec))
        for i in range(len(solutionvec)):
            solutionvec[i][0] = solutionvec[i][0] / diagmat[i][i]
            result += f' {solutionvec[i][0]}'
        guessvec = eval(repr(solutionvec))
        print(result)
    # if the number of iteration reached to the maximum amount of iterations and the matrix is not a diagonal matrix
    if currNumOfIterations >= maxiteration and not ismaxdiagonal:
        print("The matrix isn't converging")
    # if there is a solution
    else:
        if not ismaxdiagonal:
            print("Although the matrix isn't a max diagonal matrix it does converge")
        print(f'number of iterations:{currNumOfIterations}')
        print_matrix(solutionvec)


def zaidel(matrixA, vectorB):
    """
        finds the solution (if there is one) for a system of equations with n variables and n equations if a form of
        a matrix by Gauss Seidel method calculations

        :param matrixA: the variables coefficients matrix (NxN)
        :param vectorB: the solution column (Nx1)
        :return: the solution if there is one, otherwise informs the user that there is no solution
        """
    # rearranges the matrix so the max element in every column will be on the diagonal
    pivotmaxmat = makePivotMax(matrixA)
    # checks if the matrix is a dominant diagonal matrix
    isDominantDiagonalMatrix = checkPivotMax(pivotmaxmat)
    if not isDominantDiagonalMatrix:
        print("No dominant diagonal")
    maxiteration = 1000
    # creates a copy of the matrix in size NxN and places 0 in every element that is not on the diagonal
    notdiagmat = putZeroInDiagonal(pivotmaxmat)
    # creates a copy of the matrix in size NxN and places 0 in every element that is on the diagonal
    diagmat = putZeroExceptDiagonal(pivotmaxmat)
    # initialize guess vector to the zero col vector
    guessvec = empty_matrix(len(matrixA), 1)
    # initialize solution vector to be the guess vector except the first element is 1
    solutionvec = eval(repr(guessvec))
    solutionvec[0][0] = 1
    prevGuessVector = eval(repr(solutionvec))
    currNumOfIterations = 0
    # start Gauss Seidel method calculation
    while not checkclose(guessvec, prevGuessVector) and (isDominantDiagonalMatrix or currNumOfIterations < maxiteration):
        # the guess vector is now our previous guess vector
        prevGuessVector = eval(repr(guessvec))
        currNumOfIterations += 1
        updatingGuessVector = eval(repr(guessvec))
        result = f'run number {currNumOfIterations}: '
        # calculate the next guess vector by Gauss Seidel method calculation
        for i in range(len(guessvec)):
            guessvec[i][0] = vectorB[i][0]
            for y in range(len(matrixA)):
                """guessvec[i][0] = guessvec[i][0] - notdiagmat[i][y] * guessvec[y][0]"""
                guessvec[i][0] = guessvec[i][0] - notdiagmat[i][y] * updatingGuessVector[y][0]
            guessvec[i][0] = guessvec[i][0] / diagmat[i][i]
            updatingGuessVector[i][0] = guessvec[i][0]
            result += f' {updatingGuessVector[i][0]}'
        print(result)
    # if the number of iteration reached to the maximum amount of iterations and the matrix is not a diagonal matrix
    if currNumOfIterations >= maxiteration and not isDominantDiagonalMatrix:
        print("The matrix isn't converging")
    # if there is a solution
    else:
        if not isDominantDiagonalMatrix:
            print("Although the matrix isn't a max diagonal matrix it does converge")
        print(f'number of iterations:{currNumOfIterations}')
        print_matrix(guessvec)


def userMenuForJacobiAndGauss(matrix, vector_b):
    """
    presents the user with a menu that lets him choose between the Jacobi method and the Gauss Seidel method for solving
    a system of equations in a form of a matrix.

    param matrixA: the variables coefficients matrix (NxN)
    param vectorB: the solution column (Nx1)
    """
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


matrixA = [[4, 2, 0], [2, 10, 4], [0, 4, 5]]
vectorB = [[2], [6], [5]]
userMenuForJacobiAndGauss(matrixA, vectorB)

# https://github.com/cullena20/matrix_calculator/blob/main/matrix_calculator.py
