import math
import sympy as sp


def dividesection(leftbound, rightbound, numberofsections):
    """
    dividing the boundaries into sections in list [0.1,0.2] [0.2,0.3] ....

    :param leftbound:  left boundary
    :param rightbound: right boundary
    :param numberofsections: number of sections
    :return: list of sections
    """
    dist = (rightbound - leftbound) / numberofsections
    sectionslist = []
    while (leftbound < rightbound):
        sectionslist.append([leftbound, leftbound + dist])
        leftbound = leftbound + dist
    return sectionslist


def Trapezemethod(leftboundary, rightboundary, function):
    """
    Calculates the integral of the function between the borders

    :param leftboundary:  left boundary
    :param rightboundary: right boundary
    :param function: function
    :return: integral
    """

    def calculateIntegral(integral, sections):
        for section in sections:
            integral = integral + 0.5 * (section[1] - section[0]) * (f(section[0]) + f(section[1]))
        return integral

    x = sp.symbols('x')
    f = sp.utilities.lambdify(x, function)
    numofsection = 10
    section = dividesection(leftboundary, rightboundary, numofsection)
    oldintegral = 0
    oldintegral = calculateIntegral(oldintegral, section)
    numofsection += 10
    section = dividesection(leftboundary, rightboundary, numofsection)
    newintegral = 0
    newintegral = calculateIntegral(newintegral, section)
    while abs(newintegral - oldintegral) > 0.0001:
        oldintegral = newintegral
        numofsection += 10
        section = dividesection(leftboundary, rightboundary, numofsection)
        newintegral = 0
        newintegral = calculateIntegral(newintegral, section)
    return newintegral


def callsympsonmethod(leftboundary, rightboundary, function):
    """
    Activates sympsonMethod untill the difference will match the precise that we chose

    :param leftboundary:  left boundary
    :param rightboundary: right boundary
    :param function: function
    :return: integral
    """
    numofsection = 10
    oldintegral = sympsonMethod(leftboundary, rightboundary, function, numofsection)
    print(oldintegral)
    numofsection += 10
    newintegral = sympsonMethod(leftboundary, rightboundary, function, numofsection)
    print(newintegral)
    while abs(newintegral - oldintegral) > 0.0000001:
        oldintegral = newintegral
        newintegral = 0
        numofsection += 10
        newintegral = sympsonMethod(leftboundary, rightboundary, function, numofsection)
        print(newintegral)
    return newintegral


def sympsonMethod(leftBoundary, rightBoundary, polynomial, numofsection):
    """
    calculates the integral of the polynomial between the range leftBoundary to rightBoundary using the Sympson method.

    @param leftBoundary: the smaller x value.
    @param rightBoundary: the bigger x value.
    @param polynomial: the polynomial.
    @return:float, the integral of the polynomial between the range leftBoundary to rightBoundary
    """
    x = sp.symbols('x')
    f = sp.utilities.lambdify(x, polynomial)
    # divide the big range to a list of smaller ranges in order to minimize the error in the calculations
    mash = dividesection(leftBoundary, rightBoundary, numofsection)
    h = mash[0][1] - mash[0][0]
    size = len(mash)
    # calculate result
    result = h * f(leftBoundary)
    print(result)
    #  for every boundary in mash starting from the second boundary
    for index in range(1, size):
        # calculate h
        h = mash[index][1] - mash[index][0]
        if index % 2 == 1:
            result += 4 * h * f(mash[index][0])
        else:
            result += 2 * h * f(mash[index][0])
    result += h * f(rightBoundary)
    return 1.0 / 3.0 * result


def main():
    x = sp.symbols('x')
    # TODO: ↓ ENTER FUNCTION HERE ↓.
    f = sp.cos((2 * x ** 3) + (5 * x ** 2) - 6) / (2 * math.e ** (-2 * x))
    # get boundaries from user
    leftb = float(input("enter the left boundary: "))
    rightb = float(input("enter the right boundary: "))
    # calculate the number of sub- ranges to divide the big range into
    choice = ''
    while choice != -1:
        print("Press 1 to solve with Trapez Method.")
        print("Press 2 to solve with Sympson Method.")
        print("Press 3 to Exit.")
        choice = input("Enter number of method you want to solve with: ")
        if choice == '1':
            print("The Area Is: " + str(Trapezemethod(leftb, rightb, f)))
        elif choice == '2':
            print("The Area Is: " + str(callsympsonmethod(leftb, rightb, f)))
        elif choice == '3':
            break
        else:
            print("Wrong choice, try again.")
    print("GoodBye.")


main()
