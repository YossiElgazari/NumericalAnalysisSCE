import sympy as sp



def dividesection(leftbound, rightbound, numberofsections):
    dist = (rightbound - leftbound) / numberofsections
    sectionslist = []
    while (leftbound < rightbound):
        sectionslist.append([leftbound, leftbound + dist])
        leftbound = leftbound + dist
    return sectionslist


def Trapezemethod(leftboundary, rightboundary, function):
    x = sp.symbols('x')
    f = sp.utilities.lambdify(x, function)
    numofsection = 10
    section = dividesection(leftboundary, rightboundary, numofsection)
    i = 0
    oldintegral = 0
    while i < len(section):
        oldintegral = oldintegral + 0.5 * (section[i][1] - section[i][0]) * (f(section[i][0]) + f(section[i][1]))
        i += 1
    numofsection += 10
    section = dividesection(leftboundary, rightboundary, numofsection)
    i = 0
    newintegral = 0
    while i < len(section):
        newintegral = newintegral + 0.5 * (section[i][1] - section[i][0]) * (f(section[i][0]) + f(section[i][1]))
        i += 1
    while abs(newintegral - oldintegral) > 0.0000001:
        oldintegral = newintegral
        newintegral = 0
        numofsection += 10
        section = dividesection(leftboundary, rightboundary, numofsection)
        i = 0
        while i < len(section):
            newintegral = newintegral + 0.5 * (section[i][1] - section[i][0]) * (f(section[i][0]) + f(section[i][1]))
            i += 1
    return newintegral


def callsympsonmethod(leftboundary, rightboundary, function):
    numofsection = 10
    oldintegral = sympsonMethod(leftboundary, rightboundary, function, numofsection)
    numofsection += 10
    newintegral = sympsonMethod(leftboundary, rightboundary, function, numofsection)
    while abs(newintegral - oldintegral) > 0.0000001:
        oldintegral = newintegral
        newintegral = 0
        numofsection += 10
        newintegral = sympsonMethod(leftboundary, rightboundary, function, numofsection)
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


x = sp.symbols('x')
p = x ** 3 + sp.sin(x) + 5 * x ** 2 - sp.cos(x) ** 2
p = 2*x
a = 0.1
b = 0.2

print(Trapezemethod(a, b, p))
print(callsympsonmethod(a, b, p))
