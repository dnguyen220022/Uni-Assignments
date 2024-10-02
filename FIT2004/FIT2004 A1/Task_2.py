import heapq

class FloorGraph:
    def __init__(self, paths, keys) -> None:
        """
    Creates an adjacency list for the floor, and a list of key locations and clear times
    
    Input:
        paths: a list of tuples in form (start, end, travel time)
        keys: a list of tuples in form (location, clear time)
        
    Output:
        Floor: an adjacency list in form [[start, end, travel time], ...]
        RoomMonster: a list of rooms with a monster + key in form: [[location, clear time], ...]
    
    Time complexity:
        path in paths == O(E)
        
        key in keys == O(V)
        
        i in range(FloorEdges) == O(2(E + V))
        
        max(NodeList) == O(2(E + V))
        
        i in range(MaxNode) == O(V)
        
        edge in FloorEdges == O(E)
        
        Time complexity == O(V + E)
        
    Space complexity:
        i path in paths == creates a list of len(E)
        
        i key in keys == appends V entries to a list
        
        i in range(FloorEdges) == appends 2(E + V) entries to a list
        
        MaxNode == single variable
        
        Floor == create list of len(V)
        
        edge in FloorEdges == appends E + V entries to various lists
        
        Space complexity == O(V + E)
        """
        
        FloorEdges = []                                                 #create edge list for floor
         
        for path in paths:  
            FloorEdges.append([path[0], path[1], path[2]])              #append adjacencies in form [origin, destination, travel time, boolean if source node has a key]        
        
        NodeList = []                                                   #creates list of all start and end nodes
        for i in FloorEdges:
            NodeList.append(i[0])
            NodeList.append(i[1])
                       
                        
        MaxNode = max(NodeList) + 1                                     #finds number of nodes
                
        Floor = []                                                      #create adjacency list for floor
        keyLocations = []                                               #create list of key locations
        for i in range(MaxNode):                                        #appends V lists to Floor and keyLocations
            Floor.append([])
            keyLocations.append([False, None])
        
        for key in keys:
            keyLocations[key[0]] = [True, key[1]]    
        
        for edge in FloorEdges:                                         #Fills the adjacency list with relevant information to make a list that is formed by filling the nth index with a list for x edges exiting the relevant node
            Floor[edge[0]].append(edge)
        
        
        self.FloorToExplore = Floor
        self.numNodes = MaxNode
        self.keyLocations = keyLocations


    def climb(self, start, exits):
        """
        Uses Dijkstras algorithm to find shortest path from start node to all nodes, prioritising paths with at least 1 key, and keeping track of paths and 
        """ 
        
        def Dijkstra(start):
            """
            Implementation of Dijkstras Algorithm with minHeap using heapq python library
            """
            
            MyFloor = self.FloorToExplore
            keyLocations =  self.keyLocations
            queue = []                                                                          #queue is initialised as minHeap
            visited = []
            
            for node in range(self.numNodes):
                visited.append([float('inf'), False, float('inf'), []])                         #appends information for each node in visited array in form: [travel time, key boolean, key clear time, previous node]
                
            visited[start] = [0, False, float('inf'), None]                                     #initialises information on start node in visited array
            
            heapq.heappush(queue, [0, start])                                                   #pushes start node to queue
            
            
            while queue:
                currentNode = heapq.heappop(queue)[1]                                           #pops the node with fastest travel time from the queue 
                
                if visited[currentNode][1] < keyLocations[currentNode][0]:                      #if the path thus far has not picked up a key and there is a key at the current node
                    visited[currentNode] = [visited[currentNode][0] + keyLocations[currentNode][1], True, keyLocations[currentNode][1], visited[currentNode][3]]
                                                                                                #updates node information in visited array in form: [new travel time, key picked up == True, updated key clear time, same path]
                    
                elif keyLocations[currentNode][0] and visited[currentNode][1]:                  #if the path thus far has picked up a key and there is a key at the current node
                    if keyLocations[currentNode][1] < visited[currentNode][2]:                  #if the key at the current node has a faster pickup time than then key picked up on the path 
                        visited[currentNode][0] -= visited[currentNode][2]                      #subtract previous key clear time from travel time
                        visited[currentNode][0] += keyLocations[currentNode][1]                 #add new key clear time to travel time
                        visited[currentNode][2] = keyLocations[currentNode][1]                  #update key clear time to new value
          
                
                for outgoingEdge in MyFloor[currentNode]:                                       #for every outgoing edge of CurrentNode
                    nextNode = outgoingEdge[1]                                                  #store the destination node of edge being looked at
                    
                    if visited[nextNode][1] > visited[currentNode][1]:                          #if the next node has an existing path with a key and the current node does not
                        pass                                                                    #do nothing
                    
                    elif visited[nextNode][1] < visited[currentNode][1]:                        #else if the next node does not have an existing path with a key and the current node does
                        visited[nextNode][0] = visited[currentNode][0] + outgoingEdge[2]        #the travel time to nextNode = travel time of currentNode + travel time of the outgoing edge
                        visited[nextNode][1] = True                                             #update key boolean for nextNode
                        visited[nextNode][2] = visited[currentNode][2]                          #update key clear time for nextNode
                        visited[nextNode][3] = currentNode                                      #update previous node
                        heapq.heappush(queue, [visited[nextNode][0], nextNode])                 #adds nextNode to the minHeap
                    
                    elif visited[nextNode][1] and visited[currentNode][1]:                      #else if both nodes have an existing path with a key
                        if visited[nextNode][0] > visited[currentNode][0] + outgoingEdge[2]:    #if the existing path to the nextNode is longer than the path to the currentNode + traveltime of the outgoingEdge
                            visited[nextNode] = [visited[currentNode][0] + outgoingEdge[2], True, visited[currentNode][2], visited[currentNode][3]]
                                                                                                #updates nextNode info in visited array in form: [new travel time, True key boolean, new key clear time, new previous node]
                            heapq.heappush(queue, [visited[nextNode][0], nextNode])             #pushes nextNode to the queue
                        
                        else:                                                                   #else if the existing path to the nextNode <= path to currentNode + travel time of outgoingEdge
                            pass                                                                #do nothing
                    
                    elif visited[nextNode][1] == False and visited[currentNode][1] == False:    #if existing paths to both nodes do not have a key
                        if visited[nextNode][0] > visited[currentNode][0] + outgoingEdge[2]:    #if the existing path to the nextNode is longer than the path to the currentNode + traveltime of the outgoingEdge
                            visited[nextNode][0] = visited[currentNode][0] + outgoingEdge[2]    #updates path travel time of nextNode
                            visited[nextNode][3] = currentNode                                  #updates previous node
                            heapq.heappush(queue, [visited[nextNode][0], nextNode])             #pushes nextNode to the queue
                            
                        else:                                                                   #if the path travel time to the nextNode <= path to currentNode + travel time of outgoingEdge
                            pass                                                                #do nothing
            
            return(visited)
        
        #output processing
        visited = Dijkstra(start)
        exitList = []
        exitPath = []
        
        for node in range(len(visited)):                    #adds a node number marker to every node in visited
            visited[node].append(node)
            
        
        for exit in exits:
            if visited[exit][1] == True:                    #if a key exists on the path to the exit
                exitList.append(visited[exit])              #add exit info to exitList in form: [[info], exit node]
        
        if exitList == []:                                  #if no exits have a path with a key
            return None                                     #return None
        
        minExit = min(exitList)
        backtrackNode = minExit[4]
        
        while backtrackNode != None:                        #while there is a previous node in the path
            exitPath.append(backtrackNode)                  #append current node to exitPath
            backtrackNode = visited[backtrackNode][3]       #set new previous node
            if backtrackNode == start:
                exitPath.append(backtrackNode)
                break
        
        exitPath.reverse()                                  #reverses path to be from start -> end
        
        return([minExit[0], exitPath])
        
        
        
        
        
    
#testcases

paths = [(0, 1, 4), (1, 2, 2), (2, 3, 3), (3, 4, 1), (1, 5, 2),
(5, 6, 5), (6, 3, 2), (6, 4, 3), (1, 7, 4), (7, 8, 2),
(8, 7, 2), (7, 3, 2), (8, 0, 11), (4, 3, 1), (4, 8, 10)]

keys = [(5, 10), (6, 1), (7, 5), (0, 3), (8, 4)]

MyFloor = FloorGraph(paths, keys)

print(MyFloor.climb(1, [7, 2, 4]))




                
            