def read_input():
    size = int(input())
    data = []
    for row in range(size):
        data.append([float(x) for x in filter(None, input().strip().split(" "))])
    return size, data


def swap(mat, inv, row_id1, row_id2):
    print(f"S {row_id1} {row_id2}")
    mat[row_id1], mat[row_id2] = mat[row_id2], mat[row_id1]
    inv[row_id1], inv[row_id2] = inv[row_id2], inv[row_id1]
    return mat, inv


def multiply(mat, inv, row_id, scalar):
    if abs(scalar - 1) > 0.0000001:
        print(f"M {row_id} {scalar}")
        for i, entry in enumerate(mat[row_id]):
            mat[row_id][i] *= scalar

        for i, entry in enumerate(inv[row_id]):
            inv[row_id][i] *= scalar
    return mat, inv


def add_multiple(mat, inv, row_id1, row_id2, scalar, print_=True):
    if abs(scalar) > 0.0000001:
        if print_:
            print(f"A {row_id1} {row_id2} {scalar}")
        for i, entry in enumerate(mat[row_id1]):
            mat[row_id1][i] += mat[row_id2][i] * scalar

        for i, entry in enumerate(inv[row_id1]):
            inv[row_id1][i] += inv[row_id2][i] * scalar

    return mat, inv


def identity(size):
    mat = []
    for row_i in range(size):
        mat.append([1 if i == row_i else 0 for i in range(size)])
    return mat


def check_row_zero(matrix, row_index):
    for entry in matrix[row_index]:
        if abs(entry) >= 0.000001:
            return False
    return True


def print_mat(matrix):
    for row in matrix:
        for entry in row:
            print(entry, end=" ")
            #print("{:.4f}".format(entry).rjust(12), end="")
        print()
    print()


def solve(matrix, size):
    inverse = identity(size)

    if size == 1:
        if matrix[0][0] == 0:
            return matrix, False
        matrix, inverse = multiply(matrix, inverse, 0, 1/matrix[0][0])
        return inverse, True

    for column_i in range(size):
        if abs(matrix[column_i][column_i]) <= 0.000001:
            if check_row_zero(matrix, column_i):
                matrix, inverse = swap(matrix, inverse, column_i, size-1)
                return inverse, False
            if column_i + 1 < size:
                matrix, inverse = swap(matrix, inverse, column_i, column_i+1)
            if matrix[column_i][column_i] == 0:
                matrix, inverse = add_multiple(matrix, inverse, column_i, column_i+1, -1)
                return inverse, False

        scalar = 1/matrix[column_i][column_i]
        matrix, inverse = multiply(matrix, inverse, column_i, scalar)

        for row_i in range(column_i+1, size):
            matrix, inverse = add_multiple(matrix, inverse, row_i, column_i, -matrix[row_i][column_i]/matrix[column_i][column_i])

    for column_i in range(size-1, 0, -1):
        for row_i in range(0, column_i):
            matrix, inverse = add_multiple(matrix, inverse, row_i, column_i, -matrix[row_i][column_i])

    return inverse, True


size, matrix = read_input()


import numpy as np
# np_mat = np.random.rand(10, 9)
# np_mat = np_mat@np_mat.T
np_mat = np.eye(4)
np_mat[2, :] = 0
np_mat[3, :] = 0
size = np_mat.shape[0]
matrix = np_mat.tolist()

inverse, success = solve(matrix, size)
if success:
    print("SOLUTION")
    print_mat(inverse)
else:
    print("DEGENERATE")


print_mat(matrix)
np_inv = np.array(inverse)
print(np.linalg.norm(np_mat@np_inv - np.eye(size)))
