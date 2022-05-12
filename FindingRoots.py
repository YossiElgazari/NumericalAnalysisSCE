# Yossi Elgazari ID
# Solal Ohana ID
# Lior Silon ID

import sympy
import sympy as sp
from mpmath.libmp.backend import xrange
from sympy import ln, Float
from sympy.utilities.lambdify import lambdify
import math


def bisection_method(poli, start_point, end_point, ep=0.0001):
    """
    Searches for a root of the polynomial given between x values: start point and end point by the bisection method.

    :param poli: sympy polynomial
    :param start_point: float representing the initial x value from which the search for roots starts.
    :param end_point: float representing the final x value which ends the search for roots.
    :param ep: the maximum calculation error.
    :return: a root of the polynomial in the given range if found one, otherwise returns None.
    """
    x = sp.symbols('x')
    f = lambdify(x, poli)
    count = 0
    m = 0
    error = -1 * (ln((ep / (end_point - start_point))) / ln(2))
    error = math.ceil(error)
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
    """
    Searches for a root of the polynomial given between x values: start point and end point by the newton raphson
    method.

    :param poli: sympy polynomial
    :param start_point: float representing the initial x value from which the search for roots starts.
    :param end_point: float representing the final x value which ends the search for roots.
    :param ep: the maximum calculation error.
    :return: a root of the polynomial in the given range if found one, otherwise returns None.
    """
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
    while abs(xr - xrr) > ep and count <= error:
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
    """
    Searches for a root of the polynomial given between x values: start point and end point by the secant method.

    :param poli: sympy polynomial
    :param start_point: float representing the initial x value from which the search for roots starts.
    :param end_point: float representing the final x value which ends the search for roots.
    :param ep: the maximum calculation error.
    :return: a root of the polynomial in the given range if found one, otherwise returns None.
    """
    x = sp.symbols('x')
    f = lambdify(x, poli)
    count = 0
    error = -1 * (ln(ep / (end_point - start_point)) / ln(2))
    error = math.ceil(error)
    xr = start_point
    xrr = end_point
    xrrr = (xr * f(xrr) - xrr * f(xr)) / (f(xrr) - f(xr))
    while abs(xrrr - xrr) > ep and count <= error:
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
    """
    gets a leftBoundary and rightBoundary representing the big range, creates a list of sub-ranges each sub range holds
    a leftBoundary and rightBoundary of its own and the difference between them is constant and equal in each range.

    :param leftBoundary: float representing the X value, the start of the big range.
    :param rightBoundary: float representing the X value, the end of the big range.
    :param numOfMashes:the number of sub-ranges to divide the big range into.
    :return: list of sub-lists each sub-list of size 2 containing a sub-range of ots own, the sub-lists cover the whole
    big range.
    """
    mash = []
    subBoundary = (rightBoundary - leftBoundary) / numOfMashes
    mash.append([leftBoundary, round(leftBoundary + subBoundary, 5)])
    for index in range(numOfMashes - 2):
        mash.append([mash[index][1], round(mash[index][1] + subBoundary, 5)])
    mash.append([round(mash[numOfMashes - 2][1], 5), round(rightBoundary, 5)])
    return mash


def activateIterativeMethod(polinom, method, mash, ep=0.0001):
    """

    :param polinom: sympy polynomial.
    :param method: the method to use for finding the polynomial roots.
    :param mash: a list of sub-ranges, will look for roots in each sub-range.
    :param ep: the maximum calculation error.
    :return: the roots of the polynomial in the given range.
    """
    print(type(method))
    solution = set()
    x = sp.symbols('x')
    f = lambdify(x, polinom)
    for border in mash:
        if f(border[0]) * f(border[1]) < 0:
            sol, count = method(polinom, border[0], border[1], ep)
            if sol is not None:
                solution.add((sol, count))
    return solution


def main():
    """
    the main method, presents a menu for the user that allows him to choose the iterative method for finding polynomial
    roots in the range given by the user.
    """
    x = sp.symbols('x')
    epsilon = 0.0001
    methods = {
        '1': bisection_method,
        '2': newton_raphson,
        '3': secant_method}
    p = x ** 3 - 57.4 * x ** 2 - 3178.4564 * x + 182471.6148  ##### ENTER POLYNOM HERE #####
    startpoint = float(input("enter the bottom limit\n"))
    endpoint = float(input("enter the upper limit\n"))
    numberofcuts = int(abs(endpoint - startpoint) * 10)
    mash = getMash(startpoint, endpoint, numberofcuts)
    choice = -1
    while choice != '4':
        choice = input(
            "1- solve with bisection methon \n"
            "2- solve with newton rapson method \n"
            "3- solve with secant method \n"
            "4- exit the program\n ")
        if choice == '4':
            break
        elif choice != '1' and choice != '2' and choice != '3':
            print("wrong entry choose again")
        else:
            chosenMethod = methods[choice]
            print('Activating', chosenMethod.__name__)
            solution = activateIterativeMethod(p, chosenMethod, mash, epsilon)
            potentialSolutions = activateIterativeMethod(sp.diff(p, x), chosenMethod, mash, epsilon)
            newp = lambdify(x, p)
            for sol in potentialSolutions:
                if abs(newp(sol[0])) <= epsilon:
                    solution.add(sol)
            if abs(newp(mash[0][0])) <= epsilon:
                solution.add((mash[0][0], 0))
            for border in mash:
                if abs(newp(border[1])) <= epsilon:
                    solution.add((border[1], 0))
            solution = list(solution)
            print(solution)
            printSolution(solution)
    print("goodbye")

# [0.1, 0.2] [0.2, 0.3] [0.3, 0.4]


def printSolution(solutions):
    """
    prints all the roots of the polynomial and the amount of iterations the iterative method took to find them.

    :param solutions: list of solutions, each solution is a tuple holding a root of the polynomial and the number
    of iterations it took the iterative method to find the root.
    """
    count = 1
    string = ""
    if len(solutions) == 0:
        print("Did not find any roots between the given boundaries")
    for solution in solutions:
        string = f'solution {count}: {solution[0]}, number of iterations for finding root: {solution[1]}'
        if solution[1] == 0:
            string += ', found by borders assignment in function'
        count += 1
        print(string + '\n')


main()
