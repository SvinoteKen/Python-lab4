import numpy

def matrix_multiplication():
    print('1) умножение произвольных матриц А (размерности 3х5) и В (5х2):')
    a = numpy.arange(15).reshape((3, 5))
    b = numpy.arange(10).reshape((5, 2))
    print('А:\n', a)
    print('В:\n', b)
    print('Итог: \n', a@b)

def vector_multiplication():
    print('\n2) умножение матрицы (5х3) на трехмерный вектор:')
    matrix = numpy.arange(15).reshape((5, 3))
    vector = numpy.array([1, 5, 2], dtype=float)
    print('Матрица:\n', matrix)
    print('Вектор:\n', vector)
    print(matrix@vector)

def linear_equation():
    print('\n3) решение системы линейных уравнений:\n3x+2y=13\n3x-2y=5')
    matrix = numpy.array([[3., 2.], [3., -2.]])
    vector = numpy.array([13., 5.])
    result = numpy.linalg.solve(matrix, vector)
    print('x =', result[0], '\ny =', result[1])

def det_matrix():
    print('4) расчет определителя матрицы: ', end='\n')
    matrix = numpy.array([[0, -1, 0], [1, 3, -2], [2, 5, -1]])
    print(matrix)
    print('Определитель = ', numpy.linalg.det(matrix))

def inverse_matrix():
    print('\n5) получение обратной матрицы:')
    a = numpy.array([[1, 0, 2], [2, -1, 1], [1, 3, -1]])
    print(a, '\n=> ')
    a_invented = numpy.linalg.inv(a)
    print(a_invented)

def transposed_matrix():
    print('\n5) получение транспонированной матрицы: ')
    a = numpy.array([[0, -1, 0], [1, 3, -2], [2, 5, -1]])
    print(a, '\n=> ')
    a = a.transpose()
    print(a)

matrix_multiplication()
vector_multiplication()
linear_equation()
det_matrix()
inverse_matrix()
transposed_matrix()
a = numpy.arange(0.1, 2.6, 0.1).reshape((5, 5))
w, v = numpy.linalg.eig(a)
print('\n', a, '\n', numpy.prod(w), '=', numpy.linalg.det(a))