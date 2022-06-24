import sympy as sy
from texttable import Texttable


class Robmerg:

    def __init__(self):
        self.x = sy.symbols("x")
        self.epsilon = 0.00001
        self.function = self.CreateFunction()
        self.boundary = self.CreateBoundary()

    def CreateFunction(self):  ## step 1 - choose a polynom
        ##fast example   x**4+x**3-3*x**2
        # funcInput = '(sin(x**2+5*x+6))/(2*E**-x)'
        # funcInput = '(x*E**(-x**2+5*x))*(2*x**2-3*x-5)'
        # TODO: INITIALIZE FUNCTION HERE
        funcInput = 'sin(x)'
        func = sy.sympify(funcInput)
        return func

    def CreateBoundary(self):  ## step 2 - choose an a and b
        # a = 0
        # b = 0
        # while a >= b:
        #     print("\nA Note: A < B")
        #     a = sy.sympify(input('please choose boundary A: '))
        #     b = sy.sympify(input('please choose boundary B: '))

        # return [0, 1]
        # initialize integral border
        # TODO: INITIALIZE BORDERS OF INTEGRAL HERE
        a = sy.sympify('0')
        b = sy.sympify('pi')
        return [a, b]

    def PrintRow(self, size, row, right):

        table = Texttable()
        table.set_precision(5)
        title = [[]]
        arr = [10 for i in range(size)]
        table.set_cols_width(arr)

        left = right
        for i in range(size):
            title[0].append(f'R({left},{right})')
            left += 1
        title.append(list(row))

        table.add_rows(title)
        print(table.draw())

    def ChooseN(self):

        return int(input('please choose the number of iterations: '))

    def RombergClac(self):

        ans = [[]]
        denum = 0
        N = self.ChooseN()
        hn = self.boundary[1] - self.boundary[0]
        cur = self.boundary[0]
        sum = 0
        j = 0
        for i in range(N):

            if denum != 0:
                devider = hn / denum

            while j < 2:
                sum += self.function.subs(self.x, self.boundary[j])
                j += 1
            j = 0
            if denum > 0:
                while cur < self.boundary[1] - devider:
                    cur += devider
                    sum += 2 * float(self.function.subs(self.x, cur))
                denum *= 2

            if denum == 0:
                denum = 2

            sum *= hn / denum
            ans[0].append(float(sum))
            sum = 0
            cur = self.boundary[0]

        myList = []
        denumArr = [3, 15]
        for i in range(10):
            a = denumArr[len(denumArr) - 1]
            b = denumArr[len(denumArr) - 2]

            x1 = a / 3
            y = b / 3

            z = x1 - y
            power = 0
            while z > 1:
                z /= 2
                power += 1
            power += 2

            nextNum = 3 * (2 ** power + x1)
            denumArr.append(nextNum)
        k = 0

        # calculate final answer
        for i in range(1, len(ans[0])):
            for j in range(0, len(ans[0]) - i):
                myList.append(ans[i - 1][j + 1] + (1 / denumArr[k]) * (ans[i - 1][j + 1] - ans[i - 1][j]))

            ans.append(myList)
            if len(ans[i]) == 1:
                break
            myList = []
            k += 1

        j = 1
        # print the answers in a table
        for i in range(len(ans), 0, -1):
            self.PrintRow(len(ans[j - 1]), ans[j - 1], j)
            j += 1

        print(f'\n(*) The Integral by Romberg is: {ans[len(ans) - 1][0]}')


myRomberg = Robmerg()
myRomberg.RombergClac()
