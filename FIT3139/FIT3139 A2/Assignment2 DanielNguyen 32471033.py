'''
FIT3139 Assignment 2

Name: Daniel Nguyen
Student Number: 32471033
Unit Code: FIT3139
Last Edit: 30/04 8:20PM
'''

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from scipy.integrate import odeint

#define our models
#the following functions are used to define our difference equations
def speciesXDiscrete(popX, popY, popZ, r, theta, a, deltaT):
    newPopX = popX + deltaT * (r * popX - theta * popX * popY - a * popX * popZ)
    return newPopX

def speciesYDiscrete(popX, popY, popZ, s, beta, phi, deltaT):
    newPopY = popY + deltaT * (s * popY - beta * popY * popZ + phi * popY * popX)
    return newPopY

def speciesZDiscrete(popX, popY, popZ, m, lambdaSymbol, rho, deltaT):
    newPopZ = popZ + deltaT * (m * popZ + lambdaSymbol * popZ * popY + rho * popZ * popX)
    return newPopZ

#model our difference equations
def modelDiscrete(timeVals, xInitial, yInitial, zInitial, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, deltaT):
    """_summary_
        Generate all model values for our difference equations based on initial variables
        
    Args:
        timeVals = numpy array of time values for plotting
        the rest = inital values and coefficients
        
    Returns:
        tuple of arrays of species pop levels at each time value
    """
    xPop = [xInitial]
    yPop = [yInitial]
    zPop = [zInitial]
    
    for timeVal in timeVals:
        if timeVal == 0:
            pass
        else:
            newXPop = speciesXDiscrete(xPop[-1], yPop[-1], zPop[-1], r, theta, a, deltaT)
            newYPop = speciesYDiscrete(xPop[-1], yPop[-1], zPop[-1], s, beta, phi, deltaT)
            newZPop = speciesZDiscrete(xPop[-1], yPop[-1], zPop[-1], m, lambdaSymbol, rho, deltaT)
            
            xPop.append(max(0, newXPop))
            yPop.append(max(0, newYPop))
            zPop.append(max(0, newZPop))
            
    return (xPop, yPop, zPop)

#define continuous model
def contModel(P, t, r, theta, a, s, beta, phi, m, lambdaSymbol, rho):
    """_summary_
        define ODEs
        
    Args:
        P0 = array of initial populations
        t = variable used for odeint, not used for RK2
        the rest = func coefficients
        
    Returns:
        numpy array of evaluated rate of change of func for each variable
    """
    dxdt = r * P[0] - theta * P[0] * P[1] - a * P[0] * P[2]
    dydt = s * P[1] - beta * P[1] * P[2] + phi * P[1] * P[0]
    dzdt = m * P[2] + lambdaSymbol * P[2] * P[1] + rho * P[2] * P[0]
    
    return np.array([dxdt, dydt, dzdt])

#scipy odeint for modelling
def odeintModel(xInitial, yInitial, zInitial, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, timeVals):
    """_summary_
        odeint method for solving ODEs
        
    Args:
        Initial pops
        func coefficients
        numpy array of time values
        
    Returns:
        numpy array of evaluated population levels for each variable
    """
    P0 = np.array([xInitial, yInitial, zInitial])
    P = odeint(contModel, P0, timeVals, args = (r, theta, a, s, beta, phi, m, lambdaSymbol, rho,))
    x, y, z = P.T
    
    return x, y, z

#general rk2 implementation for modelling
#RK2a arg defines method used (e.g. use RK2a = 1/2 for Heuns method)
def RK2(P0, maxTime, numSteps, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, RK2a):
    """_summary_
        heuns method for solving odes
        
    Args:
        P0 = np array of initial pops
        maxTime = upper bound of time for model
        numSteps = number of points where pop is measured
        func coefficients
        RK2a = weighting of first slope
        
    Returns:
        numpy array of evaluated population levels for each variable
    """
    RK2b = 1 - RK2a
    RK2alpha = 1 / (2 * RK2b)
    RK2beta = 1 / (2 * RK2b)
    h = maxTime / numSteps
    
    timeVals = np.linspace(0, maxTime, num = numSteps + 1)
    
    P = np.zeros((numSteps + 1, 3))
    P[0] = P0
    
    for i in range(numSteps):
        k1 = contModel(P[i], None, r, theta, a, s, beta, phi, m, lambdaSymbol, rho)
        k2 = contModel(P[i] + RK2beta * h * k1, None, r, theta, a, s, beta, phi, m, lambdaSymbol, rho)
        newP = P[i] + h * (RK2a * k1 + RK2b * k2)
        P[i + 1] = newP
    
    return timeVals, P

#figure 1
def plotFig1():
    timeVals = np.linspace(0, 25, num = 25)

    xInitial = 10
    r = 0.01
    theta = 0.01
    a = 0.01
    
    yInitial = 10
    s = 0.01
    beta = 0.01
    phi = 0.01
    
    zInitial = 10
    m = 0.01
    lambdaSymbol = 0.01
    rho = 0.01
    
    deltaT = 1
    
    popVals = modelDiscrete(timeVals, xInitial, yInitial, zInitial, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, deltaT)
    xPop = np.array(popVals[0])
    yPop = np.array(popVals[1])
    zPop = np.array(popVals[2])

    plt.plot(timeVals, xPop, label = "Species X (Flies)")
    plt.plot(timeVals, yPop, label = "Species Y (Spiders)")
    plt.plot(timeVals, zPop, label = "Species Z (Frogs)")
    plt.legend()
    plt.title("Species Population Levels Over 25 Time Periods")
    plt.ylabel("Population")
    plt.xlabel("Time Period")
    plt.ylim(0, 25)
    plt.show()
    
#figure 2
def plotFig2():
    timeVals = np.linspace(0, 2000, num = 2000)

    xInitial = 10
    r = 0.01
    theta = 0.01
    a = 0.01
    
    yInitial = 10
    s = 0.01
    beta = 0.01
    phi = 0.01
    
    zInitial = 10
    m = -0.2
    lambdaSymbol = 0.01
    rho = 0.01
    
    deltaT = 1
    
    popVals = modelDiscrete(timeVals, xInitial, yInitial, zInitial, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, deltaT)
    xPop = np.array(popVals[0])
    yPop = np.array(popVals[1])
    zPop = np.array(popVals[2])

    plt.plot(timeVals, xPop, label = "Species X (Flies)")
    plt.plot(timeVals, yPop, label = "Species Y (Spiders)")
    plt.plot(timeVals, zPop, label = "Species Z (Frogs)")
    plt.legend()
    plt.title("Species Population Levels Over 2000 Time Periods")
    plt.ylabel("Population")
    plt.xlabel("Time Period")
    plt.ylim(0, 150)
    plt.show()

#Figure 3
def plotFig3():
    timeVals = np.linspace(0, 3500, num = 3500)

    xInitial = 10
    r = 0.5
    theta = 0.045
    a = 0.001
    
    yInitial = 3
    s = -0.3
    beta = 0.01
    phi = 0.03
    
    zInitial = 1
    m = -0.1
    lambdaSymbol = 0.01
    rho = 0.001
    
    deltaT = 0.1
    
    popVals = modelDiscrete(timeVals, xInitial, yInitial, zInitial, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, deltaT)
    xPop = np.array(popVals[0])
    yPop = np.array(popVals[1])
    zPop = np.array(popVals[2])

    plt.plot(timeVals, xPop, label = "Species X (Flies)")
    plt.plot(timeVals, yPop, label = "Species Y (Spiders)")
    plt.plot(timeVals, zPop, label = "Species Z (Frogs)")
    plt.legend()
    plt.title("Species Population Levels Over 3500 Time Periods")
    plt.ylabel("Population")
    plt.xlabel("Time Period")
    plt.ylim(0, 200)
    plt.show()

#Figure 4
def plotFig4():
    timeVals = np.linspace(0, 350000, num = 350000)

    xInitial = 10
    r = 0.5
    theta = 0.045
    a = 0.001
    
    yInitial = 3
    s = -0.3
    beta = 0.01
    phi = 0.03
    
    zInitial = 1
    m = -0.1
    lambdaSymbol = 0.01
    rho = 0.001
    
    deltaT = 0.001
    
    popVals = modelDiscrete(timeVals, xInitial, yInitial, zInitial, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, deltaT)
    xPop = np.array(popVals[0])
    yPop = np.array(popVals[1])
    zPop = np.array(popVals[2])

    plt.plot(timeVals, xPop, label = "Species X (Flies)")
    plt.plot(timeVals, yPop, label = "Species Y (Spiders)")
    plt.plot(timeVals, zPop, label = "Species Z (Frogs)")
    plt.legend()
    plt.title("Species Population Levels Over 350000 Time Periods")
    plt.ylabel("Population")
    plt.xlabel("Time Period")
    plt.ylim(0, 600)
    plt.show()

#Figure 5  
def plotFig5():

    xInitial = 10
    r = 0.01
    theta = 0.01
    a = 0.01
    
    yInitial = 10
    s = 0.01
    beta = 0.01
    phi = 0.01
    
    zInitial = 10
    m = 0.01
    lambdaSymbol = 0.01
    rho = 0.01
    
    P0 = [xInitial, yInitial, zInitial]
    maxTime = 50
    numSteps = 1000
    RK2a = 1 / 2
    
    timeVals, P = RK2(P0, maxTime, numSteps, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, RK2a)
    
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.plot(timeVals, P)
    ax1.set_title("Species Population Levels Over Time (RK2)")
    ax1.set_ylabel("Population")
    ax1.set_xlabel("Time")
    ax1.set_ylim(0, 60)
    
    x, y, z = odeintModel(xInitial, yInitial, zInitial, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, timeVals)
    ax2.plot(timeVals, x, label = 'Flies')
    ax2.plot(timeVals, y, label = 'Spiders')
    ax2.plot(timeVals, z, label = 'Frogs')
    ax2.legend()
    ax2.set_title("Species Population Levels Over Time (OdeInt)")
    ax2.set_ylabel("Population")
    ax2.set_xlabel("Time")
    ax2.set_ylim(0, 60)

    plt.show()
    
#Figure 6  
def plotFig6():

    xInitial = 10
    r = 0.01
    theta = 0.01
    a = 0.01
    
    yInitial = 10
    s = 0.01
    beta = 0.01
    phi = 0.01
    
    zInitial = 10
    m = -0.2
    lambdaSymbol = 0.01
    rho = 0.01
    
    P0 = [xInitial, yInitial, zInitial]
    maxTime = 500
    numSteps = 50000
    RK2a = 1 / 2
    
    timeVals, P = RK2(P0, maxTime, numSteps, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, RK2a)
    
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.plot(timeVals, P)
    ax1.set_title("Species Population Levels Over Time (RK2)")
    ax1.set_ylabel("Population")
    ax1.set_xlabel("Time")
    ax1.set_ylim(0, 60)
    
    x, y, z = odeintModel(xInitial, yInitial, zInitial, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, timeVals)
    ax2.plot(timeVals, x, label = 'Flies')
    ax2.plot(timeVals, y, label = 'Spiders')
    ax2.plot(timeVals, z, label = 'Frogs')
    ax2.legend()
    ax2.set_title("Species Population Levels Over Time (OdeInt)")
    ax2.set_ylabel("Population")
    ax2.set_xlabel("Time")
    ax2.set_ylim(0, 60)

    plt.show()

#Figure 7  
def plotFig7():

    xInitial = 10
    r = 0.5
    theta = 0.045
    a = 0.001
    
    yInitial = 3
    s = -0.3
    beta = 0.01
    phi = 0.03
    
    zInitial = 1
    m = -0.1
    lambdaSymbol = 0.01
    rho = 0.001
    
    P0 = [xInitial, yInitial, zInitial]
    maxTime = 350
    numSteps = 350000
    RK2a = 1 / 2
    
    timeVals, P = RK2(P0, maxTime, numSteps, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, RK2a)
    
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.plot(timeVals, P)
    ax1.set_title("Species Population Levels Over Time (RK2)")
    ax1.set_ylabel("Population")
    ax1.set_xlabel("Time")
    ax1.set_ylim(0, 600)
    
    x, y, z = odeintModel(xInitial, yInitial, zInitial, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, timeVals)
    ax2.plot(timeVals, x, label = 'Flies')
    ax2.plot(timeVals, y, label = 'Spiders')
    ax2.plot(timeVals, z, label = 'Frogs')
    ax2.legend()
    ax2.set_title("Species Population Levels Over Time (OdeInt)")
    ax2.set_ylabel("Population")
    ax2.set_xlabel("Time")
    ax2.set_ylim(0, 600)

    plt.show()
    
#Figure 8  
def plotFig8():

    xInitial = 7.964601769911503
    r = 0.5
    theta = 0.045
    a = 0.001
    
    yInitial = 2.920353982300884
    s = 0.5
    beta = 0.01
    phi = 0.4
    
    zInitial = 368.58407079646025
    m = -0.3
    lambdaSymbol = 0.1
    rho = 0.001
    
    P0 = [xInitial, yInitial, zInitial]
    maxTime = 1000
    numSteps = 100000
    RK2a = 1 / 2
    
    timeVals, P = RK2(P0, maxTime, numSteps, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, RK2a)
    
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.plot(timeVals, P)
    ax1.set_title("Species Population Levels Over Time (RK2)")
    ax1.set_ylabel("Population")
    ax1.set_xlabel("Time")
    ax1.set_ylim(0, 600)
    
    x, y, z = odeintModel(xInitial, yInitial, zInitial, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, timeVals)
    ax2.plot(timeVals, x, label = 'Flies')
    ax2.plot(timeVals, y, label = 'Spiders')
    ax2.plot(timeVals, z, label = 'Frogs')
    ax2.legend()
    ax2.set_title("Species Population Levels Over Time (OdeInt)")
    ax2.set_ylabel("Population")
    ax2.set_xlabel("Time")
    ax2.set_ylim(0, 600)

    plt.show()

#Figure 9  
def plotFig9():

    xInitial = 8
    r = 0.5
    theta = 0.045
    a = 0.001
    
    yInitial = 3
    s = 0.5
    beta = 0.01
    phi = 0.4
    
    zInitial = 369
    m = -0.3
    lambdaSymbol = 0.1
    rho = 0.001
    
    P0 = [xInitial, yInitial, zInitial]
    maxTime = 250
    numSteps = 250000
    RK2a = 1 / 2
    
    timeVals, P = RK2(P0, maxTime, numSteps, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, RK2a)
    
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.plot(timeVals, P)
    ax1.set_title("Species Population Levels Over Time (RK2)")
    ax1.set_ylabel("Population")
    ax1.set_xlabel("Time")
    ax1.set_ylim(0, 500)
    
    x, y, z = odeintModel(xInitial, yInitial, zInitial, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, timeVals)
    ax2.plot(timeVals, x, label = 'Flies')
    ax2.plot(timeVals, y, label = 'Spiders')
    ax2.plot(timeVals, z, label = 'Frogs')
    ax2.legend()
    ax2.set_title("Species Population Levels Over Time (OdeInt)")
    ax2.set_ylabel("Population")
    ax2.set_xlabel("Time")
    ax2.set_ylim(0, 500)

    plt.show()

########################
# Uncomment to plot figs
########################

#plotFig1()
#plotFig2()
#plotFig3()
#plotFig4()
#plotFig5()
#plotFig6()
#plotFig7()
#plotFig8()  
#plotFig9()

############################
# STEADY STATE ANALYSIS
############################

#getting steady states
def getSteadyStates():
    x, y, z = sp.symbols('x y z')
    r, theta, a, s, beta, phi, m, lambdaSymbol, rho = sp.symbols('r theta a s beta phi m lambdaSymbol rho')
    
    dxdt = r * x - theta * x * y - a * x * z
    dydt = s * y - beta * y * z + phi * y * x
    dzdt = m * z + lambdaSymbol * z * y + rho * z * x
    
    steadyStates = sp.solve([dxdt, dydt, dzdt], (x, y, z))
    
    return steadyStates

#trial and error steady state value testing
def testSteadyStates():

    r = 0.5
    theta = 0.045
    a = 0.001
    
    s = 0.5
    beta = 0.01
    phi = 0.4

    m = -0.3
    lambdaSymbol = 0.1
    rho = 0.001

    x = (-a*lambdaSymbol*s + beta*lambdaSymbol*r + beta*m*theta)/(a*lambdaSymbol*phi - beta*rho*theta) 
    y = -(a*m*phi - a*rho*s + beta*r*rho)/(a*lambdaSymbol*phi - beta*rho*theta)
    z = (lambdaSymbol*phi*r + m*phi*theta - rho*s*theta)/(a*lambdaSymbol*phi - beta*rho*theta)
    
    print((x, y, z))
    
##################
#uncomment to use
##################

#print(getSteadyStates())   
#testSteadyStates()

#Figure 10 (Discrete Steady State)
def plotFig10():
    timeVals = np.linspace(0, 800, num = 800)

    xInitial = 7.964601769911503
    r = 0.5
    theta = 0.045
    a = 0.001
    
    yInitial = 2.920353982300884
    s = 0.5
    beta = 0.01
    phi = 0.4
        
    zInitial = 368.58407079646025
    m = -0.3
    lambdaSymbol = 0.1
    rho = 0.001
    
    deltaT = 0.1
    
    popVals = modelDiscrete(timeVals, xInitial, yInitial, zInitial, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, deltaT)
    xPop = np.array(popVals[0])
    yPop = np.array(popVals[1])
    zPop = np.array(popVals[2])

    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.plot(timeVals, xPop, label = "Species X (Flies)")
    ax1.plot(timeVals, yPop, label = "Species Y (Spiders)")
    ax1.plot(timeVals, zPop, label = "Species Z (Frogs)")
    ax1.set_title("Species Population With Exact Steady State Initial Conditions")
    ax1.set_ylabel("Population")
    ax1.set_xlabel("Time Period")
    ax1.set_ylim(0, 600)
    
    xInitial = 8
    yInitial = 3
    zInitial = 369

    popVals = modelDiscrete(timeVals, xInitial, yInitial, zInitial, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, deltaT)
    xPop = np.array(popVals[0])
    yPop = np.array(popVals[1])
    zPop = np.array(popVals[2])

    ax2.plot(timeVals, xPop, label = "Species X (Flies)")
    ax2.plot(timeVals, yPop, label = "Species Y (Spiders)")
    ax2.plot(timeVals, zPop, label = "Species Z (Frogs)")
    ax2.legend()
    ax2.set_title("Species Population Levels With Steady State Initial Population Rounded to Whole Number")
    ax2.set_ylabel("Population")
    ax2.set_xlabel("Time Period")
    ax2.set_ylim(0, 600)
    
    plt.show()

############################
#uncomment to plot figure 10
############################

#plotFig10()

############################
# Phase Plane Analysis
############################

#plot phase plane for Steady State 2
def plotFig11():
    r = 0
    theta = 0
    a = 0
    
    s = 0.5
    beta = 0.1
    phi = 0
    
    m = -0.3
    lambdaSymbol = 0.1
    rho = 0
    
    maxTime = 250
    numSteps = 250000
    RK2a = 1 / 2
    
    P0 = [0, 5, 6]
    timeVals, P = RK2(P0, maxTime, numSteps, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, RK2a)
    x = P[:, 0]
    y = P[:, 1]
    z = P[:, 2]
    plt.plot(y, z, label = "P* = 0, 5, 6")
    
    P0 = [0, 8, 7]
    timeVals, P = RK2(P0, maxTime, numSteps, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, RK2a)
    x = P[:, 0]
    y = P[:, 1]
    z = P[:, 2]
    plt.plot(y, z, label = "P* = 0, 8, 7")
    
    P0 = [0, 15, 11]
    timeVals, P = RK2(P0, maxTime, numSteps, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, RK2a)
    x = P[:, 0]
    y = P[:, 1]
    z = P[:, 2]
    plt.plot(y, z, label = "P* = 0, 11, 13")
    
    P0 = [0, 23, 17]
    timeVals, P = RK2(P0, maxTime, numSteps, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, RK2a)
    x = P[:, 0]
    y = P[:, 1]
    z = P[:, 2]
    plt.plot(y, z, label = "P* = 0, 15, 11")

    #create arrow grid
    xAxis = np.linspace(0, 30, 10)
    yAxis = np.linspace(0, 35, 10)
    
    for yVal in xAxis:
        for zVal in yAxis:
            P = [0, yVal, zVal]
            dxdt, dydt, dzdt = contModel(P, None, r, theta, a, s, beta, phi, m, lambdaSymbol, rho)
            plt.quiver(yVal, zVal, dydt, dzdt, color = 'blue', alpha = 0.5)
    
    #plot steady state lines
    ySteadyState = -m / lambdaSymbol
    zSteadyState = s / beta
    
    plt.axhline(y = zSteadyState, linestyle = '--', label = 'Frog Steady State Population')
    plt.axvline(x = ySteadyState, color = 'red', linestyle = '--', label = 'Spider Steady State Population')
    
    plt.title("Phase Plane Diagram Centered around Steady State 1")
    plt.ylabel("Population (Frogs)")
    plt.xlabel("Population (Spiders)")
    plt.legend()
    plt.grid(True)
    plt.show()

#plot phase plane for steady state 5
def plotFig12():

    xInitial = 8
    r = 0.5
    theta = 0.045
    a = 0.001

    yInitial = 3
    s = -0.5
    beta = 0.01
    phi = 0.4

    zInitial = 369
    m = -0.3
    lambdaSymbol = 0.1
    rho = 0.001

    P0 = [xInitial, yInitial, zInitial]
    maxTime = 50
    numSteps = 200000
    RK2a = 1 / 2

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(7.964601769911503, 2.920353982300884, 368.58407079646025, label = "Steady State Point", color = 'green')

    timeVals, P = RK2(P0, maxTime, numSteps, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, RK2a)
    x = P[:, 0]
    y = P[:, 1]
    z = P[:, 2]
    ax.plot(x, y, z, label = 'P* = (8, 3, 369)')
    
    
    P0 = [9, 4, 370]
    timeVals, P = RK2(P0, maxTime, numSteps, r, theta, a, s, beta, phi, m, lambdaSymbol, rho, RK2a)
    x = P[:, 0]
    y = P[:, 1]
    z = P[:, 2]
    ax.plot(x, y, z, label = 'P* = (9, 4, 370)')
    
    ax.set_title("Phase Plane Diagram Centered Around Steady State 5")
    ax.set_xlabel('Population (Flies)')
    ax.set_ylabel('Population (Spiders)')
    ax.set_zlabel('Population (Frogs)')
    ax.legend()
    plt.show()

#########################
# UNCOMMENT TO SHOW FIGS
#########################

#plotFig11()
#plotFig12()
