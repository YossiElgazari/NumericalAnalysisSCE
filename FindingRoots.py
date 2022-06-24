# Yossi Elgazari ID
# Solal Ohana ID
# Lior Silon ID

import sympy as sp
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
    numOfIterations = 0
    m = 0  # the root to return if found
    maxNumOfIterations = math.ceil(-1 * (ln((ep / (end_point - start_point))) / ln(2)))
    # search for a root with bisection method
    while rootNotFound(start_point, end_point, ep) and numOfIterations <= maxNumOfIterations:
        numOfIterations += 1
        m = start_point + (end_point - start_point) / 2
        # if the root is on the left
        if f(start_point) * f(m) < 0:
            end_point = m
        # if the root is on the right
        else:
            start_point = m
    if numOfIterations > maxNumOfIterations:
        return None, numOfIterations
    return round(m, 5), numOfIterations


def newton_raphson(poli, start_point, end_point, ep=0.0001):
    """
    Searches for a root of the polynomial given between x values: start point and end point by the newton raphson
    method .

    :param poli: sympy polynomial
    :param start_point: float representing the initial x value from which the search for roots starts.
    :param end_point: float representing the final x value which ends the search for roots.
    :param ep: the maximum calculation error.
    :return: a root of the polynomial in the given range if found one, otherwise returns None.
    """
    # initialize polynomial and derivative data.
    x = sp.symbols('x')
    f = lambdify(x, poli)
    ftag = poli.diff(x)
    ftag = lambdify(x, ftag)
    numOfIterations = 0
    maxNumOfIterations = math.ceil(-1 * (ln(ep / (end_point - start_point)) / ln(2)))
    xr = start_point
    try:
        xrr = xr - (f(xr) / ftag(xr))
    except ZeroDivisionError:
        print("Division by zero!")
        return None
    # search for a root with Newton Raphson method
    while rootNotFound(xr, xrr, ep) and numOfIterations <= maxNumOfIterations:
        numOfIterations += 1
        xr = xrr
        try:
            xrr = xr - (f(xr) / ftag(xr))
        except ZeroDivisionError:
            print("Division by zero!")
            return None, 0
    # if a root was not found
    if numOfIterations > maxNumOfIterations:
        return None, numOfIterations
    return round(Float(str(xrr)), 5), numOfIterations


def secant_method(poli, start_point, end_point, ep=0.0001):
    """
    Searches for a root of the polynomial given between x values: start point and end point by the secant method.

    :param poli: sympy polynomial
    :param start_point: float representing the initial x value from which the search for roots starts.
    :param end_point: float representing the final x value which ends the search for roots.
    :param ep: the maximum calculation error.
    :return: a root of the polynomial in the given range if found one, otherwise returns None.
    """
    # initialize polynomial data.
    x = sp.symbols('x')
    f = lambdify(x, poli)
    numOfIterations = 0
    maxNumOfIterations = math.ceil(-1 * (ln(ep / (end_point - start_point)) / ln(2)))
    xr = start_point
    xrr = end_point
    xrrr = (xr * f(xrr) - xrr * f(xr)) / (f(xrr) - f(xr))
    # search for a root with secant method
    while rootNotFound(xrr, xrrr, ep) and numOfIterations <= maxNumOfIterations:
        numOfIterations += 1
        xr = xrr
        xrr = xrrr
        try:
            xrrr = (xr * f(xrr) - xrr * f(xr)) / (f(xrr) - f(xr))
        except ZeroDivisionError:
            print("Division by zero!")
            return None, 0
    # if a root was not found
    if numOfIterations > maxNumOfIterations:
        return None, numOfIterations
    return round(Float(str(xrrr)), 5), numOfIterations


def rootNotFound(start_point, end_point, epsilon):
    """
    checks if an iterative method hasn't converged into a solution yet.

    :param start_point: float representing the smaller X value.
    :param end_point: float representing the bigger X value.
    :param epsilon: maximum error for calculations.
    :return: boolean value, true if the result is not the root.
    """
    return abs(end_point - start_point) > epsilon


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
    # calculate the constant difference between the boundaries of each sub-range
    constantDifference = (rightBoundary - leftBoundary) / numOfMashes
    mash.append([leftBoundary, round(leftBoundary + constantDifference, 5)])
    # for each sub-range
    for index in range(numOfMashes - 2):
        # initialize the left boundary to be the right boundary of the former sub-range
        # and the right boundary to be the left boundary plus the constant difference
        mash.append([mash[index][1], round(mash[index][1] + constantDifference, 5)])
    mash.append([round(mash[numOfMashes - 2][1], 5), round(rightBoundary, 5)])
    return mash


def searchForRoots(polinom, method, mash, ep=0.0001):
    """
    searching for roots of the polynomial in the given range by the given method.

    :param polinom: sympy polynomial.
    :param method: the method to use for finding the polynomial roots.
    :param mash: a list of sub-ranges, will look for roots in each sub-range.
    :param ep: the maximum calculation error.
    :return: the roots of the polynomial in the given range.
    """
    solutions = set()
    # initialize polynomial data
    x = sp.symbols('x')
    f = lambdify(x, polinom)
    for sub_range in mash:
        # if there is x, so f(x) = 0 in the sub-range
        if f(sub_range[0]) * f(sub_range[1]) < 0:
            # activate the given iterative method on this sub-range
            solution, numOfIterations = method(polinom, sub_range[0], sub_range[1], ep)
            # if found a solution: x
            if solution is not None:
                solutions.add((solution, numOfIterations))
    return solutions


def main():
    """
    the main method, presents a menu for the user that allows him to choose the iterative method for finding polynomial
    roots in the range given by the user.
    """
    x = sp.symbols('x')
    epsilon = 0.0001
    # iterative methods dictionary
    methods = {
        '1': bisection_method,
        '2': newton_raphson,
        '3': secant_method}
    # TODO: ↓ ENTER POLYNOMIAL HERE ↓.
    p = x ** 6 - 3 * x ** 5 - 6 * x ** 4 + 10 * x ** 3 + 21 * x ** 2 + 9 * x
    # get range from user
    startpoint = float(input("enter the bottom limit\n"))
    endpoint = float(input("enter the upper limit\n"))
    # calculate the number of sub- ranges to divide the big range into
    numberofcuts = int(abs(endpoint - startpoint) * 10)
    # create the list of sub-ranges
    mash = getMash(startpoint, endpoint, numberofcuts)
    choice = -1
    while choice != '4':
        # get the selected method
        choice = input(
            "1- solve with bisection method \n"
            "2- solve with newton raphson method \n"
            "3- solve with secant method \n"
            "4- exit the program\n ")
        # exit program selected
        if choice == '4':
            break
        # invalid input
        elif choice != '1' and choice != '2' and choice != '3':
            print("wrong entry choose again")
        # activating chosen iterative method
        else:
            chosenMethod = methods[choice]
            print('Activating', chosenMethod.__name__)
            # search for roots with the polynomial
            solutions = searchForRoots(p, chosenMethod, mash, epsilon)
            # search for roots with the derivative
            potentialSolutions = searchForRoots(sp.diff(p, x), chosenMethod, mash, epsilon)
            f = lambdify(x, p)
            for solution in potentialSolutions:
                # if the solution is also the function's root.
                if abs(f(solution[0])) <= epsilon:
                    solutions.add(solution)
            # search for root on the mash boundaries by assignment of the boundary in the function, f(x)
            # check for the first x value in the mash
            if abs(f(mash[0][0])) <= epsilon:
                solutions.add((mash[0][0], 0))
            # check for each x value in the mash
            for border in mash:
                if abs(f(border[1])) <= epsilon:
                    solutions.add((border[1], 0))
            solutions = list(solutions)
            printSolution(solutions)
    print("goodbye")


# [0.1, 0.2] [0.2, 0.3] [0.3, 0.4]


def printSolution(solutions):
    """
    prints all the roots of the polynomial and the amount of iterations the iterative method took to find them.

    :param solutions: list of solutions, each solution is a tuple holding a root of the polynomial and the number
    of iterations it took the iterative method to find the root.
    """
    count = 0
    string = ""
    # did not find aby roots
    if len(solutions) == 0:
        print("Did not find any roots between the given boundaries")
    # found roots
    else:
        for solution in solutions:
            count += 1
            string = "solution {0}: {1}, number of iterations for finding root: {2}".format(count, solution[0],
                                                                                            solution[1])
            # if the number of iteration for finding the root is zero
            if solution[1] == 0:
                # indicate the user it was found by assignment in the function
                string += ', found by borders assignment in function'
            print(string)
    print()


main()
