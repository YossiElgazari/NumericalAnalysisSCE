def buildZeroMatrix(matrix, numOfPops):
    temp = eval(repr(matrix))
    zeroMatrix = []
    for row in temp:
        for _ in range(0, numOfPops):
            row.pop()
        zeroMatrix.append(row)
    for i in range(0, len(zeroMatrix)):
        for j in range(0, len(zeroMatrix)):
            zeroMatrix[i][j] = 0
    return zeroMatrix


def MatrixMul(mat1, mat2):
    newmat = eval(repr(mat1))
    newmat = buildZeroMatrix(newmat, 0)
    for i in range(len(newmat)):
        for j in range(len(newmat[0])):
            for k in range(len(newmat)):
                newmat[i][j] = newmat[i][j] + mat1[i][k] * mat2[k][j]
    return newmat


def checkDiagonal(elmatlist, mat):
    def findValidRow(mat, row):
        for i in range(row + 1, len(mat)):
            if mat[i][row] != 0:
                return i
        return -1

    def switchRows(mat, row1, row2, elMat):
        newmat = buildZeroMatrix(mat, 1)
        for i in range(0, len(mat)):
            if i == row1:
                newmat[i][row2] = 1
            elif i == row2:
                newmat[i][row1] = 1
            else:
                newmat[i][i] = 1
                ##################

    for row in range(len(mat)):
        if mat[row][row] == 0:
            rowNum = findValidRow(mat, row)
            if rowNum == -1:
                for i in range(0, row):
                    if mat[i][row] != 0 and mat[row][i] != 0:
                        ####################
                #remember to return the matrix

def gaussElimination(mat):
    elMatrixlist = []
    checkDiagonal(elMatrixlist, mat)
    ##########################


def print_matrix(matrix):
    for row in matrix:
        rowString = ''
        for element in row:
            rowString += f'{str(element)} '
        print(rowString)
    print('')


print_matrix(MatrixMul([[1, 2], [2, 3]], [[3, 4, 7], [4, 5, 8]]))
