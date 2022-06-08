def neville(datax, datay, x):
    """
    Finds an interpolated value using Neville's algorithm.
    Input
      datax: input x's in a list of size n
      datay: input y's in a list of size n
      x: the x value used for interpolation
    Output
      p[0]: the polynomial of degree n
    """
    n = len(datax)
    p = n*[0]
    for k in range(n):
        for i in range(n-k):
            if k == 0:
                p[i] = datay[i]
            else:
                p[i] = ((x-datax[i+k])*p[i]+ \
                        (datax[i]-x)*p[i+1])/ \
                        (datax[i]-datax[i+k])
                print('the',i,'iteration is:',p[i])
    return p[0]


xList = [1.2,1.3,1.4,1.5,1.6]
yList = [3.5095,3.6984,3.9043,4.1294,4.3756]
x = 1.37

print('f(',x,')=',neville(xList,yList,x))