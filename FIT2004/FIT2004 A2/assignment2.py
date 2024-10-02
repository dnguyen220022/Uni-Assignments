'''
FIT2004 Assignment 2
DANIEL NGUYEN
32471033
'''

'''
Q1
'''
class TrieNode():
    '''
    Creation of a node class for nodes for my Trie

    Time Complexity:
        Only constant time operations
        O(1)
        
    Space Complexity:
        Only constant space operations
        creation of children arrays and empty variables for wordInfo and numMatches
        
        O(1)
    '''
    def __init__(self) -> None:
        '''
        creates a node for placement in a trie:
        creates an array of children that may become nodes themselves (1 for each letter)
        creates variables to check if current node represents a complete word, and the info regarding that word,
        a pointer to the continuing word with highest freq if one exists and the number of following words for the prefix
        represented by the current node
        '''
        self.children = [None] * 26
        self.endWord = False
        self.endWordInfo = None
        self.bestWordInfo = [None, None]
        self.numMatches = 0

class Trie():
    '''
    creation of a Trie class for storage of strings and information regarding them, as well as a way to search for
    the highest frequency word for any given prefix
    '''
    def __init__(self, dictionary) -> None:
        '''
        initialises Trie class by creating first node (firstNode), and then inserting all words of a given dictionary
        into the Trie, creating new nodes of TrieNode class as required. During the creation of the trie, each node also 
        keeps track of the best word so far for the prefix represented by that node.
        
        input:
            dictionary:
                a dictionary of words, definitions, frequencies as outlined in assgn briefing
        
        time complexity:
            runs insert for every word in dictionary, where:
            complexity if insert is O(N) where N is number of chars in given word, thus
            O(T) where T is num of chars in dictionary
        
        space complexity:
            each node with information is a TrieNode, which has space complexity of O(1), thus for T characters in
            the dictionary, there is a space complexity of O(T)
        '''
        self.firstNode = TrieNode()
        
        for wordInfo in dictionary:
            self.insert(wordInfo)

    def insert(self, wordInfo):
        '''
        inserts a word into the Trie, and updating information regarding if the word is the best word for any given prefix
        in the word
        
        input:
            wordInfo:
            an index containing info regarding the word to be input in format: [word, def, freq]
        
        output:
            no defined output however after this func is run for every word in a dictionary it will result in a Trie
            containing every word in the dictionary and information regarding them.
        
        time complexity:
            assignments are all O(1)
            string comparison is O(N) where N is num of chars in word
            
            
            for char in wordInfo[0]:
                runs O(1) operations for each char in word
            
            O(N) where N == num of chars in wordInfo[0] (the word in question)
        
        space complexity:
            explained in docString for __init__ above
        '''
        
        '''
        sets current node to the first node in the Trie (prefix is "")
        empty dictionary case is already covered in prefix_search
        updates numMatches (every word will add +1 to a search with no prefix)
        '''
        node = self.firstNode
        node.numMatches += 1
        
        '''
        checks each char in input word, and creates nodes for each char.
        once each node has been created, numMatches of the created node is incremented by 1
        if node already existed (another word with same current prefix has already been input), new node does not need
        to be created, but numMatches still needs to be incremented, which is done in line 104
        '''
        for char in wordInfo[0]:
            if node.children[ord(char) - ord('a')] == None:
                node.children[ord(char) - ord('a')] = TrieNode()
                node.children[ord(char) - ord('a')].numMatches += 1
            elif node.children[ord(char) - ord('a')] != None:
                node.children[ord(char) - ord('a')].numMatches += 1
                pass
                
            '''
            if no bestWordInfo exists for current prefix, current wordInfo freq and pointer to next letter is assigned
            if bestWordInfo already exists, compare freq and change bestWordInfo to one which has higher freq
            if bestWordInfo already exists, and freq is the same, bestWordInfo pointer points to char with lower value (comes first alphabetically)
            only comparing 1 char strings, which is O(1) time complexity, as using pointers eliminates need for full string comparison
            '''       
            if node.bestWordInfo == [None, None]:
                node.bestWordInfo = [wordInfo[2], ord(char) - ord('a')]
            else:
                if node.bestWordInfo[0] < wordInfo[2]:
                    node.bestWordInfo = [wordInfo[2], ord(char) - ord('a')]
                elif node.bestWordInfo[0] == wordInfo[2]:
                    if ord(char) - ord('a') < node.bestWordInfo[1]:
                        node.bestWordInfo = [wordInfo[2], ord(char) - ord('a')]
            
            '''
            sets node to the next relevant node (letter) in the word being input
            '''
            node = node.children[ord(char) - ord('a')]
        
        '''
        at the end of each word that is input, the final node is updated to represent endWord = True and word info is input into final node.
        as full information regarding each word is only input in the Trie once per word, space complexity does not change
        '''
        node.endWord = True
        node.endWordInfo = wordInfo
            
    def prefix_search(self, prefix):
        '''
        traverses through Trie for any given prefix, and returns [word, def, numMatches] for the word with highest freq
        for the given prefix
        
        input: prefix
            prefix to be traversed in the Trie
            
        output:
            [word, definition, numMatches] for the word with given prefix with highest freq
            
        time complexity:
            traverses the trie only the length of the best word, as at each point, there is a pointer to the next best letter,
            which results in all irrelevant words being ignored. The traversal until end of prefix must always be done, thus it is constant.
            All comparisons and assignments are in constant time.
            
            Therefore:
            
            O(M + N) where M is len(prefix) and N is len(bestWord)
        
        space complexity:
            no scaling variables are created
            
            O(1)
        '''
        
        '''
        sets search start at first node, and traverses the prefix. If no TrieNode exists for given prefix, returns [None, None, 0]
        if prefix exists in the trie, the numMatches for that prefix is found and assigned to a variable to be output
        '''
        node = self.firstNode
        for char in prefix:
            if node.children[ord(char) - ord('a')] == None:
                return [None, None, 0]
            node = node.children[ord(char) - ord('a')]
        numMatches = node.numMatches
        
        
        '''
        wordFound is a dummy variable that is never changed, as loop will always return by len(bestWord) anyway
        if current node does not represent the end of a word, go to the node that contains the bestWord
        if node does not have any children (only represents end of a word), return info regarding that word, as the relevant
        word has been fully traversed.
        if node does represent end of word and children exist, compare freq of that word to the freq of best following word in Trie.
        if freq of word represented by current node >= freq of best word in rest of Trie, return current node word, else keep traversing
        
        after traversal of prefix, this results in travelling down the path of the best word until it is found, all other branches of Trie
        are not traversed, resulting in satisfactory time complexity.
        '''
        wordFound = False
        while not wordFound:
            if node.endWord != True:
                node = node.children[node.bestWordInfo[1]]
            elif node.bestWordInfo == [None, None]:
                return([node.endWordInfo[0], node.endWordInfo[1], numMatches])
            elif node.endWordInfo[2] >= node.bestWordInfo[0]:
                return([node.endWordInfo[0], node.endWordInfo[1], numMatches])
            elif node.endWordInfo[2] < node.bestWordInfo[0]:
                node = node.children[node.bestWordInfo[1]]
                
                
### DO NOT CHANGE THIS FUNCTION
def load_dictionary(filename):
    infile = open(filename)
    word, frequency = "", 0
    aList = []
    for line in infile:
        line.strip()
        if line[0:4] == "word":
            line = line.replace("word: ","")
            line = line.strip()
            word = line            
        elif line[0:4] == "freq":
            line = line.replace("frequency: ","")
            frequency = int(line)
        elif line[0:4] == "defi":
            index = len(aList)
            line = line.replace("definition: ","")
            definition = line.replace("\n","")
            aList.append([word,definition,frequency])

    return aList
    
if __name__ == "__main__":
    Dictionary = load_dictionary("Dictionary.txt")
    myTrie = Trie(Dictionary)

'''
Q2

todo:
erase network flow from my memory so i can sleep at night
'''
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

    