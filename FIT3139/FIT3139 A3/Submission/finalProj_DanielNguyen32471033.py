import numpy as np
import copy
import matplotlib.pyplot as plt

'''
Name: Daniel Nguyen
Student Number: 32471033

Last Edit: 14/06 2:26PM
'''

##############
#Player Class
##############
class Player():
    
    def __init__(self, name, stats):
        #assign player name and player point statistics
        self.name = name

        self.winServeProb = stats[0]
        self.dblFaultProb = stats[1]
        self.inPlayServeProb = stats[2]
        
        self.returnWinProb = stats[3]
        self.returnInPlayProb = stats[4]
        self.returnLoseProb = stats[5]
        
        self.rallyWinProb = stats[6]
        self.rallyLoseProb = stats[7]
        self.rallyInPlayProb = stats[8]  

##############
#Point Class
##############       
class Point():
    
    def __init__(self, player1, player2):
        #save players to class
        self.player1 = player1
        self.player2 = player2
        
        #get player 1 stats from player class
        p1WinServeProb = player1.winServeProb
        p1DblFaultProb = player1.dblFaultProb
        p1InPlayServeProb = player1.inPlayServeProb

        p1ReturnWinProb = player1.returnWinProb
        p1ReturnInPlayProb = player1.returnInPlayProb
        p1ReturnLoseProb = player1.returnLoseProb
        
        p1RallyWinProb = player1.rallyWinProb
        p1RallyLoseProb = player1.rallyLoseProb
        p1RallyInPlayProb = player1.rallyInPlayProb
        
        #get player 2 stats from player class
        p2WinServeProb = player2.winServeProb
        p2DblFaultProb = player2.dblFaultProb
        p2InPlayServeProb = player2.inPlayServeProb
        
        p2ReturnWinProb = player2.returnWinProb
        p2ReturnInPlayProb = player2.returnInPlayProb
        p2ReturnLoseProb = player2.returnLoseProb
        
        p2RallyWinProb = player2.rallyWinProb
        p2RallyLoseProb = player2.rallyLoseProb
        p2RallyInPlayProb = player2.rallyInPlayProb
        
        #create transition matrix for point markov chain
        pointMatrix = np.array([
            [0, 0, 0, p1InPlayServeProb, 0, 0, p1WinServeProb, p1DblFaultProb], # P1 Serve
            [0, 0, p2InPlayServeProb, 0, 0, 0, p2DblFaultProb, p2WinServeProb], # P2 Serve
            [0, 0, 0, 0, 0, p1ReturnInPlayProb, p1ReturnWinProb, p1ReturnLoseProb], # P1 Return
            [0, 0, 0, 0, p2ReturnInPlayProb, 0, p2ReturnLoseProb, p2ReturnWinProb], # P2 Return
            [0, 0, 0, 0, 0, p1RallyInPlayProb, p1RallyWinProb, p1RallyLoseProb], # P1 Rally Hit
            [0, 0, 0, 0, p2RallyInPlayProb, 0, p2RallyLoseProb, p2RallyWinProb], # P2 Rally Hit
            [0, 0, 0, 0, 0, 0, 1, 0], # P1 Win
            [0, 0, 0, 0, 0, 0, 0, 1]  # P2 Win
        ])
        
        self.pointMatrix = pointMatrix
    
    #point chain monte carlo simulation
    def monteCarlo(self, numIterations):
        
        print("-------------------------------------------------------")
        print("Start Point Monte Carlo Simulation")
        
        player1Wins = 0
        player2Wins = 0
        
        print(f"{self.player1.name} is serving")
          
        #run numIterations iterations with player1 Serving    
        playerServing = 0
        for iteration in range(numIterations):
            if self.simulatePoint(playerServing) == 1:
                player1Wins += 1
            
            if iteration % 2000 == 0:
                print(f"Iteration: {iteration}")
        
        print(f"{self.player2.name} is serving")
        
        #run numIterations iterations with player2 Serving
        playerServing = 1
        for iteration in range(numIterations):
            if self.simulatePoint(playerServing) == 1:
                player2Wins += 1
            
            if iteration % 2000 == 0:
                print(f"Iteration: {iteration}")
        

        self.p1WinProbWhenServing = player1Wins / numIterations
        
        self.p2WinProbWhenServing = player2Wins / numIterations
            
        print("-------------------------------------------------------")
        print(f"{self.player1.name}'s chance of winning when serving:")
        print(f"{self.p1WinProbWhenServing}")
        print(f"{self.player2.name}'s chance of winning when serving:")
        print(f"{self.p2WinProbWhenServing}")
        print("-------------------------------------------------------")
    
    #simulate a single point
    #used to model tiebreaks
    def simulatePoint(self, playerServing):
        
        numStates = len(self.pointMatrix)
        
        #determine which player is serving
        if playerServing == 0:
            currentState = 0
        if playerServing == 1:
            currentState = 1
        
        #keep playing the point until someone has won   
        while currentState not in [6, 7]:
            transitionProb = self.pointMatrix[currentState]
            nextState = np.random.choice(numStates, p = transitionProb)
                
            currentState = nextState
        
        if currentState == 6 and playerServing == 0:
            return 1
            
        if currentState == 7 and playerServing == 1:
            return 1
        
        return 0
            
###################           
#tennisMatch Class
################### 
class tennisMatch():
    
    def __init__(self, player1, player2):
        
        self.player1 = player1
        self.player2 = player2
    
    #create gameMatrix based on point markov chain + monte carlo simulation
    def createGameMatrix(self, numIterations):
        
        gamePoint = Point(self.player1, self.player2)
        gamePoint.monteCarlo(numIterations)
        
        #create transition matrix for when player 1 is serving
        p = gamePoint.p1WinProbWhenServing
        
        p1gameMatrix = np.array([
            [0, p, 0, 0, 1-p, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 0 - 0
            [0, 0, p, 0, 0, 0, 0, 1-p, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 15 - 0
            [0, 0, 0, p, 0, 0, 0, 0, 1-p, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 30 - 0
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1-p, 0, 0, 0, 0, 0, 0, 0, 0, p, 0], # 40 - 0
            [0, 0, 0, 0, 0, 1-p, 0, p, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 0 - 15
            [0, 0, 0, 0, 0, 0, 1-p, 0, p, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 0 - 30
            [0, 0, 0, 0, 0, 0, 0, 0, 0, p, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1-p], # 0 - 40 
            [0, 0, 0, 0, 0, 0, 0, 0, p, 0, 1-p, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 15 - 15
            [0, 0, 0, 0, 0, 0, 0, 0, 0, p, 0, 0, 1-p, 0, 0, 0, 0, 0, 0, 0], # 30 - 15
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1-p, 0, 0, 0, 0, p, 0], # 40 - 15
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, p, 0, 1-p, 0, 0, 0, 0, 0], # 15 - 30
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, p, 0, 0, 0, 0, 1-p], # 15 - 40
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, p, 1-p, 0, 0, 0, 0, 0], # 30 - 30
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1-p, 0, 0, p, 0], # 40 - 30
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, p, 0, 0, 0, 1-p], # 30 - 40
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, p, 1-p, 0, 0], # Deuce
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1-p, 0, 0, p, 0], # Advantage Server
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, p, 0, 0, 0, 1-p], # Advantage Receiver
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], # Server Wins
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1] # Receiver Wins
        ])
        
        self.p1ServingGameMatrix = p1gameMatrix
        
        #create transition matrix for when player 2 is serving
        p = gamePoint.p2WinProbWhenServing
        
        p2gameMatrix = np.array([
            [0, p, 0, 0, 1-p, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 0 - 0
            [0, 0, p, 0, 0, 0, 0, 1-p, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 15 - 0
            [0, 0, 0, p, 0, 0, 0, 0, 1-p, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 30 - 0
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1-p, 0, 0, 0, 0, 0, 0, 0, 0, p, 0], # 40 - 0
            [0, 0, 0, 0, 0, 1-p, 0, p, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 0 - 15
            [0, 0, 0, 0, 0, 0, 1-p, 0, p, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 0 - 30
            [0, 0, 0, 0, 0, 0, 0, 0, 0, p, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1-p], # 0 - 40 
            [0, 0, 0, 0, 0, 0, 0, 0, p, 0, 1-p, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 15 - 15
            [0, 0, 0, 0, 0, 0, 0, 0, 0, p, 0, 0, 1-p, 0, 0, 0, 0, 0, 0, 0], # 30 - 15
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1-p, 0, 0, 0, 0, p, 0], # 40 - 15
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, p, 0, 1-p, 0, 0, 0, 0, 0], # 15 - 30
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, p, 0, 0, 0, 0, 1-p], # 15 - 40
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, p, 1-p, 0, 0, 0, 0, 0], # 30 - 30
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1-p, 0, 0, p, 0], # 40 - 30
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, p, 0, 0, 0, 1-p], # 30 - 40
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, p, 1-p, 0, 0], # Deuce
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1-p, 0, 0, p, 0], # Advantage Server
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, p, 0, 0, 0, 1-p], # Advantage Receiver
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], # Server Wins
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1] # Receiver Wins
        ])
        
        self.p2ServingGameMatrix = p2gameMatrix
    
    #simulate a single game
    def simulateGame(self, playerToServe):
        
        #20 states in the game transition matrix
        numStates = 20
        
        #change matrix depending on who is serving
        if playerToServe == 0:
            gameMatrix = self.p1ServingGameMatrix
        if playerToServe == 1:
            gameMatrix = self.p2ServingGameMatrix
        
        #game starts at 0 - 0
        currentState = 0
                
        while currentState not in [18, 19]:
            transitionProb = gameMatrix[currentState]
            nextState = np.random.choice(numStates, p = transitionProb)
            
            #return 1 if server wins
            if nextState == 18:
                return 1
            
            #return 0 if receiver wins
            if nextState == 19:
                return 0
                
            currentState = nextState
    
    #simulate a single set
    def simulateSet(self, playerToServe):
        
        #which player is serving
        currentServing = playerToServe
        nextServing = abs(currentServing - 1)
        
        #initialise game scores to 0
        p1Games = 0
        p2Games = 0
        
        keepPlaying = True
        
        #keep simulating until a player has won the set
        while keepPlaying:
            
            #tiebreak handling
            if p1Games + p2Games == 12:
                tiebreakWinner = self.simulateTiebreak(nextServing)
                if tiebreakWinner == 0:
                    p1Games += 1
                if tiebreakWinner == 1:
                    p2Games += 1
                break
            
            #simulate a game
            gameWinner = self.simulateGame(currentServing)
            
            #if player1 is serving
            if currentServing == 0:
                if gameWinner == 1:
                    p1Games += 1
                else:
                    p2Games += 1
                    
            #if player2 is serving
            if currentServing == 1:
                if gameWinner == 1:
                    p2Games += 1
                else:
                    p1Games += 1
            
            #swap servers
            currentServing, nextServing = nextServing, currentServing
            
            #set next set initial server
            #its inside the loop because if its outside it overwrites tiebreaker next set server
            #:)
            self.nextSetServer = abs(playerToServe - 1)
            
            #check if set has been won, and end while loop if it has
            if (p1Games >= 6 or p2Games >= 6) and abs(p1Games - p2Games) >= 2:
                keepPlaying = False
        
        ########################################################################################
        ########## COMMENT THIS SECTION OUT IF YOU WANT TO SIMULATE A GAME ON ITS OWN ##########
        ########################################################################################
        #save game scores
        self.gameScores.append([p1Games, p2Games])
        ########################################################################################
        ########################################################################################
        
        #return winner of set
        if p1Games > p2Games:
            return 0
        else:
            return 1
                
    #simulate a tiebreak
    def simulateTiebreak(self, playerToServe):
        
        p1Score = 0
        p2Score = 0
        currentServe = playerToServe
        
        #whoever serves first in a tiebreak game receives at the start of the next set
        self.nextSetServer = abs(playerToServe - 1)
        
        #initialise point object to simulate points
        tiebreakPoint = Point(self.player1, self.player2)
        
        #first point simulation (serve swaps after 1st point and then every 2 points after that)
        pointOutcome = tiebreakPoint.simulatePoint(currentServe)
        
        #if p1 is serving
        if playerToServe == 0:
            if pointOutcome == 1:
                p1Score += 1
            else:
                p2Score += 1
        
        #if p2 is serving
        if playerToServe == 1:
            if pointOutcome == 1:
                p2Score += 1
            else:
                p1Score += 1
        
        currentServe = abs(currentServe - 1)
        
        #simulate rest of the tiebreak points 
        while not ((p1Score >=7 or p2Score >= 7) and abs(p1Score - p2Score) >= 2): 
            
            pointOutcome = tiebreakPoint.simulatePoint(currentServe)
        
            #if p1 is serving
            if playerToServe == 0:
                if pointOutcome == 1:
                    p1Score += 1
                else:
                    p2Score += 1
            
            #if p2 is serving
            if playerToServe == 1:
                if pointOutcome == 1:
                    p2Score += 1
                else:
                    p1Score += 1
            
            #swap serves if the sum of the scores is odd
            if (p1Score + p2Score) % 2 == 1:
                currentServe = abs(currentServe - 1)
        
        #return 0 if player 1 wins tiebreak
        if p1Score > p2Score:
            return 0
        
        #return 1 if player 2 wins tiebreak
        return 1
    
    #simulate a single match
    def simulateMatch(self):
        
        #save game scores for each set
        self.gameScores = []
        
        #initialise set scores
        p1Sets = 0
        p2Sets = 0
        
        #flip a coin to see who serves at start of first set
        server = np.random.randint(2)
        
        #generate a set outcome
        setOutcome = self.simulateSet(server)
        
        if setOutcome == 0:
            p1Sets += 1
        else:
            p2Sets += 1
        
        #keep playing the match until a player has won
        keepPlaying = True
        while keepPlaying:
            
            #increment set score for whoever wins the set
            setOutcome = self.simulateSet(self.nextSetServer)
            if setOutcome == 0:
                p1Sets += 1
            else:
                p2Sets += 1
            
            #if a player reaches 3 sets won, they win the match, and we break the while loop
            if p1Sets == 3 or p2Sets == 3:
                keepPlaying = False
        
        #save set scores
        self.setScores = [p1Sets, p2Sets]
        
        #return winner
        if p1Sets == 3:
            return 0
        else:
            return 1
            
#Simulate a Tournament
#firstRoundBracket is in format [[player1, player2], [player3, player4]]]
#left to right is single elimination top to bottom where match 1 winner plays vs match 2 winner etc.
#total number of players must be a power of 2
def simulateTournament(firstRoundBracket, pointIterations, matchDict):

    #create complete tournament bracket, with empty arrays to be filled in with match winners
    tournamentBracket = []
    tournamentBracket.append(firstRoundBracket)

    while len(tournamentBracket[-1]) >= 2:
        if len(tournamentBracket[-1]) >= 2:
            tournamentBracket.append([])
        for i in range(len(tournamentBracket[-2]) // 2):
            tournamentBracket[-1].append([None, None])
    
    #copy tournament bracket as results array
    #lazy way to do it but oh well
    resultsArray = copy.deepcopy(tournamentBracket)
        
    #simulate every match except the final
    for roundNum in range(len(tournamentBracket) - 1):
        for matchNum in range(len(tournamentBracket[roundNum])):
            
            #get players to play in match
            player1 = tournamentBracket[roundNum][matchNum][0]
            player2 = tournamentBracket[roundNum][matchNum][1]
            
            #if match has already been generated before use existing match data
            currentMatchName = player1.name + player2.name
            if currentMatchName in matchDict:
                currentMatch = matchDict[currentMatchName]      
            
            #else generate new one
            else:
                currentMatch = tennisMatch(player1, player2)
                currentMatch.createGameMatrix(pointIterations)
                matchDict[currentMatchName] = currentMatch     
            
            #get match winner
            matchWinner = currentMatch.simulateMatch()
            
            if matchWinner == 0:
                nextRoundParticipant = player1
            else:
                nextRoundParticipant = player2
            
            #store gameScores in results array
            resultsArray[roundNum][matchNum] = currentMatch.gameScores
            
            #set next round participant
            if matchNum % 2 == 0:
                tournamentBracket[roundNum + 1][matchNum // 2][0] = nextRoundParticipant
            else:
                tournamentBracket[roundNum + 1][matchNum // 2][1] = nextRoundParticipant
    
    #simulate final
    player1 = tournamentBracket[-1][-1][0]
    player2 = tournamentBracket[-1][-1][1]
    
    #if matchup has already been played use existing markov chain
    currentMatchName = player1.name + player2.name
    if currentMatchName in matchDict:
        currentMatch = matchDict[currentMatchName]
        
    #otherwise generate new markov chain
    else:
        currentMatch = tennisMatch(player1, player2)
        currentMatch.createGameMatrix(pointIterations)
        matchDict[currentMatchName] = currentMatch
    
    #get match winner
    matchWinner = currentMatch.simulateMatch()
    
    #save scores
    resultsArray[-1][-1] = [currentMatch.gameScores]
    
    #return winner, completed tournament bracket, complete results, dictionary of played matches
    if matchWinner == 0:
        return player1, tournamentBracket, resultsArray, matchDict
    else:
        return player2, tournamentBracket, resultsArray, matchDict

#################       
#Player Creation
#################

#FOR TESTING 
def createRafaelNadal():
    #serve stats
    totalServe = 26381
    totalAce = 986
    totalFcdError = 4155
    totalDblFault = 307 + 252 #total double faults on both ad and deuce court
    
    #return stats
    totalReturn = 27642
    totalInPlay = 20599
    totalRetWinner = 263
    
    #rally stats
    totalShot = 112560  #total shots
    totalWinner = 6728 + 4931  #total winners + total induced forced errors
    totalUnfError = 7063
    
    #fractional stat creation to be parsed to player class
    winServeProb = (totalAce + totalFcdError) / totalServe
    dblFaultServeProb = totalDblFault / totalServe
    inPlayServeProb = 1 - winServeProb - dblFaultServeProb

    returnWinnerProb = totalRetWinner / totalReturn
    returnInPlayProb = totalInPlay / totalReturn
    returnLoseProb = 1 - returnWinnerProb - returnInPlayProb
    
    rallyWinnerProb = totalWinner / totalShot
    rallyUnfErrorProb = totalUnfError / totalShot
    rallyInPlayProb = 1 - rallyWinnerProb - rallyUnfErrorProb
    
    RafaelNadal = Player("Rafael Nadal", 
                         [winServeProb, dblFaultServeProb, inPlayServeProb, 
                          returnWinnerProb, returnInPlayProb, returnLoseProb,
                          rallyWinnerProb, rallyUnfErrorProb, rallyInPlayProb])
    
    return RafaelNadal

#FOR TESTING
def createRogerFederer():
    #serve stats
    totalServe = 35740
    totalAce = 3585
    totalFcdError = 6234
    totalDblFault = 395 + 383 #total double faults on both ad and deuce court
    
    #return stats
    totalReturn = 37979
    totalInPlay = 26402
    totalRetWinner = 539
    
    #rally stats
    totalShot = 121557  #total shots
    totalWinner = 10134 + 6796  #total winners + total induced forced errors
    totalUnfError = 11595
    
    #fractional stat creation to be parsed to player class
    winServeProb = (totalAce + totalFcdError) / totalServe
    dblFaultServeProb = totalDblFault / totalServe
    inPlayServeProb = 1 - winServeProb - dblFaultServeProb

    returnWinnerProb = totalRetWinner / totalReturn
    returnInPlayProb = totalInPlay / totalReturn
    returnLoseProb = 1 - returnWinnerProb - returnInPlayProb
    
    rallyWinnerProb = totalWinner / totalShot
    rallyUnfErrorProb = totalUnfError / totalShot
    rallyInPlayProb = 1 - rallyWinnerProb - rallyUnfErrorProb
    
    RogerFederer = Player("Roger Federer", 
                         [winServeProb, dblFaultServeProb, inPlayServeProb, 
                          returnWinnerProb, returnInPlayProb, returnLoseProb,
                          rallyWinnerProb, rallyUnfErrorProb, rallyInPlayProb])
    
    return RogerFederer

def createCarlosAlcaraz():
    #serve stats
    totalServe = 35740
    totalAce = 3585
    totalFcdError = 6234
    totalDblFault = 60 + 44 #total double faults on both ad and deuce court
    
    #return stats
    totalReturn = 4453
    totalInPlay = 3113
    totalRetWinner = 73
    
    #rally stats
    totalShot = 14866   #total shots
    totalWinner = 1224 + 837  #total winners + total induced forced errors
    totalUnfError = 1316
    
    #fractional stat creation to be parsed to player class
    winServeProb = (totalAce + totalFcdError) / totalServe
    dblFaultServeProb = totalDblFault / totalServe
    inPlayServeProb = 1 - winServeProb - dblFaultServeProb

    returnWinnerProb = totalRetWinner / totalReturn
    returnInPlayProb = totalInPlay / totalReturn
    returnLoseProb = 1 - returnWinnerProb - returnInPlayProb
    
    rallyWinnerProb = totalWinner / totalShot
    rallyUnfErrorProb = totalUnfError / totalShot
    rallyInPlayProb = 1 - rallyWinnerProb - rallyUnfErrorProb
    
    CarlosAlcaraz = Player("Carlos Alcaraz", 
                         [winServeProb, dblFaultServeProb, inPlayServeProb, 
                          returnWinnerProb, returnInPlayProb, returnLoseProb,
                          rallyWinnerProb, rallyUnfErrorProb, rallyInPlayProb])
    
    return CarlosAlcaraz

def createAlexanderZverev():
    #serve stats
    totalServe = 12490
    totalAce = 1220
    totalFcdError = 2197
    totalDblFault = 263 + 251 #total double faults on both ad and deuce court
    
    #return stats
    totalReturn = 12951
    totalInPlay = 9095
    totalRetWinner = 134
    
    #rally stats
    totalShot = 45642   #total shots
    totalWinner = 2685 + 1955   #total winners + total induced forced errors
    totalUnfError = 3751
    
    #fractional stat creation to be parsed to player class
    winServeProb = (totalAce + totalFcdError) / totalServe
    dblFaultServeProb = totalDblFault / totalServe
    inPlayServeProb = 1 - winServeProb - dblFaultServeProb

    returnWinnerProb = totalRetWinner / totalReturn
    returnInPlayProb = totalInPlay / totalReturn
    returnLoseProb = 1 - returnWinnerProb - returnInPlayProb
    
    rallyWinnerProb = totalWinner / totalShot
    rallyUnfErrorProb = totalUnfError / totalShot
    rallyInPlayProb = 1 - rallyWinnerProb - rallyUnfErrorProb
    
    AlexanderZverev = Player("Alexander Zverev", 
                         [winServeProb, dblFaultServeProb, inPlayServeProb, 
                          returnWinnerProb, returnInPlayProb, returnLoseProb,
                          rallyWinnerProb, rallyUnfErrorProb, rallyInPlayProb])
    
    return AlexanderZverev

def createCasperRuud():
    #serve stats
    totalServe = 4695
    totalAce = 268
    totalFcdError = 683
    totalDblFault = 69 + 55 #total double faults on both ad and deuce court
    
    #return stats
    totalReturn = 4684
    totalInPlay = 3380
    totalRetWinner = 51
    
    #rally stats
    totalShot = 16837   #total shots
    totalWinner = 1054 + 687   #total winners + total induced forced errors
    totalUnfError = 1298
    
    #fractional stat creation to be parsed to player class
    winServeProb = (totalAce + totalFcdError) / totalServe
    dblFaultServeProb = totalDblFault / totalServe
    inPlayServeProb = 1 - winServeProb - dblFaultServeProb

    returnWinnerProb = totalRetWinner / totalReturn
    returnInPlayProb = totalInPlay / totalReturn
    returnLoseProb = 1 - returnWinnerProb - returnInPlayProb
    
    rallyWinnerProb = totalWinner / totalShot
    rallyUnfErrorProb = totalUnfError / totalShot
    rallyInPlayProb = 1 - rallyWinnerProb - rallyUnfErrorProb
    
    CasperRuud = Player("Casper Ruud", 
                         [winServeProb, dblFaultServeProb, inPlayServeProb, 
                          returnWinnerProb, returnInPlayProb, returnLoseProb,
                          rallyWinnerProb, rallyUnfErrorProb, rallyInPlayProb])
    
    return CasperRuud

def createJannikSinner():
    #serve stats
    totalServe = 4768
    totalAce = 408
    totalFcdError = 705
    totalDblFault = 61 + 65 #total double faults on both ad and deuce court
    
    #return stats
    totalReturn = 4998
    totalInPlay = 3530 
    totalRetWinner = 51
    
    #rally stats
    totalShot = 18479   #total shots
    totalWinner = 1236 + 916   #total winners + total induced forced errors
    totalUnfError = 1558
    
    #fractional stat creation to be parsed to player class
    winServeProb = (totalAce + totalFcdError) / totalServe
    dblFaultServeProb = totalDblFault / totalServe
    inPlayServeProb = 1 - winServeProb - dblFaultServeProb

    returnWinnerProb = totalRetWinner / totalReturn
    returnInPlayProb = totalInPlay / totalReturn
    returnLoseProb = 1 - returnWinnerProb - returnInPlayProb
    
    rallyWinnerProb = totalWinner / totalShot
    rallyUnfErrorProb = totalUnfError / totalShot
    rallyInPlayProb = 1 - rallyWinnerProb - rallyUnfErrorProb
    
    JannikSinner = Player("Jannik Sinner", 
                         [winServeProb, dblFaultServeProb, inPlayServeProb, 
                          returnWinnerProb, returnInPlayProb, returnLoseProb,
                          rallyWinnerProb, rallyUnfErrorProb, rallyInPlayProb])
    
    return JannikSinner

def createNovakDjokovic():
    #serve stats
    totalServe = 30155
    totalAce = 1995
    totalFcdError = 4974
    totalDblFault = 383 + 428 #total double faults on both ad and deuce court
    
    #return stats
    totalReturn = 31165
    totalInPlay = 22153 
    totalRetWinner = 444
    
    #rally stats
    totalShot = 127269   #total shots
    totalWinner = 7135 + 6502   #total winners + total induced forced errors
    totalUnfError = 9257
    
    #fractional stat creation to be parsed to player class
    winServeProb = (totalAce + totalFcdError) / totalServe
    dblFaultServeProb = totalDblFault / totalServe
    inPlayServeProb = 1 - winServeProb - dblFaultServeProb

    returnWinnerProb = totalRetWinner / totalReturn
    returnInPlayProb = totalInPlay / totalReturn
    returnLoseProb = 1 - returnWinnerProb - returnInPlayProb
    
    rallyWinnerProb = totalWinner / totalShot
    rallyUnfErrorProb = totalUnfError / totalShot
    rallyInPlayProb = 1 - rallyWinnerProb - rallyUnfErrorProb
    
    NovakDjokovic = Player("Novak Djokovic", 
                         [winServeProb, dblFaultServeProb, inPlayServeProb, 
                          returnWinnerProb, returnInPlayProb, returnLoseProb,
                          rallyWinnerProb, rallyUnfErrorProb, rallyInPlayProb])
    
    return NovakDjokovic

def createAlexDeMinaur():
    #serve stats
    totalServe = 3908
    totalAce = 186
    totalFcdError = 510
    totalDblFault = 60 + 64 #total double faults on both ad and deuce court
    
    #return stats
    totalReturn = 4018
    totalInPlay = 2895
    totalRetWinner = 30
    
    #rally stats
    totalShot = 17907   #total shots
    totalWinner = 797 + 657   #total winners + total induced forced errors
    totalUnfError = 1236
    
    #fractional stat creation to be parsed to player class
    winServeProb = (totalAce + totalFcdError) / totalServe
    dblFaultServeProb = totalDblFault / totalServe
    inPlayServeProb = 1 - winServeProb - dblFaultServeProb

    returnWinnerProb = totalRetWinner / totalReturn
    returnInPlayProb = totalInPlay / totalReturn
    returnLoseProb = 1 - returnWinnerProb - returnInPlayProb
    
    rallyWinnerProb = totalWinner / totalShot
    rallyUnfErrorProb = totalUnfError / totalShot
    rallyInPlayProb = 1 - rallyWinnerProb - rallyUnfErrorProb
    
    AlexDeMinaur = Player("Alex De Minaur", 
                         [winServeProb, dblFaultServeProb, inPlayServeProb, 
                          returnWinnerProb, returnInPlayProb, returnLoseProb,
                          rallyWinnerProb, rallyUnfErrorProb, rallyInPlayProb])
    
    return AlexDeMinaur

def createStefanosTsitsipas():
    #serve stats
    totalServe = 6068
    totalAce = 540
    totalFcdError = 978
    totalDblFault = 91 + 87 #total double faults on both ad and deuce court
    
    #return stats
    totalReturn = 5798
    totalInPlay = 3958  
    totalRetWinner = 54 
    
    #rally stats
    totalShot = 19304   #total shots
    totalWinner = 1386 + 992    #total winners + total induced forced errors
    totalUnfError = 1731 
    
    #fractional stat creation to be parsed to player class
    winServeProb = (totalAce + totalFcdError) / totalServe
    dblFaultServeProb = totalDblFault / totalServe
    inPlayServeProb = 1 - winServeProb - dblFaultServeProb

    returnWinnerProb = totalRetWinner / totalReturn
    returnInPlayProb = totalInPlay / totalReturn
    returnLoseProb = 1 - returnWinnerProb - returnInPlayProb
    
    rallyWinnerProb = totalWinner / totalShot
    rallyUnfErrorProb = totalUnfError / totalShot
    rallyInPlayProb = 1 - rallyWinnerProb - rallyUnfErrorProb
    
    StefanosTsitsipas = Player("Stefanos Tsitsipas", 
                         [winServeProb, dblFaultServeProb, inPlayServeProb, 
                          returnWinnerProb, returnInPlayProb, returnLoseProb,
                          rallyWinnerProb, rallyUnfErrorProb, rallyInPlayProb])
    
    return StefanosTsitsipas

def createGrigorDimitrov():
    #serve stats
    totalServe = 7521
    totalAce = 654 
    totalFcdError = 1106 
    totalDblFault = 157 + 152 #total double faults on both ad and deuce court
    
    #return stats
    totalReturn = 7514
    totalInPlay = 5091  
    totalRetWinner = 89 
    
    #rally stats
    totalShot = 26702  #total shots
    totalWinner = 1748 + 1226   #total winners + total induced forced errors
    totalUnfError = 2393
    
    #fractional stat creation to be parsed to player class
    winServeProb = (totalAce + totalFcdError) / totalServe
    dblFaultServeProb = totalDblFault / totalServe
    inPlayServeProb = 1 - winServeProb - dblFaultServeProb

    returnWinnerProb = totalRetWinner / totalReturn
    returnInPlayProb = totalInPlay / totalReturn
    returnLoseProb = 1 - returnWinnerProb - returnInPlayProb
    
    rallyWinnerProb = totalWinner / totalShot
    rallyUnfErrorProb = totalUnfError / totalShot
    rallyInPlayProb = 1 - rallyWinnerProb - rallyUnfErrorProb
    
    GrigorDimitrov = Player("Grigor Dimitrov", 
                         [winServeProb, dblFaultServeProb, inPlayServeProb, 
                          returnWinnerProb, returnInPlayProb, returnLoseProb,
                          rallyWinnerProb, rallyUnfErrorProb, rallyInPlayProb])
    
    return GrigorDimitrov

def createMrServe():
      
    #fractional stat creation to be parsed to player class
    winServeProb = 0.08 * 1.05
    dblFaultServeProb = 0.06 * 0.95
    inPlayServeProb = 1 - winServeProb - dblFaultServeProb

    returnWinnerProb = 0.02
    returnInPlayProb = 0.96 * 0.71  #returns in play * proportion of returnable serves
    returnLoseProb = 1 - returnWinnerProb - returnInPlayProb
    
    rallyWinnerProb = 0.07 + 0.05
    rallyUnfErrorProb = 0.09
    rallyInPlayProb = 1 - rallyWinnerProb - rallyUnfErrorProb
    
    mrServe = Player("Mr Serve", 
                         [winServeProb, dblFaultServeProb, inPlayServeProb, 
                          returnWinnerProb, returnInPlayProb, returnLoseProb,
                          rallyWinnerProb, rallyUnfErrorProb, rallyInPlayProb])
    
    return mrServe

def createMrReceive():
      
    #fractional stat creation to be parsed to player class
    winServeProb = 0.08 
    dblFaultServeProb = 0.06
    inPlayServeProb = 1 - winServeProb - dblFaultServeProb

    returnWinnerProb = 0.02 * 1.05
    returnInPlayProb = 1 * 0.71     #returns in play * proportion of returnable serves
    returnLoseProb = 1 - returnWinnerProb - returnInPlayProb
    
    rallyWinnerProb = 0.07 + 0.05
    rallyUnfErrorProb = 0.09
    rallyInPlayProb = 1 - rallyWinnerProb - rallyUnfErrorProb
    
    mrReceive = Player("Mr Receive", 
                         [winServeProb, dblFaultServeProb, inPlayServeProb, 
                          returnWinnerProb, returnInPlayProb, returnLoseProb,
                          rallyWinnerProb, rallyUnfErrorProb, rallyInPlayProb])
    
    return mrReceive

def createMrRally():
      
    #fractional stat creation to be parsed to player class
    winServeProb = 0.08
    dblFaultServeProb = 0.06
    inPlayServeProb = 1 - winServeProb - dblFaultServeProb

    returnWinnerProb = 0.02
    returnInPlayProb = 0.96 * 0.71  #returns in play * proportion of returnable serves
    returnLoseProb = 1 - returnWinnerProb - returnInPlayProb
    
    rallyWinnerProb = (0.07 + 0.05) * 1.05
    rallyUnfErrorProb = 0.09 * 0.95
    rallyInPlayProb = 1 - rallyWinnerProb - rallyUnfErrorProb
    
    mrRally = Player("Mr Rally", 
                         [winServeProb, dblFaultServeProb, inPlayServeProb, 
                          returnWinnerProb, returnInPlayProb, returnLoseProb,
                          rallyWinnerProb, rallyUnfErrorProb, rallyInPlayProb])
    
    return mrRally
#####################        
#End Player Creation
#####################

###########################
# Figure Creation
###########################

#draw figure 1
#grand final outcome distribution
def drawFig1():
    
    carlosWins = 0
    alexWins = 0
    
    #create players
    carlos = createCarlosAlcaraz()
    alex = createAlexanderZverev()
    
    #create match
    simMatch = tennisMatch(carlos, alex)
    simMatch.createGameMatrix(10000)
    
    for _ in range(5000):
        
        #printing iterations
        print(f"Simulating Match Number: {_} ")
        
        matchResult = simMatch.simulateMatch()
        if matchResult == 0:
            carlosWins += 1
        else:
            alexWins += 1 
    
    #print results
    print(carlosWins)
    print(alexWins)

    #get pie chart info
    labels = ["Carlos Alcaraz", "Alexander Zverev"]
    sizes = [carlosWins, alexWins]
    
    #draw plots
    plt.pie(sizes, labels = labels, autopct = "%1.2f%%", shadow = True)
    plt.title("Roland Garros Finals Simulated Winning Probabilities after 5000 Simulations")
    plt.axis("equal")
    
    plt.show()

#draw figure 2
#plot finals score distribution
def drawFig2():

    carlosWinsNumGames = [0, 0, 0]
    alexWinsNumGames = [0, 0, 0]
    
    #create players
    carlos = createCarlosAlcaraz()
    alex = createAlexanderZverev()
    
    #create match
    simMatch = tennisMatch(carlos, alex)
    simMatch.createGameMatrix(10000)
    
    for _ in range(5000):
        
        #printing iterations
        print(f"Simulating Match Number: {_} ")
        
        matchResult = simMatch.simulateMatch()
        if matchResult == 0:
            carlosWinsNumGames[len(simMatch.gameScores) - 3] += 1
        else:
            alexWinsNumGames[len(simMatch.gameScores) - 3] += 1
    
    fig, axs = plt.subplots(1, 2, figsize=(14, 7))
    
    #get pie chart info
    labels1 = ["3 - 0", "3 - 1", "3 - 2"]
    sizes1 = carlosWinsNumGames
    
    labels2 = ["3 - 0", "3 - 1", "3 - 2"]
    sizes2 = alexWinsNumGames
    
    #draw plots
    axs[0].pie(sizes1, labels = labels1, autopct = "%1.2f%%", shadow = True)
    axs[0].set_title("Match Scores for Carlos Alcaraz Wins")
    axs[0].axis("equal")
    
    axs[1].pie(sizes2, labels = labels2, autopct = "%1.2f%%", shadow = True)
    axs[1].set_title("Match Scores for Alexander Zverev Wins")
    axs[1].axis("equal")
    
    plt.show()
    pass

#draw figure 3
#simulate quarterfinals+ of french open
#show champion probabilities
def drawFig3():
    
    #player creation
    novakDjokovic = createNovakDjokovic()
    casperRuud = createCasperRuud()
    alexZverev = createAlexanderZverev()
    alexDeMinaur = createAlexDeMinaur()
    stefanosTsitsipas = createStefanosTsitsipas()
    carlosAlcaraz = createCarlosAlcaraz()
    grigorDimitrov = createGrigorDimitrov()
    jannikSinner = createJannikSinner()
    
    bracket = [[novakDjokovic, casperRuud], [alexZverev, alexDeMinaur], [stefanosTsitsipas, carlosAlcaraz], [grigorDimitrov, jannikSinner]]
    
    results = [0, 0, 0, 0, 0, 0, 0, 0]
    
    matchDict = {}
    
    for tournamentNum in range(2000):
        print(f"Simulating tournament number: {tournamentNum}")
        winner, tournamentBracket, resultsArray, matchDict = simulateTournament(bracket, 10000, matchDict)
        
        if winner == casperRuud:
            results[0] +=  1
        if winner == novakDjokovic:
            results[1] += 1
        if winner == alexZverev:
            results[2] += 1
        if winner == alexDeMinaur:
            results[3] += 1
        if winner == stefanosTsitsipas:
            results[4] += 1
        if winner == carlosAlcaraz:
            results[5] += 1
        if winner == grigorDimitrov:
            results[6] += 1
        if winner == jannikSinner:
            results[7] += 1
      
    #print results        
    print(results)
    
    #get pie chart info
    labels = ["Novak Djokovic", "Casper Ruud", "Alexander Zverev", "Alex De Minaur", 
              "Stefanos Tsitsipas", "Carlos Alcaraz", "Grigor Dimitrov", "Jannik Sinner"]
    sizes = results
    
    #draw plots
    plt.pie(sizes, labels = labels, autopct = "%1.2f%%", shadow = True)
    plt.title("Roland Garros Simulated Winning Probabilities after 2000 Simulations")
    plt.axis("equal")
    
    plt.show()

def drawFig4():
    
    #player creation
    novakDjokovic = createNovakDjokovic()
    casperRuud = createCasperRuud()
    alexZverev = createAlexanderZverev()
    alexDeMinaur = createAlexDeMinaur()
    stefanosTsitsipas = createStefanosTsitsipas()
    carlosAlcaraz = createCarlosAlcaraz()
    grigorDimitrov = createGrigorDimitrov()
    jannikSinner = createJannikSinner()
    
    bracket = [[novakDjokovic, casperRuud], [alexZverev, alexDeMinaur], [stefanosTsitsipas, carlosAlcaraz], [grigorDimitrov, jannikSinner]]
    
    results = np.array([0, 0, 0, 0, 0, 0, 0, 0])
    
    winningProbOverTime = np.zeros((2000, 8))
    
    matchDict = {}
    
    for tournamentNum in range(2000):
        print(f"Simulating tournament number: {tournamentNum}")
        winner, tournamentBracket, resultsArray, matchDict = simulateTournament(bracket, 10000, matchDict)
        
        if winner == casperRuud:
            results[0] +=  1
        if winner == novakDjokovic:
            results[1] += 1
        if winner == alexZverev:
            results[2] += 1
        if winner == alexDeMinaur:
            results[3] += 1
        if winner == stefanosTsitsipas:
            results[4] += 1
        if winner == carlosAlcaraz:
            results[5] += 1
        if winner == grigorDimitrov:
            results[6] += 1
        if winner == jannikSinner:
            results[7] += 1
        
        #store cumulative win probability at each iteration
        winningProbOverTime[tournamentNum] = results / (tournamentNum + 1)
    
    #plot graph
    names = ["Novak Djokovic", "Casper Ruud", "Alexander Zverev", "Alex De Minaur", 
              "Stefanos Tsitsipas", "Carlos Alcaraz", "Grigor Dimitrov", "Jannik Sinner"]
    
    lines = []
    for playerNum in range(8):
        line, = plt.plot(winningProbOverTime[:, playerNum])
        lines.append(line)
    
    plt.legend(lines, names)
    
    plt.title("Winning Probability over Tournaments Simulated")
    plt.xlabel("Number of Tournaments Simulated")
    
    plt.show() 
    
#draw figure 5
#simulate 2500 round robin tournaments
def drawFig5():
    
    results = np.array([0, 0, 0])
    winningProbOverTime = np.zeros((2500, 3))
    
    #create players
    mrServe = createMrServe()
    mrReceive = createMrReceive()
    mrRally = createMrRally()
    
    #create matches and generate game markov chains
    serveReceiveMatch = tennisMatch(mrServe, mrReceive)
    serveReceiveMatch.createGameMatrix(10000)
    
    serveRallymatch = tennisMatch(mrServe, mrRally)
    serveRallymatch.createGameMatrix(10000)
    
    receiveRallymatch = tennisMatch(mrReceive, mrRally)
    receiveRallymatch.createGameMatrix(10000)
    
    #simulate round robin
    for roundRobin in range(2500):
        print(f"Simulating round robin number: {roundRobin}")
        if serveReceiveMatch.simulateMatch() == 0:
            results[0] += 1
        else:
            results[1] += 1
        
        if serveRallymatch.simulateMatch() == 0:
            results[0] += 1
        else:
            results[2] += 1
            
        if receiveRallymatch.simulateMatch() == 0:
            results[1] += 1
        else:
            results[2] == 1
            
        winningProbOverTime[roundRobin] = results / (2 * (roundRobin + 1))
    
    #Plot Graph
    names = ["Mr Serve", "Mr Receive", "Mr Rally"]
    
    lines = []
    for playerNum in range(3):
        line, = plt.plot(winningProbOverTime[:, playerNum])
        lines.append(line)
    
    plt.legend(lines, names)
    
    plt.title("Match Win Probability over 2500 Simulated Round Robin Tournaments")
    plt.xlabel("Number of Tournaments Simulated")
    
    plt.show()
    
    print(results)

###############################################################
#Bottleneck Testing
#
#this was just used by me to see what was taking up
#most of my code runtime
###############################################################
def testFunc():
    rN = createRafaelNadal()
    rF = createRogerFederer()

    matchDict = {}

    for _ in range(1000):
        print(_)
        winner, tournBracket, results, matchArray = simulateTournament([[rN, rF], [rF, rN]], 5000, matchDict)

    for round in range(len(tournBracket)):
        for match in range(len(tournBracket[round])):
            for player in range(len(tournBracket[round][match])):
                tournBracket[round][match][player] = tournBracket[round][match][player].name

import cProfile
def findBottleneck():
    cProfile.run('testFunc()')

###################################################
#uncomment to see code runtime for the testing func
#which simulates 1000 semifinals
###################################################

# findBottleneck()

###################################################

    
###################################################
# Uncomment these to generate figures
###################################################

# drawFig1()
# drawFig2()
# drawFig3()
# drawFig4()
# drawFig5()

###################################################