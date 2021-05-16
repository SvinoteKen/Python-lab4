from sympy import *

def solution(*equations):
    if len(equations) == 1:
        return solve(equations[0])
    return solve_poly_system(equations)

x = Symbol('x')
fun = x + 2
print('Заданная функция: ', str(fun))
print('Производная функции: ', end='')
derivative = diff(fun)
pprint(derivative)
plot(derivative)
print('\nИнтеграл функции: ', end='')
integral = integrate(fun)
pprint(integral)
plot(integral)

x, y = symbols('x y')
eq1 = Equality(0, x - 2*y)
eq2 = Equality(0, y-3)
eq3 = Equality(12, 2*x)
print('\nСистема уравнений:')
pprint(eq1)
pprint(eq2)
print('\nОтвет: ', end='')
pprint(solution(eq1, eq2))
print('\nУравнение:')
pprint(eq3)
print('\nОтвет: ', end='')
pprint(solution(eq3))