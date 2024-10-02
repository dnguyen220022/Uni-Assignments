#package handling
install.packages("tree")
install.packages("e1071")
install.packages("adabag")
install.packages("randomForest")
install.packages("ROCR")
install.packages("neuralnet")
library(tree)
library(e1071)
library(adabag)
library(rpart)
library(randomForest)
library(ROCR)
library(dplyr)
library(neuralnet)

#data setup
rm(list = ls())
Phish <- read.csv("PhishingData.csv")
set.seed(32471033) # Your Student ID is the random seed
L <- as.data.frame(c(1:50))
L <- L[sample(nrow(L), 10, replace = FALSE),]
Phish <- Phish[(Phish$A01 %in% L),]
PD <- Phish[sample(nrow(Phish), 2000, replace = FALSE),] # sample of 2000 rows

#q1
#get summaries
summary(PD)

#get standard deviations
sapply(PD, sd, na.rm = TRUE)

#q2
#convert Class to factors
PD$Class <- factor(PD$Class, levels = c(0, 1), labels = c(0, 1))

#q3
set.seed(32471033)
train.row = sample(1:nrow(PD), 0.7*nrow(PD))
PD.train = PD[train.row,]
PD.test = PD[-train.row,]

#q4
#decision tree
pdDT <- tree(Class~., data = PD.train)

plot(pdDT)
text(pdDT)

#naive bayes
pdNB <- naiveBayes(Class~., data = PD.train)

#bagging
#take sample with replacement
#see https://www.ibm.com/topics/bagging
set.seed(32471033)
sub <-c(sample(1:1400, 700, replace = TRUE))

#fit model
pdBag <- bagging(Class~., data = PD.train[sub,])

#boosting
pdBoost <- boosting(Class~., data = PD.train)

#random forest
pdRF <- randomForest(Class~., data = PD.train, na.action = na.exclude)

#q5
#decision tree
pdDTPredict <- predict(pdDT, PD.test, type = "class")

#confusion matrix
table(predicted = pdDTPredict, actual = PD.test$Class)

#naive bayes
pdNBPredict <- predict(pdNB, PD.test)

#confusion matrix
table(predicted = pdNBPredict, actual = PD.test$Class)

#bagging
pdBagPredict <- predict(pdBag, PD.test)

#confusion matrix
table(predicted = pdBagPredict$class, actual = PD.test$Class)

#boosting
pdBoostPredict = predict(pdBoost, PD.test)

#confusion matrix
table(predicted = pdBoostPredict$class, actual = PD.test$Class)

#random forest
pdRFPredict <- predict(pdRF, PD.test)

#confusion matrix
table(predicted = pdRFPredict, actual = PD.test$Class)

#q6
#get raw probability data
#decision tree
pdDTPredict <- predict(pdDT, PD.test)[,2] %>%
  ROCR::prediction(., PD.test$Class)
pdDTPerf <- performance(pdDTPredict, "tpr", "fpr")

#naive bayes
pdNBPredict <- predict(pdNB, PD.test, type = 'raw')[,2] %>%
  ROCR::prediction(., PD.test$Class)
pdNBPerf <- performance(pdNBPredict, "tpr", "fpr")

#bagging
pdBagPredict <- predict(pdBag, PD.test)$prob[,2] %>%
  ROCR::prediction(., PD.test$Class)
pdBagPerf <- performance(pdBagPredict, "tpr", "fpr")

#boosting
pdBoostPredict <- predict(pdBoost, PD.test)$prob[,2] %>%
  ROCR::prediction(., PD.test$Class)
pdBoostPerf <- performance(pdBoostPredict, "tpr", "fpr")

#random forest
pdRFPredict <- na.omit(predict(pdRF, PD.test, type = 'prob'))[,2] %>%
  ROCR::prediction(., na.omit(PD.test)$Class)
pdRFPerf <- performance(pdRFPredict, "tpr", "fpr")

#plot the graph
plot(pdDTPerf, main = "ROC Curve", col = "blue")
plot(pdNBPerf, col = "red", add = TRUE)
plot(pdBagPerf, col = "green", add = TRUE)
plot(pdBoostPerf, col = "pink", add = TRUE)
plot(pdRFPerf, col = "yellow", add = TRUE)
lines(c(0, 1), c(0, 1), col = "black", lty = 2)
legend("bottomright", legend = c("Decision Tree", "Naive Bayes", "Bagging", "Boosting", "Random Forest"), col = c("blue", "red", "green", "pink", "yellow"), lwd = 2)

#get areas under the curve
performance(pdDTPredict, "auc")@y.values
performance(pdNBPredict, "auc")@y.values
performance(pdBagPredict, "auc")@y.values
performance(pdBoostPredict, "auc")@y.values
performance(pdRFPredict, "auc")@y.values

#q8
#decision tree variable importance
#plot the decision tree and look at the variables
plot(pdDT)
text(pdDT, pretty = 0)

#bagging
pdBag$importance

#boosting
pdBoost$importance

#randomForest
pdRF$importance

#create new training and testing datasets after removing variables
excludedVars <- c("A03", "A05", "A07", "A09", "A10", "A11", "A13", "A21", "A25")

PD.train2 <- PD.train[, -which(names(PD.train) %in% excludedVars)]
PD.test2 <- PD.test[, -which(names(PD.test) %in% excludedVars)]

#create models
pdDT2 <- tree(Class~., data = PD.train2)

pdNB2 <- naiveBayes(Class~., data = PD.train2)

set.seed(32471033)
sub <-c(sample(1:1400, 700, replace = TRUE))
pdBag2 <- bagging(Class~., data = PD.train2[sub,])

pdBoost2 <- boosting(Class~., data = PD.train2)

pdRF2 <- randomForest(Class~., data = PD.train2, na.action = na.exclude)

#get new performance data
pdDTPredict2 <- predict(pdDT2, PD.test2)[,2] %>%
  ROCR::prediction(., PD.test2$Class)
pdDTPerf2 <- performance(pdDTPredict2, "tpr", "fpr")

pdNBPredict2 <- predict(pdNB2, PD.test2, type = 'raw')[,2] %>%
  ROCR::prediction(., PD.test2$Class)
pdNBPerf2 <- performance(pdNBPredict2, "tpr", "fpr")

pdBagPredict2 <- predict(pdBag2, PD.test2)$prob[,2] %>%
  ROCR::prediction(., PD.test2$Class)
pdBagPerf2 <- performance(pdBagPredict2, "tpr", "fpr")

pdBoostPredict2 <- predict(pdBoost2, PD.test2)$prob[,2] %>%
  ROCR::prediction(., PD.test2$Class)
pdBoostPerf2 <- performance(pdBoostPredict2, "tpr", "fpr")

pdRFPredict2 <- na.omit(predict(pdRF2, PD.test2, type = 'prob'))[,2] %>%
  ROCR::prediction(., na.omit(PD.test2)$Class)
pdRFPerf2 <- performance(pdRFPredict2, "tpr", "fpr")

#plot new ROC graph
plot(pdDTPerf2, main = "ROC Curve of New Classifier Versions", col = "blue")
plot(pdNBPerf2, col = "red", add = TRUE)
plot(pdBagPerf2, col = "green", add = TRUE)
plot(pdBoostPerf2, col = "pink", add = TRUE)
plot(pdRFPerf2, col = "yellow", add = TRUE)
lines(c(0, 1), c(0, 1), col = "black", lty = 2)
legend("bottomright", legend = c("Decision Tree", "Naive Bayes", "Bagging", "Boosting", "Random Forest"), col = c("blue", "red", "green", "pink", "yellow"), lwd = 2)

#get areas under the curve
performance(pdDTPredict2, "auc")@y.values
performance(pdNBPredict2, "auc")@y.values
performance(pdBagPredict2, "auc")@y.values
performance(pdBoostPredict2, "auc")@y.values
performance(pdRFPredict2, "auc")@y.values

#q9
#create train and test datasets
nbTrain <- PD.train[, c(1, 18, 22, 23, 26)]
nbTrain <- na.omit(nbTrain)
nbTest <- PD.test[, c(1, 18, 22, 23, 26)]
nbTest <- na.omit(nbTest)

#summary table to view median values
summary(nbTrain)

#splitting and factoring function
medianFactor <- function(x) {
  medianVal <- median(x)
  newCol <- ifelse(x < medianVal, 0, 1)
  newCol <- factor(newCol, levels = c(0, 1), labels = c("Below", "Above or Equal"))
  return(newCol)
}

#apply function to datasets
nbTrain[, c(1:4)] <- lapply(nbTrain[, c(1:4)], medianFactor)
nbTest[, c(1:4)] <- lapply(nbTest[, c(1:4)], medianFactor)

#fit model
pdNBSimple <- naiveBayes(Class~., data = nbTrain)

#model probability tables
pdNBSimple$tables

#model class distribution
pdNBSimple$apriori

#make predictions
pdNBSimplePredict <- predict(pdNBSimple, nbTest)

#confusion matrix
table(predicted = pdNBSimplePredict, actual = nbTest$Class)

#get AUC
pdNBSimplePrediction <- predict(pdNBSimple, nbTest, type = 'raw')[,2] %>%
  ROCR::prediction(., nbTest$Class)
performance(pdNBSimplePrediction, "auc")@y.values

#q10
#remove NA values
PD.trainOmit <- na.omit(PD.train)
PD.testOmit <- na.omit(PD.test)

PD.trainOmit <- PD.trainOmit[, c(1, 8, 12, 14, 17, 18, 22, 23, 24, 26)]
PD.testOmit <- PD.testOmit[, c(1, 8, 12, 14, 17, 18, 22, 23, 24, 26)]

#see if variables can be removed with cross validation
rfcv(PD.trainOmit[, -10], PD.trainOmit$Class, cv.fold=3, step=0.9)

#remove 2 least important variables
PD.trainOmit <- PD.trainOmit[, -c(4, 5)]
PD.testOmit <- PD.testOmit[, -c(4, 5)]

#get error by numtrees plot
set.seed(32471033)
pdTreeError <- randomForest(Class~., data = PD.trainOmit, ntree = 1000)

plot(pdTreeError)

#get best mtry val
set.seed(32471033)
tuneRF(PD.trainOmit[, -8], PD.trainOmit$Class, mtryStart = 2, ntreeTry = 300, stepFactor = 1.5, plot = TRUE, trace = TRUE, improve = 0.01)

#create model
set.seed(32471033)
pdBest <- randomForest(Class~., data = PD.trainOmit, ntree = 300, mtry = 2, sampsize = c('0' = 300, '1' = 160), replace = TRUE)

#get AUC
pdBestPredict <- predict(pdBest, PD.testOmit, type = 'prob')[,2] %>%
  ROCR::prediction(., PD.testOmit$Class)
pdBestPerf <- performance(pdBestPredict, "tpr", "fpr")
performance(pdBestPredict, "auc")@y.values

#plot ROC curve
plot(pdBestPerf, main = "ROC Curve of Best Classifier", col = "blue")

#confusion table
pdBestPredict <- predict(pdBest, PD.testOmit)
table(predicted = pdBestPredict, actual = PD.testOmit$Class)

#q11
#remove missing vals
nn.train <- na.omit(PD.train)
nn.test <- na.omit(PD.test)

#scale data while keeping real Class vals
nn.train <- as.data.frame(scale(nn.train[1:25]))
nn.train$Class <- (na.omit(PD.train))$Class

nn.test <- as.data.frame(scale(nn.test[1:25]))
nn.test$Class <- (na.omit(PD.test))$Class

#create neural network
set.seed(32471033)
pd.nn <- neuralnet(Class~A01 + A08 + A12 + A14 + A17 + A18 + A22 + A23 + A24, nn.train, hidden = c(6), stepmax = 1e+6, lifesign = "full")

#plot neural network
plot(pd.nn)

#prediction + prediction processing
nn.pred <- compute(pd.nn, nn.test)
nn.predr <- round(nn.pred$net.result[, 2], 0)
nn.predrdf <- as.data.frame(as.table(nn.predr))

#ROC processing
nnPredict <- nn.pred$net.result[, 2] %>%
  ROCR::prediction(., nn.test$Class)
nnPerf <- performance(nnPredict, "tpr", "fpr")

#plot ROC curve
plot(pdDTPerf, main = "ROC Curve", col = "blue")
plot(pdNBPerf, col = "red", add = TRUE)
plot(pdBagPerf, col = "green", add = TRUE)
plot(pdBoostPerf, col = "pink", add = TRUE)
plot(pdRFPerf, col = "yellow", add = TRUE)
plot(nnPerf, col = "purple", add = TRUE)
lines(c(0, 1), c(0, 1), col = "black", lty = 2)
legend("bottomright", legend = c("Decision Tree", "Naive Bayes", "Bagging", "Boosting", "Random Forest", "Neural Network"), col = c("blue", "red", "green", "pink", "yellow", "purple"), lwd = 2)

#get AUC
performance(nnPredict, "auc")@y.values

#confusion matrix
table(predicted = nn.predrdf$Freq, actual = nn.test$Class)

#q12
#support vector classification
#train model
svc <- svm(Class ~., data = PD.train, na.action = na.omit)

#get predictions
svcPred <- predict(svc, PD.test)

#confusion table
table(predicted = svcPred, actual = na.omit(PD.test)$Class)


