import math

class flowGraph():
    '''
    class for a flowGraph that creates an empty adjacency list size n, and contains methods for
    populating the flowGraph with edges and their corresponding reverse edges, as well as methods
    for finding the max flow using the Ford-Fulkerson algorithm
    
    time complexities are explained in the docstrings for their methods
    '''
    def __init__(self, preferences, numCars) -> None:
        '''
        init func for flowGraph. creates an array size N + N/5 + 2 to be populated with edge data
        
        input:
        preferences:
        a list of preferences as stated in assignment briefing
        
        numCars:
        the number of cars required for the number of people travelling, which is the ceiling of
        N/5
        
        time complexity:
        O(N) as a list scaling with N is created
        '''
        '''
        sourceIndex == index of source Node
        sinkIndex == index of sink node
        '''
        self.sourceIndex = len(preferences) + numCars
        self.sinkIndex = self.sourceIndex + 1
        '''
        create flowGraph by initialising flowGraph that contains source Node, sink Node
        create numPeople == total num people travelling
        create array that tracks if each person has been allocated a car
        '''
        self.numPeople = len(preferences)
        self.numCars = numCars
        self.graph = [[], []]
        
        '''
        create nodes for each person
        '''
        for person in preferences:
            self.graph.append([])
        
        '''
        create nodes for each car
        '''
        for car in range(numCars):
            self.graph.append([])
    
    def addEdge(self, source, dest, flow, capacity):
        '''
        adds edges and their corresponding edges to the flowGraph, sets reverse edge of forward edge to
        the reverse edge, and the reverse edge of the reverse edge to the forward edge, and appends both 
        to their relevant places in the flow graph.
        
        input: source, destination, flow, capacity
        
        time complexity:
        constant time
        '''
        edge = Edge(source, dest, flow, capacity)
        reverseEdge = Edge(dest, source, 0, 0)
        edge.setReverseEdge(reverseEdge)
        reverseEdge.setReverseEdge(edge)
        self.graph[source].append(edge)
        self.graph[dest].append(reverseEdge)
    
    def dfs(self, start, target, bottleneck, visited):
        '''
        uses depth first search to go from start to target and augments flow along the way
        
        input:
        start node, end node,
        bottleneck:
            max possible flow along the path
        visited:
            array of visited nodes so as to not repeatedly backtrack
        
        output:
        augment value, which will always be <= bottleneck, as if path cannot be augmented, returns 0,
        else if path can be augmented, you cannot augment more than the bottleneck, as you will overflow
        another edge in the flowGraph
        
        time complexity:
        we only need to find 1 augmenting path, so dfs in this case has a time complexity of 
        O(E)
        '''
        
        '''
        if start and target node are the same, you have reached the sink Node,
        return bottleneck
        
        else:
        mark start node as visited
        '''
        if start == target:
            return bottleneck
        visited[start] = True
        
        '''
        search edges of current node, and find residual flow (this means the edge can be augmented)
        
        if the edge can be augmented, and does not lead to a node already visited on this path, find augment
        value by recursively calling this func on the destination node, with a new bottleneck value,
        as if residual < bottleneck, residual must be the new bottleneck, while keeping track of nodes
        already visited in the visited array.
        
        Once augment value has been found (>0 if path can be augmented, ==0 if cannot)
        if path can be augmented, augment path, return augment value
        
        if path cannot be augmented, return augment value (which will be 0)
        '''
        for edge in self.graph[start]:
            residual = edge.capacity - edge.flow
            if residual > 0 and visited[edge.dest] == False:
                augment = self.dfs(edge.dest, target, min(bottleneck, residual), visited)
                if augment > 0:
                    edge.flow += augment
                    edge.reverseEdge.flow -= augment
                    return augment
        return 0
    
    def fordFulkerson(self):
        '''
        implementation of Ford-Fulkerson algorithm using DFS
        
        time complexity:
        the maximum flow of the flowGraph for this question is N, and in the worst case, each augmentation we
        only increase the maxFlow by 1, therefore with a DFS with complexity E, this implementation of 
        the Ford-Fulkerson algorithm has a worst case time complexity of 
        O(E * maxFlow) == O(E * N)
        '''
        
        '''
        initalise the inital start and target index values, and initalise flow to 0
        '''
        start = self.sourceIndex
        target = self.sinkIndex
        flow = 0

        '''
        initalise visited values for each node to False
        '''
        visited = [False] * len(self.graph)
        
        '''
        find first augmentation path by call dfs func, and updated flow value with augment value
        '''
        augment = self.dfs(start, target, float('inf'), visited)
        flow += augment
        
        '''
        while an augmentation path exists, search for another augmentation path and update flow value.
        Once an augmentation path no longer exists (max flow has been found), return flow value.
        '''
        while augment > 0:
            visited = [False] * len(self.graph)
            augment = self.dfs(start, target, float('inf'), visited)
            flow += augment
        return flow

class Edge():
    '''
    Edge class for use in our flowGraph
    
    time complexity:
    constant time
    '''
    def __init__(self, source, dest, flow, capacity) -> None:
        '''
        initalise the Edge class with info containing the source node, destination node, flow value, capacity
        for each edge.
        Additionally, create the corresponding reverse edge and input both in their relevant positions in the flow graph
        '''
        self.source = source
        self.dest = dest
        self.flow = flow
        self.capacity = capacity
        self.reverseEdge = None

    def setReverseEdge(self, reverseEdge):
        '''
        set the pointer for the reverse edge
        '''
        self.reverseEdge = reverseEdge

def allocate(preferences, licences):
    '''
    main function that checks for edge cases and calls the Ford Fulkerson algorithm,
    first on a flowGraph with only the drivers, to allocate drivers, then on people who have not been
    allocated a car. This func also handles output processing.
    
    input:
    preferences, licences as explained in assignment briefing
    
    output:
    output which contains information regarding car assignments in form:
    [[people in car 1], [people in car 2], ...]
    
    time complexity:
    in the worst case, 2 flowGraphs with N ^ 2 edges is created (source goes to n nodes, which then, in the worst case,
    go to each car, of which there are N/5). the Ford Fulkerson algorithm is then called, which has 
    a time complexity of O(E * maxflow), which results in a time complexity of:
    O(N ^ 2 * n)
    -> (N^3)
    '''
    
    numCars = math.ceil(len(preferences)/5)

    '''
    if there are not enough drivers for cars (num drivers must be >= 2 * num chars)
    return None
    '''
    if len(licences) < numCars * 2:
        return None
    
    '''
    if any person has no preferences
    return None
    '''
    for passengerPrefs in preferences:
        if passengerPrefs == []:
            return None
    
    '''
    sort licences by lower number of preferences, this assures that drivers with less preferences
    get assigned cars first
    '''
    driverprefs = []
    for driver in licences:
        driverprefs.append([len(preferences[driver]), driver])
    driverprefs.sort()
    for driver in range(len(driverprefs)):
        licences[driver] = driverprefs[driver][1]
    
    '''
    initalise the flow graph containing drivers
    '''  
    driverPrefFlowGraph = flowGraph(preferences, numCars)
    
    '''
    add edge for source -> driver
    add edge for driver -> driver car preferences
    '''
    for driver in licences:
        driverPrefFlowGraph.addEdge(driverPrefFlowGraph.sourceIndex, driver, 0, 1)
        for driverpref in preferences[driver]:
            driverPrefFlowGraph.addEdge(driver, len(preferences) + driverpref, 0, 1)

    '''
    add edge for car -> sink
    this edge has capacity 2 as only 2 drivers per car
    '''
    for car in range(numCars):
        driverPrefFlowGraph.addEdge(len(preferences) + car, driverPrefFlowGraph.sinkIndex, 0, 2)
    
    '''
    call fordFulkerson method on created flow graph
    '''
    driverPrefFlowGraph.fordFulkerson()
    
    '''
    mark allocated drivers as allocated, all other drivers will now be passengers.
    This is done by check source node, any edge from source node with a flow of 1 leads to an assigned
    driver, and the corresponding index in remainingAllocations = False, as they have already been
    allocated
    '''
    remainingAllocations = [True] * len(preferences)
    for person in range(len(preferences)):
        for edge in driverPrefFlowGraph.graph[person]:
            if edge.flow == 1:
                remainingAllocations[person] = False
    
    '''
    check if drivers are fully saturated by checking reverse edges of sink node, if saturated, flow
    will be -(flow of forward edge) == -2 
    if not, this means at least 1 car does not have enough drivers, therefore return None
    '''
    for edge in driverPrefFlowGraph.graph[driverPrefFlowGraph.sinkIndex]:
        if edge.flow != -2:
            return None

    '''
    create flow graph for all unallocated people, who are now passengers
    '''
    passengerPrefFlowGraph = flowGraph(preferences, numCars)
    
    '''
    if a person is unallocated:
    create edge source -> passenger
    create edge passenger -> car preference
    '''
    for remainingIndex in range(len(remainingAllocations)):
        if remainingAllocations[remainingIndex] == True:
            passengerPrefFlowGraph.addEdge(driverPrefFlowGraph.sourceIndex, remainingIndex, 0, 1)
            for pref in preferences[remainingIndex]:
                passengerPrefFlowGraph.addEdge(remainingIndex, len(preferences) + pref, 0, 1)
    
    '''
    create edge car -> sink
    this has capacity of 3 as only 3 passengers per car
    '''
    for car in range(numCars):
        passengerPrefFlowGraph.addEdge(len(preferences) + car, driverPrefFlowGraph.sinkIndex, 0, 3)
    
    '''
    call the FordFulkerson method to perform the algorithm on the created flow graph
    '''
    passengerPrefFlowGraph.fordFulkerson()
    
    '''
    if max flow has been achieved but there are still unassigned people (i.e. too many people with conflicting
    preferences), return None
    '''
    for sourceEdge in passengerPrefFlowGraph.graph[passengerPrefFlowGraph.sourceIndex]:
        if sourceEdge.capacity == 1:
            if sourceEdge.flow != 1:
                return None

    '''
    create output array in format:
    [[car 1], [car 2], ...]
    '''
    output = []
    for car in range(numCars):
        output.append([])
    
    '''
    append allocated drivers to ouptut
    '''
    for person in range(len(preferences)):
        for personEdge in driverPrefFlowGraph.graph[person]:
            if personEdge.flow == 1:
                output[personEdge.dest - len(preferences)].append(person)
                break
    '''
    append allocated passengers to output
    '''
    for person in range(len(preferences)):
        for personEdge in passengerPrefFlowGraph.graph[person]:
            if personEdge.flow == 1:
                output[personEdge.dest - len(preferences)].append(person)
                break
    
    return(output)