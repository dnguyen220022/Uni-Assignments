library(slam)
library(tm)
library(SnowballC)
library(igraph)
library(dendextend)
library(igraphdata)

rm(list = ls())

#create corpus
cname = file.path(".", "Documents")
docs = Corpus(DirSource((cname)))
summary(docs)

#text transformations
toJIT <- content_transformer(function(x, pattern) gsub(pattern, "JIT", x))
docs <- tm_map(docs, toJIT, "Just-In-Time")

toSpace <- content_transformer(function(x, pattern) gsub(pattern, " ", x))
docs <- tm_map(docs, toSpace, "-")

#tokenisation and stemming
#removePunctuation does not work well with typographical punctuation marks
#so i am using this to remove all non alphanumeric characters.
#i have kept newline char to preserve spaces between words on different lines
#https://stackoverflow.com/questions/30994194/quotes-and-hyphens-not-removed-by-tm-package-functions-while-cleaning-corpus
removeSpecialChars <- function(x) gsub("[^a-zA-Z0-9 \n]","",x)
docs <- tm_map(docs, removeSpecialChars)

docs <- tm_map(docs, removeNumbers)
docs <- tm_map(docs, content_transformer(tolower))
docs <- tm_map(docs, removeWords, stopwords("english"))
docs <- tm_map(docs, stripWhitespace)
docs <- tm_map(docs, stemDocument, language = "english")

#print ClimChange1
writeLines(as.character(docs[[1]]))

#create dtm
dtm <- DocumentTermMatrix(docs)

#print number of terms
freq <- colSums(as.matrix(dtm))
length(freq)
ord = order(freq)

#show most/least used terms
freq[head(ord)]
freq[tail(ord)]

#remove sparce terms
dtms <- removeSparseTerms(dtm, 0.7)

#perform Term frequency - Inverse Document Frequency to preserve important terms
tfidf <- weightTfIdf(dtms)
tfidf <- col_sums(as.matrix(tfidf))
finalTerms <- sort(tfidf, decreasing = TRUE)[1:20]

dtms <- dtms[, names(finalTerms)]

#show document term matrix dimensions
dim(dtms)

#convert to matrix
dtms <- as.matrix(dtms)

#write csv
write.csv(dtms, "dtms.csv")

#create distance matrix
distmatrix = proxy::dist(dtms, method = "cosine")

#fix plot margins
par(mar = c(10, 4, 4, 2))

#clustering and plot dendrogram
fit = hclust(distmatrix, method = "ward.D")
dendrogram <- as.dendrogram(fit)
plot(dendrogram, main = "Document Dendrogram")

#colour clusters and plot
dendrogramColour <- color_branches(dendrogram, k = 3)
plot(dendrogramColour, main = "Document Dendrogram Showing Clusters")

#analyse accuracy
topics = c("ClimChange","ClimChange","ClimChange", "ClimChange", "ClimChange", "Taiwan",
           "Taiwan", "Taiwan", "Taiwan", "Taiwan", "UFC", "UFC", "UFC", "UFC",
           "UFC")

groups = cutree(fit, k = 3)
TA = as.data.frame.matrix(table(GroupNames =topics, Clusters = groups))
TA = TA[,c(1, 2, 3)]
TA

##############################################################
# Accuracy = 93%
# calculated by correct classifications / number of documents
##############################################################

#create network data for single mode network for documents
dtmsx = dtms
dtmsx = as.matrix((dtmsx > 0) + 0)
ByDocMatrix = dtmsx %*% t(dtmsx)
diag(ByDocMatrix) = 0

#create and plot graph
ByDoc = graph_from_adjacency_matrix(ByDocMatrix,mode = "undirected", weighted = TRUE)
plot(ByDoc, main = "Single-Mode Document Network")

#get centrality
degree(ByDoc)

#community identification
set.seed(32471033)
cfb =  cluster_fast_greedy(ByDoc)
plot(cfb, ByDoc,vertex.label = V(ByDoc)$role, 
     main = "Fast-Greedy Algorithm Community Clustering")

###############################
#improved graph of documents
#shows communities
#shows strength of connections
###############################


ByDoc.sp <- ByDoc

#graph layout
l <- layout_in_circle(ByDoc.sp)

#get communities
set.seed(32471033)
cl <- cluster_spinglass(ByDoc.sp)

#normalise weight
normalise <- function(x) (x - min(x)) / (max(x) - min(x))
normalisedWeights <- normalise(E(ByDoc.sp)$weight)

#set edge colour based on weight
edgeColour <- colorRampPalette(c("black", "red"))
E(ByDoc.sp)$color <- edgeColour(100)[(cut(normalisedWeights, breaks = 100))]

#plot graph
plot(cl, ByDoc.sp, layout = l, edge.width = 2, edge.color = E(ByDoc.sp)$color, 
     main = "Communities and Connection Strengh in the Document Network")

#format legend
legendColours <- edgeColour(5)
legendWeights <- seq(min(E(ByDoc.sp)$weight), max(E(ByDoc.sp)$weight), length.out = 5)
legendLabels <- round(legendWeights, 1)

#add legend to graph
legend("topright", legend = legendLabels, col = legendColours, lwd = 3,
       title = "Edge Weight", bty = "n", cex = 1)

##############################################################################

#create network data for single mode network for tokens
dtmsx = dtms
dtmsx = as.matrix((dtmsx > 0) + 0)
byTokenMatrix = t(dtmsx) %*% dtmsx
diag(byTokenMatrix) = 0

#create and plot graph
byToken = graph_from_adjacency_matrix(byTokenMatrix,mode = "undirected", weighted = TRUE)
plot(byToken)

###############################
#improved graph of tokens
#shows communities
#shows strength of connections
###############################

#remove edges with low weight (below mean edge weight)
token.cut.off <- mean(E(byToken)$weight)
byToken.sp <- delete_edges(byToken, E(byToken)[weight<token.cut.off])

#graph layout
l <- layout_with_fr(byToken.sp)

#get communities
clp <- cluster_optimal(byToken.sp)

#normalise weight
normalise <- function(x) (x - min(x)) / (max(x) - min(x))
normalisedWeights <- normalise(E(byToken.sp)$weight)

#set edge colour based on weight
edgeColour <- colorRampPalette(c("black", "green"))
E(byToken.sp)$color <- edgeColour(100)[(cut(normalisedWeights, breaks = 100))]

#plot graph
plot(clp, byToken.sp, layout = l, vertex.size = 20, edge.width = 2, edge.color = E(byToken.sp)$color, 
     main = "Communities and Connection Strengh in the Token Network")

#format legend
legendColours <- edgeColour(5)
legendWeights <- seq(min(E(byToken.sp)$weight), max(E(byToken.sp)$weight), length.out = 5)
legendLabels <- round(legendWeights, 2)

#add legend to graph
legend("topright", legend = legendLabels, col = legendColours, lwd = 3,
       title = "Edge Weights", bty = "n", cex = 1)

###############################################

#2 mode graph
#code taken from lecture slides
dtmsa = as.data.frame(dtms)
dtmsa$ABS = rownames(dtmsa)
dtmsb = data.frame()
for (i in 1:nrow(dtmsa)){
  for (j in 1:(ncol(dtmsa)-1)){
    touse = cbind(dtmsa[i,j], dtmsa[i,ncol(dtmsa)],
                    colnames(dtmsa[j]))
    dtmsb = rbind(dtmsb, touse ) } }
colnames(dtmsb) = c("weight", "doc", "token")
dtmsc = dtmsb[dtmsb$weight != 0,]
dtmsc = dtmsc[,c(2,3,1)]

#plot graph
g <- graph.data.frame(dtmsc, directed=FALSE)
bipartite.mapping(g)
V(g)$type <- bipartite_mapping(g)$type
V(g)$color <- ifelse(V(g)$type, "lightgreen", "pink")
V(g)$shape <- ifelse(V(g)$type, "circle", "square")
E(g)$color <- "gray"

vertex.label <- V(g)$name

l <- layout_nicely(g)
plot(g, layout = l)

###############################
#improved graph of tokens
#shows communities
#shows strength of connections
###############################

#get data
g.sp <- g

#set margins
par(mar = c(3, 3, 3, 3))

#graph layout
l <- layout_with_graphopt(g.sp)

#get communities
set.seed(32471033)
clp <- cluster_spinglass(g.sp)

#normalise weight
normalise <- function(x) (x - min(x)) / (max(x) - min(x))
normalisedWeights <- normalise(as.numeric(E(g.sp)$weight))

#set edge colour based on weight
edgeColour <- colorRampPalette(c("red", "green"))
E(g.sp)$color <- edgeColour(100)[(cut(normalisedWeights, breaks = 100))]

#change size based on centrality
V(g.sp)$size <- degree(g.sp) * 1.75
V(g.sp)$label.cex <- degree(g.sp) * 0.2

#plot graph
V(g.sp)$label.color <- "black"
plot(clp, g.sp, layout = layout.auto, edge.width = 2, edge.color = E(g.sp)$color,
     main = "Communities and Connection Strength in 2 Mode Network with Node Size Corresponding to Centrality")

#format weight legend
legendColours <- edgeColour(5)
legendWeights <- seq(min(E(g.sp)$weight), max(E(g.sp)$weight), length.out = 5)
legendLabels <- round(legendWeights, 2)

#add legend
legend("topright", legend = legendLabels, col = legendColours, lwd = 3,
       title = "Edge Weights", bty = "n", cex = 1)

#format node colour legend
nodeCommunity <- unique(membership(clp))
nodeColour <- c("yellow", "skyblue", "darkgreen", "orange")

#add legend
legend("right", legend = paste("Community", nodeCommunity),
       col = nodeColour[nodeCommunity], pch = 19, pt.cex = 2, bty = "n")

#add node shape legend
legend("bottomright", legend = c("Document", "Token"),
       pch = c(0, 1), pt.cex = 2, bty = "n")

