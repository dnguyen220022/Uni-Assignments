'''
FIT3139 Assignment 1

Name: Daniel Nguyen
Student Number: 32471033
Unit Code: FIT3139
Last Edit: 21/03 8:20PM

Notes:
some of the plotting functions are intensive, so run in debug mode and wait for func to resolve, this is for calculating nth derivates of 
trig funcs when n is very high.
'''

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

def taylorSeries(f, c, n):
    """_summary_
        Generate all taylor series terms for a given function (f), with a degree (n terms),
        centred at point x = c
        
    Args:
        f (_SymPy function_): original function
        c (_int / float_): centring point
        n (_int_): number of terms to compute
        
    Returns:
        taylorSeriesTerms (_arr_): array containing all terms of the taylor series computed
    """
    
    x = sp.Symbol('x')
    
    taylorSeriesPolynomial = 0
    
    '''
    Creation of each individual term in the taylor series, summing them as they are created
    '''
    for i in range(n + 1):
        factorial = sp.factorial(i)
        term = (f.subs(x, c) / factorial) * ((x - c) ** i)
        f = f.diff()
        taylorSeriesPolynomial += term
    
    return taylorSeriesPolynomial

def smallAngleRelError(xVals):
    """_summary_
        Calculate relative error for the small angle theorem for cos(x)

    Args:
        xVals (_NumPy Linspace_): range of x values to be subbed into our equation

    Returns:
        _y values_: the relative error at each x value, expressed as a percentage
    """
    x = sp.Symbol('x')
    cos = sp.cos(x)
    approx = 1 - ((x ** 2) / 2)
    
    relError = abs((cos - approx) / cos) * 100
    relErrorLambdify = sp.lambdify(x, relError, 'numpy')
    
    return relErrorLambdify(xVals)

def smallAngleBoundary(tolerance, xVals):
    """_summary_
        Finds the boundary for which the relative error for the small angle theorem for cos(x) is below the tolerance threshold
    Args:
        tolerance (_float/int_): tolerance for accuracy
        xVals (_NumPy Linspace_): _description_

    Returns:
        _float_: first x value in the linspace that is over the tolerance (i.e. every value under this in our Linspace satisifies our tolerance)
    """
    for x in xVals:
        error = smallAngleRelError(x)
        if error > tolerance:
            return x

def roundPi(sigFigs):
    """_summary_
        rounds pi to needed significant figures
    Args:
        sigFigs (_int_): number of significant figures to be rounded to

    Returns:
        _type_: pi rounded to sigFigs significant figures
    """
    return round(np.pi, sigFigs - 1)

def relForwardError1Term(x):
    """_summary_
        calculated relative forward error for Part 3
    Args:
        x (_float_): x value

    Returns:
        _type_: forward error of our function at that x value
    """
    cosval = np.cos(2 * np.pi * x)
    approxval = 1
    
    return abs((approxval - cosval) / cosval)

def relBackwardError1Term(xVals):
    """_summary_
        calculated relative backwards error for Part 3
    Args:
        xVals (_NumPy Linspace_): range of x values to be processed

    Returns:
        _type_: array of backwards error values for each index in the linspace input
    """
    backwardErrorVals = []
    for x in xVals:
        backwardErrorVals.append(abs((round(x, 0) - x) / x))
    return backwardErrorVals

def conditionNumber1Term(x):
    """_summary_
        calculates condition number for Part 3
    Args:
        x (_type_): x value

    Returns:
        _type_: condition number at x value
    """
    return relForwardError1Term(x) / relBackwardError1Term(x)

'''
Figure 1
'''
def plotFig1():
    x = sp.Symbol('x')

    cos = sp.cos(x)

    cosMaclaurinSeries = taylorSeries(cos, 0, 2)
    xVals = np.linspace(-1 * np.pi, np.pi, 1000)

    cosLambdify = sp.lambdify(x, cos, 'numpy')
    maclaurinLambdify = sp.lambdify(x, cosMaclaurinSeries, 'numpy')

    cosVals = cosLambdify(xVals)
    cosMacluarinVals = maclaurinLambdify(xVals)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (14, 6))
    ax1.plot(xVals, cosVals, label = 'cos(x)')
    ax1.plot(xVals, cosMacluarinVals, label = 'Maclaurin Series of cos(x) up to 2 terms')
    ax1.set_title('Plot of cos(x) against Maclaurin Series of cos(x) up to 2 terms')
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.legend()
    ax1.grid(True)
    ax1.set_ylim(-1.2, 1.2)
    
    ax2.plot(xVals, abs(cosVals - cosMacluarinVals))
    ax2.set_title('Absolute difference between cos(x) and Maclaurin Series')
    ax2.grid(True)
    
    plt.show()
    
'''
Figure 2
'''
def plotFig2():
    x = sp.Symbol('x')

    cos = sp.cos(x)

    cosMaclaurinSeries = taylorSeries(cos, 0, 4)
    xVals = np.linspace(-1 * np.pi, np.pi, 1000)

    cosLambdify = sp.lambdify(x, cos, 'numpy')
    maclaurinLambdify = sp.lambdify(x, cosMaclaurinSeries, 'numpy')

    cosVals = cosLambdify(xVals)
    cosMacluarinVals = maclaurinLambdify(xVals)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (14, 6))
    ax1.plot(xVals, cosVals, label = 'cos(x)')
    ax1.plot(xVals, cosMacluarinVals, label = 'Maclaurin Series of cos(x) up to 4 terms')
    ax1.set_title('Plot of cos(x) against Maclaurin Series of cos(x) up to 4 terms')
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.legend()
    ax1.grid(True)
    ax1.set_ylim(-1.2, 1.2)
    
    ax2.plot(xVals, abs(cosVals - cosMacluarinVals))
    ax2.set_title('Absolute difference between cos(x) and Maclaurin Series')
    ax2.grid(True)
    
    plt.show()

'''
Figure 3
'''    
def plotFig3():
    x = sp.Symbol('x')

    cos = sp.cos(x)

    plt.figure(figsize = (10, 6))
    
    for i in range(2, 9, 2):
        cosMaclaurinSeries = taylorSeries(cos, 0, i)
        xVals = np.linspace(-2 * np.pi, 2 * np.pi, 1000)

        cosLambdify = sp.lambdify(x, cos, 'numpy')
        maclaurinLambdify = sp.lambdify(x, cosMaclaurinSeries, 'numpy')

        cosVals = cosLambdify(xVals)
        cosMacluarinVals = maclaurinLambdify(xVals)
        
        plt.plot(xVals, abs(cosVals - cosMacluarinVals), label = f"absolute difference between cos(x) and the Maclaurin Series at {i} terms")
    
    plt.title("Absolute differences between cos(x) and the first 4 Maclaurin series of cos(x)")
    plt.xlabel('x')
    plt.ylabel('Absolute Difference')
    plt.legend()
    plt.grid()
    
    plt.show()

'''
Figure 4
'''
def plotFig4():
    x = sp.Symbol('x')

    cos = sp.cos(x)

    cosMaclaurinSeries = taylorSeries(cos, 0, 34)
    xVals = np.linspace(-5 * np.pi, 5 * np.pi, 1000)

    cosLambdify = sp.lambdify(x, cos, 'numpy')
    maclaurinLambdify = sp.lambdify(x, cosMaclaurinSeries, 'numpy')

    cosVals = cosLambdify(xVals)
    cosMacluarinVals = maclaurinLambdify(xVals)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (16, 8))
    ax1.plot(xVals, cosVals, label = 'cos(x)')
    ax1.plot(xVals, cosMacluarinVals, label = 'Maclaurin Series of cos(x) up to 34 terms')
    ax1.set_title('Plot of cos(x) against Maclaurin Series of cos(x) up to 34 terms')
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.legend()
    ax1.grid(True)
    ax1.set_ylim(-1.2, 1.2)

    ax2.plot(xVals, abs(cosVals - cosMacluarinVals))
    ax2.set_title('Absolute difference between cos(x) and Maclaurin Series')
    ax2.grid(True)
    
    plt.show()

'''
Figure 5
'''
def plotFig5():
    x = sp.Symbol('x')

    cos = sp.cos(x)

    cosTaylorSeries = taylorSeries(cos, np.pi/2, 1)
    xVals = np.linspace(0, np.pi, 1000)

    cosLambdify = sp.lambdify(x, cos, 'numpy')
    taylorLambdify = sp.lambdify(x, cosTaylorSeries, 'numpy')

    cosVals = cosLambdify(xVals)
    cosTaylorVals = taylorLambdify(xVals)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (14, 6))
    ax1.plot(xVals, cosVals, label = 'cos(x)')
    ax1.plot(xVals,  cosTaylorVals, label = 'Taylor Series of cos(x) up to 1 term')
    ax1.set_title('Plot of cos(x) against Taylor Series of cos(x) up to 1 term centred at x = pi/2')
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.legend()
    ax1.grid(True)
    
    ax2.plot(xVals, abs(cosVals - cosTaylorVals))
    ax2.set_title('Absolute difference between cos(x) and Taylor Series')
    ax2.grid(True)
    
    plt.show()
    
'''
Figure 6
'''
def plotFig6():
    x = sp.Symbol('x')

    cos = sp.cos(x)

    cosTaylorSeries = taylorSeries(cos, np.pi/2, 22)
    xVals = np.linspace(-2.5 * np.pi, 3.5 * np.pi, 1000)

    cosLambdify = sp.lambdify(x, cos, 'numpy')
    taylorLambdify = sp.lambdify(x, cosTaylorSeries, 'numpy')

    cosVals = cosLambdify(xVals)
    cosTaylorVals = taylorLambdify(xVals)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (16, 8))
    ax1.plot(xVals, cosVals, label = 'cos(x)')
    ax1.plot(xVals,  cosTaylorVals, label = 'Taylor Series of cos(x) up to 1 term')
    ax1.set_title('Plot of cos(x) against Taylor Series of cos(x) up to 1 term centred at x = pi/2')
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.legend()
    ax1.grid(True)
    ax1.set_ylim(-1.2, 1.2)
    
    ax2.plot(xVals, abs(cosVals - cosTaylorVals))
    ax2.set_title('Absolute difference between cos(x) and Taylor Series')
    ax2.grid(True)
    
    plt.show()

'''
Figure 7
'''
def plotFig7():
    x = sp.Symbol('x')

    cos = sp.cos(x)

    plt.figure(figsize = (10, 6))
    
    for i in range(1, 8, 2):
        cosMaclaurinSeries = taylorSeries(cos, np.pi/2, i)
        xVals = np.linspace(-1 * np.pi, 2 * np.pi, 1000)

        cosLambdify = sp.lambdify(x, cos, 'numpy')
        maclaurinLambdify = sp.lambdify(x, cosMaclaurinSeries, 'numpy')

        cosVals = cosLambdify(xVals)
        cosMacluarinVals = maclaurinLambdify(xVals)
        
        plt.plot(xVals, abs(cosVals - cosMacluarinVals), label = f"absolute difference between cos(x) and the Taylor Series at {i} terms")
    
    plt.title("Absolute differences between cos(x) and the first 4 Taylor Series of cos(x) centred at x = pi/2")
    plt.xlabel('x')
    plt.ylabel('Absolute Difference')
    plt.legend()
    plt.grid()
    
    plt.show()

'''
Figure 8
'''
def plotFig8():
    x = sp.Symbol('x')
    xVals = np.linspace(0, 0.3, 1000)
    
    plt.plot(xVals, smallAngleRelError(xVals))
    plt.ylim(0, 0.1)
    plt.title("Relative error of the small angle theorem for cos(x)")
    plt.xlabel('x')
    plt.ylabel('Relative Error %')
    plt.show()

'''
Figure 9
'''
def plotFig9():
    xVals = np.linspace(0, 0.3, 1000)
    maxXVal = smallAngleBoundary(0.01, xVals)
    
    plt.plot(xVals, smallAngleRelError(xVals), label = 'relative error')
    plt.axvline(x = maxXVal, label = f'approximate maximum x value ({round(maxXVal, 4)})', color = 'red')
    plt.axhline(y = 0.01, label = '0.01% tolerance', color = 'red')
    plt.ylim(0, 0.05)
    plt.title("Relative error of the small angle theorem for cos(x)")
    plt.xlabel('x')
    plt.ylabel('Relative Error %')
    plt.legend()
    plt.show()
    
    plt.show()

'''
Figure 10
'''
def plotFig10():
    x = sp.Symbol('x')

    tan = sp.tan(x)

    tanMaclaurinSeries = taylorSeries(tan, 0, 3)
    xVals = np.linspace(-2 * np.pi, 2 * np.pi, 1000)

    tanLambdify = sp.lambdify(x, tan, 'numpy')
    maclaurinLambdify = sp.lambdify(x, tanMaclaurinSeries, 'numpy')

    tanVals = tanLambdify(xVals)
    tanMacluarinVals = maclaurinLambdify(xVals)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (16, 8))
    ax1.plot(xVals, tanVals, label = 'tan(x)')
    ax1.plot(xVals, tanMacluarinVals, label = 'Maclaurin Series of tan(x) up to 3 terms')
    ax1.set_title('Plot of cos(x) against Maclaurin Series of tan(x) up to 3 terms')
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.legend()
    ax1.grid(True)
    ax1.set_ylim(-15, 15)

    ax2.plot(xVals, abs(tanVals - tanMacluarinVals))
    ax2.set_title('Absolute difference between tan(x) and Maclaurin Series')
    ax2.set_ylim(0, 100)
    
    plt.show()

'''
Figure 11
''' 
def plotFig11():
    x = sp.Symbol('x')

    tan = sp.tan(x)

    tanMaclaurinSeries = taylorSeries(tan, 0, 15)
    xVals = np.linspace(-2 * np.pi, 2 * np.pi, 1000)

    tanLambdify = sp.lambdify(x, tan, 'numpy')
    maclaurinLambdify = sp.lambdify(x, tanMaclaurinSeries, 'numpy')

    tanVals = tanLambdify(xVals)
    tanMacluarinVals = maclaurinLambdify(xVals)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (16, 8))
    ax1.plot(xVals, tanVals, label = 'tan(x)')
    ax1.plot(xVals, tanMacluarinVals, label = 'Maclaurin Series of tan(x) up to 15 terms')
    ax1.set_title('Plot of cos(x) against Maclaurin Series of tan(x) up to 15 terms')
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.legend()
    ax1.grid(True)
    ax1.set_ylim(-15, 15)

    ax2.plot(xVals, abs(tanVals - tanMacluarinVals))
    ax2.set_title('Absolute difference between tan(x) and Maclaurin Series')
    ax2.set_ylim(0, 100)
    
    plt.show()

'''
Figure 12
'''
def plotFig12():
    x = sp.Symbol('x')

    tan = sp.tan(x)

    tanMaclaurinSeries = taylorSeries(tan, np.pi / 4, 5)
    xVals = np.linspace(-2 * np.pi, 2 * np.pi, 1000)

    tanLambdify = sp.lambdify(x, tan, 'numpy')
    maclaurinLambdify = sp.lambdify(x, tanMaclaurinSeries, 'numpy')

    tanVals = tanLambdify(xVals)
    tanMacluarinVals = maclaurinLambdify(xVals)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (16, 8))
    ax1.plot(xVals, tanVals, label = 'tan(x)')
    ax1.plot(xVals, tanMacluarinVals, label = 'Taylor Series of tan(x) up to 5 terms centred at pi/4')
    ax1.set_title('Plot of cos(x) against Taylor Series of tan(x) up to 5 terms')
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.legend()
    ax1.grid(True)
    ax1.set_ylim(-15, 15)

    ax2.plot(xVals, abs(tanVals - tanMacluarinVals))
    ax2.set_title('Absolute difference between tan(x) and Taylor Series')
    ax2.set_ylim(0, 100)
    ax2.set_xlabel('x')
    ax2.set_ylabel('Absolute Difference')
    
    plt.show()

'''
Figure 13
'''    
def plotFig13():
    x = sp.Symbol('x')

    tan = sp.tan(x)

    tanMaclaurinSeries = taylorSeries(tan, np.pi / 4, 15)
    xVals = np.linspace(-2 * np.pi, 2 * np.pi, 1000)

    tanLambdify = sp.lambdify(x, tan, 'numpy')
    maclaurinLambdify = sp.lambdify(x, tanMaclaurinSeries, 'numpy')

    tanVals = tanLambdify(xVals)
    tanMacluarinVals = maclaurinLambdify(xVals)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (16, 8))
    ax1.plot(xVals, tanVals, label = 'tan(x)')
    ax1.plot(xVals, tanMacluarinVals, label = 'Taylor Series of tan(x) up to 15 terms centred at pi/4')
    ax1.set_title('Plot of cos(x) against Taylor Series of tan(x) up to 15 terms')
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.legend()
    ax1.grid(True)
    ax1.set_ylim(-15, 15)

    ax2.plot(xVals, abs(tanVals - tanMacluarinVals))
    ax2.set_title('Absolute difference between tan(x) and Taylor Series')
    ax2.set_ylim(0, 100)
    ax2.set_xlabel('x')
    ax2.set_ylabel('Absolute Difference')
    
    plt.show()

'''
Figure 14
'''
def plotFig14():
    xVals = np.linspace(-1/2 * np.pi, 1/2 * np.pi, 1000)
    
    x = sp.Symbol('x')
    
    func = sp.cos(2 * np.pi * x)
    roundedFunc = sp.cos(2 * roundPi(2) * x)
    
    funcLamdify = sp.lambdify(x, func, 'numpy')
    roundedFuncLamdify = sp.lambdify(x, roundedFunc, 'numpy')
    
    plt.figure(figsize = (12, 6))
    plt.plot(xVals, funcLamdify(xVals), label = 'cos(2 * pi * x)')
    plt.plot(xVals, roundedFuncLamdify(xVals), label = 'cos(2 * pi * x) with pi rounded to 2 significant figures')
    plt.title("cos(2*pi*x) against against cos(2*pi*x) with pi rounded to 2 significant figures")
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend(loc = 1)
    plt.grid()
    plt.show()

'''
Figure 15
'''
def plotFig15():
    xVals = np.linspace(-1/2 * np.pi, 1/2 * np.pi, 1000)
    
    x = sp.Symbol('x')
    
    func = sp.cos(2 * np.pi * x)
    roundedFunc = sp.cos(2 * roundPi(1) * x)
    
    funcLamdify = sp.lambdify(x, func, 'numpy')
    roundedFuncLamdify = sp.lambdify(x, roundedFunc, 'numpy')
    
    plt.figure(figsize = (12, 6))
    plt.plot(xVals, funcLamdify(xVals), label = 'cos(2 * pi * x)')
    plt.plot(xVals, roundedFuncLamdify(xVals), label = 'cos(2 * pi * x) with pi rounded to 1 significant figure')
    plt.title("cos(2*pi*x) against against cos(2*pi*x) with pi rounded to 1 significant figure")
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend(loc = 1)
    plt.grid()
    plt.show()

'''
Figure 16
'''
def plotFig16():
    xVals = np.linspace(-2 * np.pi, 2 * np.pi, 1000)
    
    x = sp.Symbol('x')
    
    func = sp.cos(2 * np.pi * x)
    roundedFunc = sp.cos(2 * roundPi(2) * x)
    
    absError = func - roundedFunc
    
    absErrorLambd = sp.lambdify(x, absError, 'numpy')
    
    plt.figure(figsize = (12, 6))
    plt.plot(xVals, abs(absErrorLambd(xVals)))
    plt.title("Absolute difference between cos(2*pi*x) and cos(2*pi*x) when pi is rounded to 2 significant figures")
    plt.xlabel('x')
    plt.ylabel('Absolute Difference')
    plt.grid()
    plt.show()

'''
Figure 17
'''
def plotFig17():
    xVals = np.linspace(-30 * np.pi, 30 * np.pi, 1000)
    
    x = sp.Symbol('x')
    
    func = sp.cos(2 * np.pi * x)
    roundedFunc = sp.cos(2 * roundPi(2) * x)
    
    absError = func - roundedFunc
    
    absErrorLambd = sp.lambdify(x, absError, 'numpy')
    
    plt.figure(figsize = (12, 6))
    plt.plot(xVals, abs(absErrorLambd(xVals)))
    plt.title("Absolute difference between cos(2*pi*x) and cos(2*pi*x) when pi is rounded to 2 significant figures")
    plt.xlabel('x')
    plt.ylabel('Absolute Difference')
    plt.grid()
    plt.show()

'''
Figure 18
'''  
def plotFig18():
    #xVals = np.linspace(-1/2 * np.pi, 1/2 * np.pi, 1000)
    xVals = np.linspace(0.4999, 0.5001, 1000)
    
    x = sp.Symbol('x')
    
    func = sp.cos(2 * np.pi * x)
    roundedFunc = sp.cos(2 * roundPi(5) * x)
    
    funcLamdify = sp.lambdify(x, func, 'numpy')
    roundedFuncLamdify = sp.lambdify(x, roundedFunc, 'numpy')
    
    plt.figure(figsize = (12, 6))
    plt.plot(xVals, funcLamdify(xVals), label = 'cos(2 * pi * x)')
    plt.plot(xVals, roundedFuncLamdify(xVals), label = 'cos(2 * pi * x) with pi rounded to 5 significant figures')
    plt.title("cos(2*pi*x) against against cos(2*pi*x) with pi rounded to 5 significant figures")
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend(loc = 1)
    plt.grid()
    plt.show()

'''
Figure 19
'''
def plotFig19():
    xVals = np.linspace(-2, 2, 5000)
    
    x = sp.Symbol('x')

    plt.figure(figsize = (12, 6))
    plt.plot(xVals, conditionNumber1Term(xVals))
    plt.title("Condition Number for values of x")
    plt.xlabel('x')
    plt.ylabel('Condition Number')
    plt.grid()
    plt.ylim(0, 200)
    plt.show()

'''
Figure 20
'''
def plotFig20():
    xVals = np.linspace(-2, 2, 5000)
    
    x = sp.Symbol('x')
    
    f = sp.cos(2 * np.pi * x)
    fprime = f.diff(x)
    condNumber = (x * fprime) / f
    
    condNumberLambdify = sp.lambdify(x, condNumber, 'numpy')
    
    plt.figure(figsize = (12, 6))
    plt.plot(xVals, abs(condNumberLambdify(xVals)))
    plt.title("Approximated Condition Number for cos(2 * pi * x)")
    plt.xlabel('x')
    plt.ylabel('approximate condition number')
    plt.grid()
    plt.ylim(0, 200)
    plt.show()

### REMOVE COMMENT TO PLOT FIGURE ###   
# plotFig1()
plotFig2()
# plotFig3()
# plotFig4()
# plotFig5()
# plotFig6()
# plotFig7()
# plotFig8()
# plotFig9()
# plotFig10()
# plotFig11()
# plotFig12()
# plotFig13()
# plotFig14()
# plotFig15()
# plotFig16()
# plotFig17()
# plotFig18()
# plotFig19()
# plotFig20()