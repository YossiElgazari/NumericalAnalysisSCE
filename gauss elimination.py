def MatrixMul(mat1, mat2):
    newmat = eval(repr(mat1))
    for i in range(len(newmat)):
        for j in range(len(newmat[0])):
            newmat[i][j] = 0
    for i in range(len(newmat)):
        for j in range(len(newmat[0])):
            for k in range(len(newmat)):
                newmat[i][j] = newmat[i][j] + mat1[i][k] * mat2[k][j]
    print_matrix((newmat))


def print_matrix(matrix):
    for row in matrix:
        rowString = ''
        for element in row:
            rowString += f'{str(element)} '
        print(rowString)
    print('')


MatrixMul([[1, 2], [2, 3]], [[3, 4], [4, 5]])
