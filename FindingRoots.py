# Yossi Elgazari ID
# Solal Ohana ID
# Lior Silon ID

import sympy
import sympy as sp
from sympy import ln, Float
from sympy.utilities.lambdify import lambdify
import math


def bisection_method(poli, start_point, end_point, ep=0.0001):
    x = sp.symbols('x')
    f = lambdify(x, poli)
    count = 0
    m = 0
    error = -1 * (ln((ep / (end_point - start_point))) / ln(2))
    print(float(error))
    error = math.ceil(error)
    print(error)
    error = 100
    while abs(end_point - start_point) > ep and count <= error:
        count += 1
        m = start_point + (end_point - start_point) / 2
        if f(start_point) * f(m) < 0:
            end_point = m
        else:
            start_point = m
    if count > error:
        return None, count
    return round(m, 2), count


def newton_raphson(poli, start_point, end_point, ep=0.0001):
    x = sp.symbols('x')
    f = lambdify(x, poli)
    ftag = poli.diff(x)
    ftag = lambdify(x, ftag)
    count = 0
    error = -1 * (ln(ep / (end_point - start_point)) / ln(2))
    error = math.ceil(error)
    xr = start_point
    try:
        xrr = xr - (f(xr) / ftag(xr))
    except ZeroDivisionError:
        print("Division by zero!")
        return None
    while abs(xr - xrr) > ep and count < error:
        count += 1
        xr = xrr
        try:
            xrr = xr - (f(xr) / ftag(xr))
        except ZeroDivisionError:
            print("Division by zero!")
            return None, 0
    if count >= error:
        return None, count
    return round(Float(str(xrr)), 2), count


def secant_method(poli, start_point, end_point, ep=0.0001):
    x = sp.symbols('x')
    f = lambdify(x, poli)
    count = 0
    error = -1 * (ln(ep / (end_point - start_point)) / ln(2))
    error = math.ceil(error)
    xr = start_point
    xrr = end_point
    xrrr = (xr * f(xrr) - xrr * f(xr)) / (f(xrr) - f(xr))
    while abs(xrrr - xrr) > ep and count < error:
        count += 1
        xr = xrr
        xrr = xrrr
        try:
            xrrr = (xr * f(xrr) - xrr * f(xr)) / (f(xrr) - f(xr))
        except ZeroDivisionError:
            print("Division by zero!")
            return None, 0
    if count >= error:
        return None, count
    return round(Float(str(xrrr)), 2), count


def getMash(leftBoundary, rightBoundary, numOfMashes):
    mash = []
    subBoundary = (rightBoundary - leftBoundary) / numOfMashes
    mash.append([leftBoundary, leftBoundary + subBoundary])
    for index in range(numOfMashes - 2):
        mash.append([mash[index][1], mash[index][1] + subBoundary])
    mash.append([mash[numOfMashes - 2][1], rightBoundary])
    for x in mash:
        x[0] = round(x[0], 1)
        x[1] = round(x[1], 1)
    return mash


def divide(polinom, choice, mash, ep=0.00000001):
    solution = set()
    x = sp.symbols('x')
    f = lambdify(x, polinom)
    for border in mash:
        if f(border[0]) * f(border[1]) < 0:
            if choice == 1:
                sol, count = bisection_method(polinom, border[0], border[1], ep)
                if sol is not None:
                    solution.add((sol, count))
            elif choice == 2:
                sol, count = newton_raphson(polinom, border[0], border[1], ep)
                if sol is not None:
                    solution.add((sol, count))
            elif choice == 3:
                sol, count = secant_method(polinom, border[0], border[1], ep)
                if sol is not None:
                    solution.add((sol, count))

    for border in mash:
        if abs(f(border[0])) <= ep:
            solution.add((border[0], 0))
        if abs(f(border[1])) <= ep:
            solution.add((border[1], 0))
    return list(solution)


def main():
    x = sp.symbols('x')
    temp = input("enter your polynom\n")
    p = sympy.parsing.sympy_parser.parse_expr(temp)
    startpoint = float(input("enter the bottom limit\n"))
    endpoint = float(input("enter the upper limit\n"))
    numberofcuts = int(abs(endpoint - startpoint) * 10)
    mash = getMash(startpoint, endpoint, numberofcuts)
    choice = -1
    while choice != 4:
        choice = int(input(
            "1- solve with bisection methon \n"
            "2- solve with newton rapson method \n"
            "3- solve with secant method \n"
            "4- exit the program\n "))
        if choice == 4:
            break
        elif choice != 1 and choice != 2 and choice != 3:
            print("wrong entry choose again")
        else:
            solution = divide(p, choice, mash)
            solution2 = divide(sp.diff(p, x), choice, mash)
            newp = lambdify(x, p)
            for sol in solution2:
                if newp(sol[0]) == 0:
                    solution.append(sol)
            while startpoint <= endpoint:
                if newp(startpoint) == 0:
                    solution.append((startpoint, 0))
                startpoint += 0.1
            printSolution(solution)
    print("goodbye")


def printSolution(solutions):
    count = 1
    for solution in solutions:
        string = f'solution {count}: {solution[0]}, number of iterations for finding root: {solution[1]}'
        if solution[1] == 0:
            string += ', found by borders assignment in function'
        print(string + '\n')




main()
