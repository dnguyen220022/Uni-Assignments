library(ggplot2)
library(dplyr)
library(tidyr)
library(patchwork)
library(likert)
library(RColorBrewer)


########################################################
#data setup
########################################################

rm(list = ls())
set.seed(32471033) # XXXXXXXX = your student ID
cvbase = read.csv("PsyCoronaBaselineExtract.csv")
cvbase <- cvbase[sample(nrow(cvbase), 40000), ] # 40000 rows

########################################################
#1a
########################################################

#get num of rows and columns
dim(cvbase)

########################################################
#1b
########################################################

#filter out responses where all relevant questions are left blank
cvbase <- cvbase %>% 
  filter(rowSums(!is.na(select(., -coded_country))) > 0)

#convert all hours worked into 1 column
cvbase <- cvbase %>%
  transform(employstatus_hours = case_when
    (
      employstatus_1 == 1 ~ 1,
      employstatus_2 == 1 ~ 2,
      employstatus_3 == 1 ~ 3,
      TRUE ~ NA
    )
  )

cvbase <- cvbase %>%
  transform(employstatus_lookingForWork = case_when
    (
      employstatus_4 == 1 ~ 1,
      employstatus_5 == 1 ~ 0,
      TRUE ~ NA
    )
  )

#create new column for employed or unemployed
cvbase <- cvbase %>%
  transform(employstatus_employed = ifelse(is.na(employstatus_hours), 0, 1))

#add focus country indicator
cvbase <- cvbase %>%
  mutate(focusCountry = ifelse(coded_country == "Brazil", 1, 0))

########################################################
#2a
########################################################

#################
#Fig1
#################

#create new dataframe for employment percentage values
percentage_data_employment <- cvbase %>%
  group_by(focusCountry, employstatus_employed) %>%
  summarise(count = n()) %>%
  group_by(focusCountry) %>%
  mutate(total_count = sum(count)) %>%
  mutate(percentage = count / total_count * 100)

#Factor Variables for graph labelling
percentage_data_employment$employstatus_employed <- factor(percentage_data_employment$employstatus_employed, levels = c(0, 1), labels = c("Unemployed", "Employed"))

percentage_data_employment$focusCountry <- factor(percentage_data_employment$focusCountry, levels = c(0, 1), labels = c("Other Countries", "Brazil"))

# Create the dodged bar chart
ggplot(percentage_data_employment, aes(x = employstatus_employed, y = percentage, fill = focusCountry)) +
  
  geom_bar(position = position_dodge(width = 0.7), stat = "identity") +
  
  geom_text(aes(label = paste0(round(percentage), "%")), 
            position = position_dodge(width = 0.7), vjust = -0.5, size = 3.5, color = "black") +
  
  scale_fill_manual(values = c("Other Countries" = "blue", "Brazil" = "orange")) +
  
  labs(title = "Employment Status", x = "Employment Status", y = "Percentage", fill = "Legend") +
  
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5))

#################
#Fig2
#################

#create new dataframe for hours worked percentage values
percentage_data_hours <- cvbase %>%
  group_by(focusCountry, employstatus_hours) %>%
  summarise(count = n()) %>%
  group_by(focusCountry)
  percentage_data_hours <- na.omit(percentage_data_hours) %>%
  mutate(total_count = sum(count)) %>%
  mutate(percentage = count / total_count * 100)

#Factor Variables for graph labelling
percentage_data_hours$employstatus_hours <- factor(percentage_data_hours$employstatus_hours, levels = c(1, 2, 3), labels = c("1-24", "24-39", "40+"))
  
percentage_data_hours$focusCountry <- factor(percentage_data_hours$focusCountry, levels = c(0, 1), labels = c("Other Countries", "Brazil"))

# Create dodged bar chart  
ggplot(percentage_data_hours, aes(x = employstatus_hours, y = percentage, fill = focusCountry)) +
    
  geom_bar(position = position_dodge(width = 0.7), stat = "identity") +
    
  geom_text(aes(label = paste0(round(percentage), "%")), 
            position = position_dodge(width = 0.7), vjust = -0.5, size = 3.5, color = "black") +
    
  scale_fill_manual(values = c("Other Countries" = "blue", "Brazil" = "orange")) +
    
  labs(title = "Hours Worked", x = "Hours Worked", y = "Percentage", fill = "Legend") +
    
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5))

#################
#Fig3
#################

#create new dataframe for looking for work percentage values
percentage_lookingForWork <- cvbase %>%
  group_by(focusCountry, employstatus_lookingForWork) %>%
  summarise(count = n()) %>%
  group_by(focusCountry)
percentage_lookingForWork <- na.omit(percentage_lookingForWork) %>%
  mutate(total_count = sum(count)) %>%
  mutate(percentage = count / total_count * 100)

#Factor Variables for graph labelling
percentage_lookingForWork$employstatus_lookingForWork <- factor(percentage_lookingForWork$employstatus_lookingForWork, levels = c(0, 1), labels = c("Not Looking For Work", "Looking For Work"))

percentage_lookingForWork$focusCountry <- factor(percentage_lookingForWork$focusCountry, levels = c(0, 1), labels = c("Other Countries", "Brazil"))

#create dodged bar chart
ggplot(percentage_lookingForWork, aes(x = employstatus_lookingForWork, y = percentage, fill = focusCountry)) +
  
  geom_bar(position = position_dodge(width = 0.7), stat = "identity") +
  
  geom_text(aes(label = paste0(round(percentage), "%")), 
            position = position_dodge(width = 0.7), vjust = -0.5, size = 3.5, color = "black") +
  
  scale_fill_manual(values = c("Other Countries" = "blue", "Brazil" = "orange")) +
  
  labs(title = "Proportion of Unemployed People Looking for Work", x = "", y = "Percentage", fill = "Legend") +
  
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5))

#################
#Fig4
#################

#Create new dataframe for the rest of employstatus attributes
percentage_employstatusRest <- cvbase %>%
  group_by(focusCountry) %>%
  summarise(               
    employstatus_6 = sum(employstatus_6 == 1, na.rm = TRUE),
    employstatus_7 = sum(employstatus_7 == 1, na.rm = TRUE),
    employstatus_8 = sum(employstatus_8 == 1, na.rm = TRUE),
    employstatus_9 = sum(employstatus_9 == 1, na.rm = TRUE),
    employstatus_10 = sum(employstatus_10 == 1, na.rm = TRUE),
    total_count = sum(focusCountry %in% c(0, 1), na.rm = TRUE),  # Calculate total count for country 0 or 1
  )

#convert to long format
percentage_employstatusRest <- percentage_employstatusRest %>%
  pivot_longer(cols = starts_with("employstatus_"), 
               names_to = "employment_status", 
               values_to = "count")

#calculate percentages
percentage_employstatusRest <- percentage_employstatusRest %>%
  mutate(percentage = count / total_count * 100)

#Rename column factors for labelling purposes
percentage_employstatusRest <- percentage_employstatusRest %>%
  mutate(employment_status = case_when(
    employment_status == "employstatus_6" ~ "Homemaker",
    employment_status == "employstatus_7" ~ "Retired",
    employment_status == "employstatus_8" ~ "Disabled, Unable to work",
    employment_status == "employstatus_9" ~ "Student",
    employment_status == "employstatus_10" ~ "Volunteering"
  ))

#factor data for labelling purposes
percentage_employstatusRest$focusCountry <- factor(percentage_employstatusRest$focusCountry, levels = c(0, 1), labels = c("Other Countries", "Brazil"))

# Plot the dodged bar chart
ggplot(percentage_employstatusRest, aes(x = employment_status, y = percentage, fill = focusCountry)) +
  
  geom_bar(position = position_dodge(width = 0.7), stat = "identity") +
  
  geom_text(aes(label = paste0(round(percentage), "%")), 
            position = position_dodge(width = 0.7), vjust = -0.5, size = 3.5, color = "black") +
  
  scale_fill_manual(values = c("Other Countries" = "blue", "Brazil" = "orange")) +
  
  labs(title = "Percentage of People Identifying as Below", x = "", y = "Percentage", fill = "Legend") +
  
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5))

#################
#Fig5
#################

#create new dataframe for isoFriends_inPerson
isoFriends_inPerson <- cvbase[, c("isoFriends_inPerson", "focusCountry")]

#remove NA values
isoFriends_inPerson <- na.omit(isoFriends_inPerson)

#factor data for labelling
isoFriends_inPerson$focusCountry <- factor(isoFriends_inPerson$focusCountry, levels = c(0, 1), labels = c("Other Countries", "Brazil"))

#draw graph 1
isoPlot1 <- ggplot(isoFriends_inPerson, aes(x = factor(focusCountry), fill = factor(isoFriends_inPerson))) +
  geom_bar(position = "fill") +
  scale_fill_brewer(palette = "GnBu") +
  labs(title = "In Person Contact with Friends and Family in the Past Week", x = "Country", y = "Proportion", fill = "Days of Contact") +
  theme_minimal()

#create new dataframe for isoOthPpl_inPerson
isoOthPpl_inPerson <- cvbase[, c("isoOthPpl_inPerson", "focusCountry")]

#remove NA values
isoOthPpl_inPerson <- na.omit(isoOthPpl_inPerson)

#factor data for labelling
isoOthPpl_inPerson$focusCountry <- factor(isoOthPpl_inPerson$focusCountry, levels = c(0, 1), labels = c("Other Countries", "Brazil"))

#draw graph 2
isoPlot2 <- ggplot(isoOthPpl_inPerson, aes(x = factor(focusCountry), fill = factor(isoOthPpl_inPerson))) +
  geom_bar(position = "fill") +
  scale_fill_brewer(palette = "GnBu") +
  labs(title = "In Person Contact with Other People in the Past Week", x = "Country", y = "Proportion", fill = "Days of Contact") +
  theme_minimal()

#create new dataframe for isoFriends_Online
isoFriends_online <- cvbase[, c("isoFriends_online", "focusCountry")]

#remove NA values
isoFriends_online <- na.omit(isoFriends_online)

#factor data for labelling
isoFriends_online$focusCountry <- factor(isoFriends_online$focusCountry, levels = c(0, 1), labels = c("Other Countries", "Brazil"))

#draw graph 3
isoPlot3 <- ggplot(isoFriends_online, aes(x = factor(focusCountry), fill = factor(isoFriends_online))) +
  geom_bar(position = "fill") +
  scale_fill_brewer(palette = "GnBu") +
  labs(title = "Online Contact with Friends and Family in the Past Week", x = "Country", y = "Proportion", fill = "Days of Contact") +
  theme_minimal()

#create new dataframe for isoOthPpl_Online
isoOthPpl_online <- cvbase[, c("isoOthPpl_online", "focusCountry")]

#remove NA values
isoOthPpl_online <- na.omit(isoOthPpl_online)

#factor data for labelling
isoOthPpl_online$focusCountry <- factor(isoOthPpl_online$focusCountry, levels = c(0, 1), labels = c("Other Countries", "Brazil"))

#draw graph 4
isoPlot4 <- ggplot(isoOthPpl_online, aes(x = factor(focusCountry), fill = factor(isoOthPpl_online))) +
  geom_bar(position = "fill") +
  scale_fill_brewer(palette = "GnBu") +
  labs(title = "Online Contact with Other People in the Past Week", x = "Country", y = "Proportion", fill = "Days of Contact") +
  theme_minimal()

#combine plots using patchwork library

isoPlot1 + 
isoPlot2 +
isoPlot3 +
isoPlot4

#################
#Fig6
#################

#NOTES
#Refer to https://stackoverflow.com/questions/27061286/likert-grouping-with-different-levels-in-r
#for future likert plotting
#extremely helpful

#create dataframe for loneliness
lone_data <- cvbase[, c("focusCountry", "lone01", "lone02", "lone03")]

#apply factor function to all question responses to give response levels
lone_data[2:4] <- lapply(lone_data[2:4], factor, levels = 1:5, labels = c("Never", "Rarely", "Sometimes", "Often", "All the Time"))

#factor focusCountry to get label names
lone_data$focusCountry <- factor(lone_data$focusCountry, levels = c(0, 1), labels = c("Other Countries", "Brazil"))

#rename question columns to represent the question text
lone_data <- lone_data %>%
  rename("During the past week, did you feel lonely?" = lone01,
        "During the past week, did you feel isolated from others?" = lone02,
        "During the past week, did you feel left out?" = lone03
    )

#convert responses to a likert object, and group by focus country
lone_likert <- likert(lone_data[, c(2:4)], grouping = lone_data$focusCountry)

#plot the graph
plot(lone_likert)

################# 
#Fig7
#################

#create dataframe for happy

happy_data <- cvbase[, c("focusCountry", "happy")]
happy_data <- na.omit(happy_data)

#factor for labelling
happy_data$focusCountry <- factor(happy_data$focusCountry, levels = c(0, 1), labels = c("Other Countries", "Brazil"))

#create and store boxplot
happy_plot <- ggplot(happy_data, aes(x = focusCountry, y = happy, fill = focusCountry)) +
  
  geom_boxplot() +
  
  scale_y_continuous(breaks = seq(0, 10, by = 1)) +
  
  scale_fill_manual(values = c("Other Countries" = "lightblue", "Brazil" = "orange")) +
  
  labs(title = "Rate your Happiness from 1 (Extremely Unhappy) to 10 (Extremely Happy)", x = "Country", y = "Rating", fill = "Legend") +
  
  theme_minimal()

#create dataframe for lifeSat
lifeSat_data <- cvbase[, c("focusCountry", "lifeSat")]
lifeSat_data <- na.omit(lifeSat_data)

#assign levels to response values
lifeSat_data[2] <- lapply(lifeSat_data[2], factor, levels = 1:6, labels = c("Very Dissatisfied", "Dissatisfied", "Slightly Dissatisfied", "Slightly Satisfied", "Satisfied", "Very Satisfied"))

#factor to assign labels to focusCountry
lifeSat_data$focusCountry <- factor(lifeSat_data$focusCountry, levels = c(0, 1), labels = c("Other Countries", "Brazil"))

#rename question column to represent the actual question
lifeSat_data <- lifeSat_data %>%
  rename("In general, how satisfied are you with your life?" = lifeSat
    )

#convert to likert object
lifeSat_likert <- likert(items=lifeSat_data[,2, drop=FALSE], grouping = lifeSat_data$focusCountry)

#Store the plot
lifeSat_plot <- plot(lifeSat_likert)

#create dataframe for MLQ
mlq_data <- cvbase[, c("focusCountry", "MLQ")]
mlq_data <- na.omit(mlq_data)

#convert values from -3:3 to 1:7 because idk how to assign levels to negative numbers
mlq_data <- mlq_data %>%
  mutate(
    MLQ = MLQ + 4
    )

#assign levels to response values
mlq_data[2] <- lapply(mlq_data[2], factor, levels = 1:7, 
            labels = c("Strongly Disagree", "Disagree", "Somewhat Disagree", "Neither Agree nor Disagree", "Somewhat Agree", "Agree", "Strongly Agree")
                    )

#assign labels to focusCountry
mlq_data$focusCountry <- factor(mlq_data$focusCountry, levels = c(0, 1), labels = c("Other Countries", "Brazil"))

#rename question name
mlq_data <- mlq_data %>%
  rename("My life has a clear sense of purpose" = MLQ
  )

#convert to likert object
mlq_likert <- likert(items=mlq_data[,2, drop=FALSE], grouping = mlq_data$focusCountry)

mlq_plot <- plot(mlq_likert)

#combine plots
happy_plot + lifeSat_plot / mlq_plot

################# 
#Fig8
#################

#create dataframe for boredom
bor_data <- cvbase[, c("focusCountry", "bor01", "bor02", "bor03")]

#convert from -3:3 to 1:7
bor_data <- bor_data %>%
  mutate(
    bor01 = bor01 + 4,
    bor02 = bor02 + 4,
    bor03 = bor03 + 4
  )

#assign levels to response values
bor_data[2:4] <- lapply(bor_data[2:4], factor, levels = 1:7, 
                      labels = c("Strongly Disagree", "Disagree", "Somewhat Disagree", "Neither Agree nor Disagree", "Somewhat Agree", "Agree", "Strongly Agree")
)

#factor focusCountry to get label names
bor_data$focusCountry <- factor(bor_data$focusCountry, levels = c(0, 1), labels = c("Other Countries", "Brazil"))

#rename question columns to represent the question text
bor_data <- bor_data %>%
  rename("I Wish Time Would Go Faster" = bor01,
         "Time is Moving Very Slowly" = bor02,
         "I Feel in Control of My Time" = bor03
  )

#convert responses to a likert object, and group by focus country
bor_likert <- likert(bor_data[, c(2:4)], grouping = bor_data$focusCountry)

#plot the graph
plot(bor_likert)

################# 
#Fig9
#################

#create dataframe for Conspiracy
consp_data <- cvbase[, c("focusCountry", "consp01", "consp02", "consp03")]

#assign levels to response values
consp_data[2:4] <- lapply(consp_data[2:4], factor, levels = 0:10, 
  labels = c("Certainly Not", "10%", "20%", "30%", "40%", "Undecided", "60%", "70%", "80%", "90%", "Certainly")
)

#factor focusCountry to get label names
consp_data$focusCountry <- factor(consp_data$focusCountry, levels = c(0, 1), labels = c("Other Countries", "Brazil"))

#rename question columns to represent the question text
consp_data <- consp_data %>%
  rename("think that many very important things happen in the world, which the public is never informed about" = consp01,
         "I think that politicians usually do not tell us the true motives for their decisions" = consp02,
         "I think that government agencies closely monitor all citizens." = consp03
  )

#convert responses to a likert object, and group by focus country
consp_likert <- likert(consp_data[, c(2:4)], grouping = consp_data$focusCountry)

#plot the graph
plot(consp_likert)

################# 
#Fig10
#################

#create dataframe for rankOrdLife
rankOrd_data <- cvbase[, c("focusCountry", "rankOrdLife_1", "rankOrdLife_2", "rankOrdLife_3", "rankOrdLife_4", "rankOrdLife_5", "rankOrdLife_6")]

#pivot table
rankOrd_data <- rankOrd_data %>%
  pivot_longer(cols = starts_with("rankOrdLife"), names_to = "rank", values_to = "category")

#omit NA vals
rankOrd_data <- na.omit(rankOrd_data)

#rename row values to numerical ranking
rankOrd_data <- rankOrd_data %>%
  mutate(rank = case_when(
    rank == "rankOrdLife_1" ~ 1,
    rank == "rankOrdLife_2" ~ 2,
    rank == "rankOrdLife_3" ~ 3,
    rank == "rankOrdLife_4" ~ 4,
    rank == "rankOrdLife_5" ~ 5,
    rank == "rankOrdLife_6" ~ 6
  ))

#rename row values to categories
rankOrd_data <- rankOrd_data %>%
  mutate(category = case_when(
    category == "A" ~ "Beauty",
    category == "B" ~ "Achievement",
    category == "C" ~ "Victory",
    category == "D" ~ "Friendship",
    category == "E" ~ "Love",
    category == "F" ~ "Empathy"
  ))

#label country
rankOrd_data$focusCountry <- factor(rankOrd_data$focusCountry, levels = c(0, 1), labels = c("Other Countries", "Brazil"))

#draw boxplot
ggplot(rankOrd_data, aes(x=category, y=rank, fill=focusCountry)) + 
  
  geom_boxplot() +
  scale_fill_manual(values = c("Other Countries" = "lightblue", "Brazil" = "orange")) +
  scale_y_continuous(trans = "reverse", breaks = unique(rankOrd_data$rank)) +
  labs(title = "Rank the Following in Order From 1 (Most Important) to 6 (Least Important)", x = "Category", y = "Rank", fill = "Legend") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5))

################# 
#Fig11
#################

#create dataframe for c19perBeh and c19RCA
c19Resp_data <- cvbase[, c("focusCountry", "c19perBeh01", "c19perBeh02", "c19perBeh03", "c19RCA01", "c19RCA02", "c19RCA03")]

#convert from -3:3 to 1:7
c19Resp_data <- c19Resp_data %>%
  mutate(
    c19perBeh01 = c19perBeh01 + 4,
    c19perBeh02 = c19perBeh02 + 4,
    c19perBeh03 = c19perBeh03 + 4,
    c19RCA01 = c19RCA01 + 4,
    c19RCA02 = c19RCA02 + 4,
    c19RCA03 = c19RCA03 + 4
  )

#assign levels to response values
c19Resp_data[2:7] <- lapply(c19Resp_data[2:7], factor, levels = 1:7, 
                        labels = c("Strongly Disagree", "Disagree", "Somewhat Disagree", "Neither Agree nor Disagree", "Somewhat Agree", "Agree", "Strongly Agree")
)

#factor focusCountry to get label names
c19Resp_data$focusCountry <- factor(c19Resp_data$focusCountry, levels = c(0, 1), labels = c("Other Countries", "Brazil"))

#rename question columns to represent the question text
c19Resp_data <- c19Resp_data %>% 
  rename("To minimize my chances of getting coronavirus, I wash my hands more often" = c19perBeh01,
         "To minimize my chances of getting coronavirus, I avoid crowded spaces" = c19perBeh02,
         "To minimize my chances of getting coronavirus, I put myself in quarantine" = c19perBeh03,
         "I would sign a petition that supports mandatory vaccination once a vaccine has been developed for coronavirus." = c19RCA01,
         "I would sign a petition that supports mandatory quarantine for those that have coronavirus and those that have been exposed to the virus." = c19RCA02,
         "I would sign a petition that supports reporting people who are suspected to have coronavirus." = c19RCA03
  )

#convert responses to a likert object, and group by focus country
c19Resp_likert <- likert(c19Resp_data[, c(2:7)], grouping = c19Resp_data$focusCountry)

#plot the graph
plot(c19Resp_likert)

################# 
#Fig12
#################

#Create new dataframe for coronaClose
percentage_coronaClose <- cvbase %>%
  group_by(focusCountry) %>%
  summarise(               
    coronaClose_1 = sum(coronaClose_1 == 1, na.rm = TRUE),
    coronaClose_2 = sum(coronaClose_2 == 1, na.rm = TRUE),
    coronaClose_3 = sum(coronaClose_3 == 1, na.rm = TRUE),
    coronaClose_4 = sum(coronaClose_4 == 1, na.rm = TRUE),
    coronaClose_5 = sum(coronaClose_5 == 1, na.rm = TRUE),
    coronaClose_6 = sum(coronaClose_6 == 1, na.rm = TRUE),
    total_count = sum(focusCountry %in% c(0, 1), na.rm = TRUE),  # Calculate total count for country 0 or 1
  )

#convert to long format
percentage_coronaClose <- percentage_coronaClose %>%
  pivot_longer(cols = starts_with("coronaClose_"), 
               names_to = "coronaClose", 
               values_to = "count")

#calculate percentages
percentage_coronaClose <- percentage_coronaClose %>%
  mutate(percentage = count / total_count * 100)

#Rename column factors for labelling purposes
percentage_coronaClose <- percentage_coronaClose %>%
  mutate(coronaClose = case_when(
    coronaClose == "coronaClose_1" ~ "Yes, Myself",
    coronaClose == "coronaClose_2" ~ "Yes, a member of my family",
    coronaClose == "coronaClose_3" ~ "Yes, a close friend",
    coronaClose == "coronaClose_4" ~ "Yes, someone I know",
    coronaClose == "coronaClose_5" ~ "Yes, someone else",
    coronaClose == "coronaClose_6" ~ "No, I do not know anyone"
  ))

percentage_coronaClose$focusCountry <- factor(percentage_coronaClose$focusCountry, levels = c(0, 1), labels = c("Other Countries", "Brazil"))

# Plot the dodged bar chart
ggplot(percentage_coronaClose, aes(x = coronaClose, y = percentage, fill = focusCountry)) +
  
  geom_bar(position = position_dodge(width = 0.7), stat = "identity") +
  geom_text(aes(label = paste0(round(percentage), "%")), 
            position = position_dodge(width = 0.7), vjust = -0.5, size = 3.5, color = "black") +

  scale_fill_manual(values = c("Other Countries" = "blue", "Brazil" = "orange")) +
  labs(title = "Do you personally know anyone who currently has coronavirus?", x = "", y = "Percentage", fill = "Legend") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5))

################# 
#Fig13
#################

#create dataframe for gender
gender_data <- cvbase[, c("focusCountry", "gender")]

#remove NA values
gender_data <- na.omit(gender_data)

#factor data for labelling
gender_data$focusCountry <- factor(gender_data$focusCountry, levels = c(0, 1), labels = c("Other Countries", "Brazil"))

gender_data$gender <- factor(gender_data$gender, levels = (1:3), labels = c("Female", "Male", "Other"))

#draw stacked bar chart
ggplot(gender_data, aes(x = factor(focusCountry), fill = factor(gender))) +
  geom_bar(position = "fill") +
  scale_fill_brewer(palette = "RdYlBu") +
  labs(title = "Gender of Participant", x = "Country", y = "Proportion", fill = "Gender") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5))

################# 
#Fig14
#################

#create dataframe for age
age_data <- cvbase[, c("focusCountry", "age")]

#remove NA values
age_data <- na.omit(age_data)

#factor focusCountry for labelling
age_data$focusCountry <- factor(age_data$focusCountry, levels = c(0, 1), labels = c("Other Countries", "Brazil"))

#factor age values for labelling
age_data$age <- factor(age_data$age, levels = (1:8), labels = c("18-24", "25-34", "35-44", "45-54", "55-64", "65-75", "75-85", "85+"))

#draw graph 4
ggplot(age_data, aes(x = factor(focusCountry), fill = factor(age))) +
  geom_bar(position = "fill") +
  scale_fill_brewer(palette = "GnBu") +
  labs(title = "Age of Participants", x = "Country", y = "Proportion", fill = "Age") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5))

################# 
#Fig15
#################

#create dataframe for education level
edu_data <- cvbase[, c("focusCountry", "edu")]

#remove NA values
edu_data <- na.omit(edu_data)

#factor focusCountry for labelling
edu_data$focusCountry <- factor(edu_data$focusCountry, levels = c(0, 1), labels = c("Other Countries", "Brazil"))

#factor age values for labelling
edu_data$edu <- factor(edu_data$edu, levels = (1:7), 
    labels = c("Primary Education", "General Secondary Education", "Vocational Education", "Higher Education", "Bachelors Degree", "Masters Degree", "PhD Degree"))

#draw graph 4
ggplot(edu_data, aes(x = factor(focusCountry), fill = factor(edu))) +
  geom_bar(position = "fill") +
  scale_fill_brewer(palette = "GnBu") +
  labs(title = "Education Level of Participants", x = "Country", y = "Proportion", fill = "Education Level") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5))

################# 
#Fig16
#################

#create dataframe for country data
country_data <- cvbase %>%
  summarise(               
    "Other Countries" = sum(focusCountry == 0, na.rm = TRUE),
    "Brazil" = sum(focusCountry == 1, na.rm = TRUE),
  )

#pivot to longer, and add percentage column
country_data <- country_data %>%
  pivot_longer(everything(), names_to = "focusCountry", values_to = "count") %>%
  mutate(
    percentage = count / sum(count) * 100
  )

#create plot
ggplot(country_data, aes(x = "", y = percentage, fill = focusCountry)) +
  geom_bar(stat = "identity") +
  coord_flip() +
  geom_text(aes(label = paste0(round(percentage), "%")),
            position = position_stack(vjust = 0.5), size = 4, color = "black") +
  scale_fill_manual(values = c("Brazil" = "#f4a582", "Other Countries" = "#92c5de")) +
  labs(title = "Country of Residence",
       x = NULL, y = "Percentage", fill = "Country") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5))

################# 
#Fig17
#################

#create dataframe for c19ProSo
c19ProSo_data <- cvbase[, c("focusCountry", "c19ProSo01", "c19ProSo02", "c19ProSo03", "c19ProSo04")]

#convert from -3:3 to 1:7
c19ProSo_data <- c19ProSo_data %>%
  mutate(
    c19ProSo01 = c19ProSo01 + 4,
    c19ProSo02 = c19ProSo02 + 4,
    c19ProSo03 = c19ProSo03 + 4,
    c19ProSo04 = c19ProSo04 + 4
  )

#assign levels to response values
c19ProSo_data[2:5] <- lapply(c19ProSo_data[2:5], factor, levels = 1:7, 
                        labels = c("Strongly Disagree", "Disagree", "Somewhat Disagree", "Neither Agree nor Disagree", "Somewhat Agree", "Agree", "Strongly Agree")
)

#factor focusCountry to get label names
c19ProSo_data$focusCountry <- factor(c19ProSo_data$focusCountry, levels = c(0, 1), labels = c("Other Countries", "Brazil"))

#rename question columns to represent the question text
c19ProSo_data <- c19ProSo_data %>%
  rename("I am willing to help others who suffer from coronavirus." = c19ProSo01,
         "I am willing to make donations to help others that suffer from coronavirus." = c19ProSo02,
         "I am willing to protect vulnerable groups from coronavirus even at my own expense." = c19ProSo03,
         "I am willing to make personal sacrifices to prevent the spread of coronavirus." = c19ProSo04,
  )

#convert responses to a likert object, and group by focus country
c19ProSo_likert <- likert(c19ProSo_data[, c(2:5)], grouping = c19ProSo_data$focusCountry)

#plot the graph
plot(c19ProSo_likert)

########################################################
#2b and 2c
########################################################

#assign dataframe
regression_data <- cvbase

#change na vals to 0 for dummy vars
regression_data[, c(1:10, 39:44)][is.na(regression_data[, c(1:10, 39:44)])] <- 0

#convert scales that include neg vals to positive only
regression_data <- regression_data %>%
  mutate(
    c19ProSo01 = c19ProSo01 + 4,
    c19ProSo02 = c19ProSo02 + 4,
    c19ProSo03 = c19ProSo03 + 4,
    c19ProSo04 = c19ProSo04 + 4,
    c19perBeh01 = c19perBeh01 + 4,
    c19perBeh02 = c19perBeh02 + 4,
    c19perBeh03 = c19perBeh03 + 4,
    c19RCA01 = c19RCA01 + 4,
    c19RCA02 = c19RCA02 + 4,
    c19RCA03 = c19RCA03 + 4,
    bor01 = bor01 + 4,
    bor02 = bor02 + 4,
    bor03 = bor03 + 4,
    MLQ = MLQ + 4
  )

#convert rankOrd to be in terms of category, rather than rank
regression_processing <- regression_data %>%
  mutate(rowNum = row_number()) %>%
  pivot_longer(
    cols = starts_with("rankOrdLife"), 
    names_to = "rank", 
    values_to = "category"
  )

#NA out rankOrd responses where multiple categories have the same rank (idk how this would even occur given the nature of the question)
#look at rowNum == 141 for example
regression_processing <- regression_processing %>%
  group_by(rowNum) %>%
  mutate(category = if (!any(is.na(category)) && length(unique(category)) < 6) NA else category = category) %>%
  ungroup()

#rename column text values to be numerical
regression_processing <- regression_processing %>%
  mutate(rank = case_when(
    rank == "rankOrdLife_1" ~ 1,
    rank == "rankOrdLife_2" ~ 2,
    rank == "rankOrdLife_3" ~ 3,
    rank == "rankOrdLife_4" ~ 4,
    rank == "rankOrdLife_5" ~ 5,
    rank == "rankOrdLife_6" ~ 6
  ))

#pivot back to wide format to return to correct num of rows
regression_processing <- regression_processing %>%
  pivot_wider(
    id_cols = rowNum,
    names_from = category,
    values_from = rank,
    names_prefix = "rank_"
  )

#remove NA ranking column and rowNum column
regression_processing <- regression_processing %>%
  select(-c(rowNum, rank_NA))

#when pivoting back to wide format, list columns were created, due to the NA values
#we will have to convert the list columns back into regular columns to make any more changes
regression_processing <- unnest_longer(regression_processing, col = c(rank_C, rank_E, rank_F, rank_D, rank_A, rank_B), keep_empty = TRUE)

#Replace NULL (No Value) with NA(Missing Value)
regression_processing <- replace(regression_processing, is.null(regression_processing), NA)

#Bind table to retrieve all other data
regression_processing <- regression_data %>%
  select(-starts_with("Rank")) %>%
  bind_cols(regression_processing)

#assign clean and tidy data to regression_data
regression_data <- regression_processing

#Extract data from focus country (Brazil) only
brazil_data <- regression_data[regression_data$focusCountry == 1, ]

#Extract data from other countries only
otherCountry_data <- regression_data[regression_data$focusCountry == 0, ]

#one-hot encode gender data
otherCountry_data <- otherCountry_data %>%
  transform(female = case_when
            (
              gender == 1 ~ 1,
              TRUE ~ 0
            )
  ) %>%
  transform(male = case_when
            (
              gender == 2 ~ 1,
              TRUE ~ 0
            )
  ) %>%
  transform(other = case_when
            (
              gender == 3 ~ 1,
              TRUE ~ 0
            )
  )
##########################
#Regressions
##########################

#regression for Brazil proso01
brazil_c19ProSo01 = lm(c19ProSo01 ~
                        employstatus_1 +
                        employstatus_2 +
                        employstatus_3 +
                        employstatus_4 +
                        employstatus_5 +
                        employstatus_6 +
                        employstatus_7 +
                        employstatus_8 +
                        employstatus_9 +
                        employstatus_10 +
                        isoFriends_inPerson +
                        isoOthPpl_inPerson +
                        isoFriends_online +
                        isoOthPpl_online +
                        lone01 +
                        lone02 +
                        lone03 +
                        happy +
                        lifeSat +
                        MLQ +
                        bor01 +
                        bor02 +
                        bor03 +
                        consp01 +
                        consp02 +
                        consp03 +
                        rank_A +
                        rank_B +
                        rank_C +
                        rank_D +
                        rank_E +
                        rank_F +
                        c19perBeh01 +
                        c19perBeh02 +
                        c19perBeh03 +
                        c19RCA01 +
                        c19RCA02 +
                        c19RCA03 +
                        coronaClose_1 +
                        coronaClose_2 +
                        coronaClose_3 +
                        coronaClose_4 +
                        coronaClose_5 +
                        coronaClose_6 +
                        gender +
                        age +
                        edu,
                        data = brazil_data)

#regression for Brazil proso02
brazil_c19ProSo02 = lm(c19ProSo02 ~
                         employstatus_1 +
                         employstatus_2 +
                         employstatus_3 +
                         employstatus_4 +
                         employstatus_5 +
                         employstatus_6 +
                         employstatus_7 +
                         employstatus_8 +
                         employstatus_9 +
                         employstatus_10 +
                         isoFriends_inPerson +
                         isoOthPpl_inPerson +
                         isoFriends_online +
                         isoOthPpl_online +
                         lone01 +
                         lone02 +
                         lone03 +
                         happy +
                         lifeSat +
                         MLQ +
                         bor01 +
                         bor02 +
                         bor03 +
                         consp01 +
                         consp02 +
                         consp03 +
                         rank_A +
                         rank_B +
                         rank_C +
                         rank_D +
                         rank_E +
                         rank_F +
                         c19perBeh01 +
                         c19perBeh02 +
                         c19perBeh03 +
                         c19RCA01 +
                         c19RCA02 +
                         c19RCA03 +
                         coronaClose_1 +
                         coronaClose_2 +
                         coronaClose_3 +
                         coronaClose_4 +
                         coronaClose_5 +
                         coronaClose_6 +
                         gender +
                         age +
                         edu,
                       data = brazil_data)

#regression for Brazil proso03
brazil_c19ProSo03 = lm(c19ProSo03 ~
                         employstatus_1 +
                         employstatus_2 +
                         employstatus_3 +
                         employstatus_4 +
                         employstatus_5 +
                         employstatus_6 +
                         employstatus_7 +
                         employstatus_8 +
                         employstatus_9 +
                         employstatus_10 +
                         isoFriends_inPerson +
                         isoOthPpl_inPerson +
                         isoFriends_online +
                         isoOthPpl_online +
                         lone01 +
                         lone02 +
                         lone03 +
                         happy +
                         lifeSat +
                         MLQ +
                         bor01 +
                         bor02 +
                         bor03 +
                         consp01 +
                         consp02 +
                         consp03 +
                         rank_A +
                         rank_B +
                         rank_C +
                         rank_D +
                         rank_E +
                         rank_F +
                         c19perBeh01 +
                         c19perBeh02 +
                         c19perBeh03 +
                         c19RCA01 +
                         c19RCA02 +
                         c19RCA03 +
                         coronaClose_1 +
                         coronaClose_2 +
                         coronaClose_3 +
                         coronaClose_4 +
                         coronaClose_5 +
                         coronaClose_6 +
                         gender +
                         age +
                         edu,
                       data = brazil_data)

#regression for Brazil proso04
brazil_c19ProSo04 = lm(c19ProSo04 ~
                         employstatus_1 +
                         employstatus_2 +
                         employstatus_3 +
                         employstatus_4 +
                         employstatus_5 +
                         employstatus_6 +
                         employstatus_7 +
                         employstatus_8 +
                         employstatus_9 +
                         employstatus_10 +
                         isoFriends_inPerson +
                         isoOthPpl_inPerson +
                         isoFriends_online +
                         isoOthPpl_online +
                         lone01 +
                         lone02 +
                         lone03 +
                         happy +
                         lifeSat +
                         MLQ +
                         bor01 +
                         bor02 +
                         bor03 +
                         consp01 +
                         consp02 +
                         consp03 +
                         rank_A +
                         rank_B +
                         rank_C +
                         rank_D +
                         rank_E +
                         rank_F +
                         c19perBeh01 +
                         c19perBeh02 +
                         c19perBeh03 +
                         c19RCA01 +
                         c19RCA02 +
                         c19RCA03 +
                         coronaClose_1 +
                         coronaClose_2 +
                         coronaClose_3 +
                         coronaClose_4 +
                         coronaClose_5 +
                         coronaClose_6 +
                         gender +
                         age +
                         edu,
                       data = brazil_data)

#create brazil summaries
brazil_proSo1_summary <- summary(brazil_c19ProSo01)
brazil_proSo2_summary <- summary(brazil_c19ProSo02)
brazil_proSo3_summary <- summary(brazil_c19ProSo03)
brazil_proSo4_summary <- summary(brazil_c19ProSo04)

#create otherCountry regressions
#regression for otherCountry proso01
otherCountry_c19ProSo01 = lm(c19ProSo01 ~
                             employstatus_1 +
                             employstatus_2 +
                             employstatus_3 +
                             employstatus_4 +
                             employstatus_5 +
                             employstatus_6 +
                             employstatus_7 +
                             employstatus_8 +
                             employstatus_9 +
                             employstatus_10 +
                             isoFriends_inPerson +
                             isoOthPpl_inPerson +
                             isoFriends_online +
                             isoOthPpl_online +
                             lone01 +
                             lone02 +
                             lone03 +
                             happy +
                             lifeSat +
                             MLQ +
                             bor01 +
                             bor02 +
                             bor03 +
                             consp01 +
                             consp02 +
                             consp03 +
                             rank_A +
                             rank_B +
                             rank_C +
                             rank_D +
                             rank_E +
                             rank_F +
                             c19perBeh01 +
                             c19perBeh02 +
                             c19perBeh03 +
                             c19RCA01 +
                             c19RCA02 +
                             c19RCA03 +
                             coronaClose_1 +
                             coronaClose_2 +
                             coronaClose_3 +
                             coronaClose_4 +
                             coronaClose_5 +
                             coronaClose_6 +
                             gender +
                             age +
                             edu,
                           data = otherCountry_data)

#regression for otherCountry proso02
otherCountry_c19ProSo02 = lm(c19ProSo02 ~
                               employstatus_1 +
                               employstatus_2 +
                               employstatus_3 +
                               employstatus_4 +
                               employstatus_5 +
                               employstatus_6 +
                               employstatus_7 +
                               employstatus_8 +
                               employstatus_9 +
                               employstatus_10 +
                               isoFriends_inPerson +
                               isoOthPpl_inPerson +
                               isoFriends_online +
                               isoOthPpl_online +
                               lone01 +
                               lone02 +
                               lone03 +
                               happy +
                               lifeSat +
                               MLQ +
                               bor01 +
                               bor02 +
                               bor03 +
                               consp01 +
                               consp02 +
                               consp03 +
                               rank_A +
                               rank_B +
                               rank_C +
                               rank_D +
                               rank_E +
                               rank_F +
                               c19perBeh01 +
                               c19perBeh02 +
                               c19perBeh03 +
                               c19RCA01 +
                               c19RCA02 +
                               c19RCA03 +
                               coronaClose_1 +
                               coronaClose_2 +
                               coronaClose_3 +
                               coronaClose_4 +
                               coronaClose_5 +
                               coronaClose_6 +
                               gender +
                               age +
                               edu,
                             data = otherCountry_data)

#regression for otherCountry proso03
otherCountry_c19ProSo03 = lm(c19ProSo03 ~
                               employstatus_1 +
                               employstatus_2 +
                               employstatus_3 +
                               employstatus_4 +
                               employstatus_5 +
                               employstatus_6 +
                               employstatus_7 +
                               employstatus_8 +
                               employstatus_9 +
                               employstatus_10 +
                               isoFriends_inPerson +
                               isoOthPpl_inPerson +
                               isoFriends_online +
                               isoOthPpl_online +
                               lone01 +
                               lone02 +
                               lone03 +
                               happy +
                               lifeSat +
                               MLQ +
                               bor01 +
                               bor02 +
                               bor03 +
                               consp01 +
                               consp02 +
                               consp03 +
                               rank_A +
                               rank_B +
                               rank_C +
                               rank_D +
                               rank_E +
                               rank_F +
                               c19perBeh01 +
                               c19perBeh02 +
                               c19perBeh03 +
                               c19RCA01 +
                               c19RCA02 +
                               c19RCA03 +
                               coronaClose_1 +
                               coronaClose_2 +
                               coronaClose_3 +
                               coronaClose_4 +
                               coronaClose_5 +
                               coronaClose_6 +
                               gender +
                               age +
                               edu,
                             data = otherCountry_data)

#regression for otherCountry proso04
otherCountry_c19ProSo04 = lm(c19ProSo04 ~
                               employstatus_1 +
                               employstatus_2 +
                               employstatus_3 +
                               employstatus_4 +
                               employstatus_5 +
                               employstatus_6 +
                               employstatus_7 +
                               employstatus_8 +
                               employstatus_9 +
                               employstatus_10 +
                               isoFriends_inPerson +
                               isoOthPpl_inPerson +
                               isoFriends_online +
                               isoOthPpl_online +
                               lone01 +
                               lone02 +
                               lone03 +
                               happy +
                               lifeSat +
                               MLQ +
                               bor01 +
                               bor02 +
                               bor03 +
                               consp01 +
                               consp02 +
                               consp03 +
                               rank_A +
                               rank_B +
                               rank_C +
                               rank_D +
                               rank_E +
                               rank_F +
                               c19perBeh01 +
                               c19perBeh02 +
                               c19perBeh03 +
                               c19RCA01 +
                               c19RCA02 +
                               c19RCA03 +
                               coronaClose_1 +
                               coronaClose_2 +
                               coronaClose_3 +
                               coronaClose_4 +
                               coronaClose_5 +
                               coronaClose_6 +
                               gender +
                               age +
                               edu,
                             data = otherCountry_data)

#create otherCountry summaries
otherCountry_proSo1_summary <- summary(otherCountry_c19ProSo01)
otherCountry_proSo2_summary <- summary(otherCountry_c19ProSo02)
otherCountry_proSo3_summary <- summary(otherCountry_c19ProSo03)
otherCountry_proSo4_summary <- summary(otherCountry_c19ProSo04)

#view summaries (highlight to use)
brazil_proSo1_summary
brazil_proSo2_summary
brazil_proSo3_summary
brazil_proSo4_summary
otherCountry_proSo1_summary
otherCountry_proSo2_summary
otherCountry_proSo3_summary
otherCountry_proSo4_summary

#create correlation table for otherCountries
otherCountry_corTable <- cor(cbind(otherCountry_data[, c(1:38, 57:59, 40:41, 51:56, 43:46)]), use = "complete.obs")

#take only relevant columns
otherCountry_corTable <- otherCountry_corTable[, 50:53]

#convert matrix to a dataframe
otherCountry_corTable <- as.data.frame(otherCountry_corTable)

#assign rows to remove (rows should be predictors, columns should be outcomes)
rows_to_remove <- c("c19ProSo01",
                    "c19ProSo02",
                    "c19ProSo03",
                    "c19ProSo04")

#remove outcome rows, keeping only outcome columns
otherCountry_corTable <- subset(otherCountry_corTable, subset = !(rownames(otherCountry_corTable) %in% rows_to_remove))

#create correlation heatmap
#add rownames (predictors) as a column
otherCountry_corTable$predictor <- rownames(otherCountry_corTable)

#pivot the table to get correlation of variable pairs
otherCountry_corHeatmap <- pivot_longer(otherCountry_corTable, cols = -predictor, names_to = "outcome", values_to = "Correlation")

#plot the heatmap
ggplot(otherCountry_corHeatmap, aes(x = outcome, y = predictor, fill = Correlation)) +
  geom_tile() +
  scale_fill_gradient2(low = "#08306b", mid = "white", high = "#67000d", midpoint = 0) +
  theme_minimal() +
  labs(
    title = "Correlation Heatmap",
    x = "Outcomes",
    y = "Predictors",
    fill = "Correlation"
  )

View(otherCountry_corTable)

########################################################
#3b
########################################################

#label cluster countries
regression_data <- regression_data %>%
  mutate(clusterCountry = ifelse(coded_country %in% c("Bulgaria", 
                                                      "Armenia", 
                                                      "Georgia", 
                                                      "Argentina", 
                                                      "Panama", 
                                                      "Turkey", 
                                                      "Colombia", 
                                                      "Albania", 
                                                      "Ukraine", 
                                                      "Bosnia and Herzegovina", 
                                                      "Greece", 
                                                      "Montenegro"), 1, 0))

#extract cluster country data
clusterCountry_data <- regression_data[regression_data$clusterCountry == 1, ]

clusterCountry_c19ProSo01 = lm(c19ProSo01 ~
                               employstatus_1 +
                               employstatus_2 +
                               employstatus_3 +
                               employstatus_4 +
                               employstatus_5 +
                               employstatus_6 +
                               employstatus_7 +
                               employstatus_8 +
                               employstatus_9 +
                               employstatus_10 +
                               isoFriends_inPerson +
                               isoOthPpl_inPerson +
                               isoFriends_online +
                               isoOthPpl_online +
                               lone01 +
                               lone02 +
                               lone03 +
                               happy +
                               lifeSat +
                               MLQ +
                               bor01 +
                               bor02 +
                               bor03 +
                               consp01 +
                               consp02 +
                               consp03 +
                               rank_A +
                               rank_B +
                               rank_C +
                               rank_D +
                               rank_E +
                               rank_F +
                               c19perBeh01 +
                               c19perBeh02 +
                               c19perBeh03 +
                               c19RCA01 +
                               c19RCA02 +
                               c19RCA03 +
                               coronaClose_1 +
                               coronaClose_2 +
                               coronaClose_3 +
                               coronaClose_4 +
                               coronaClose_5 +
                               coronaClose_6 +
                               gender +
                               age +
                               edu,
                             data = clusterCountry_data)

#regression for otherCountry proso02
clusterCountry_c19ProSo02 = lm(c19ProSo02 ~
                               employstatus_1 +
                               employstatus_2 +
                               employstatus_3 +
                               employstatus_4 +
                               employstatus_5 +
                               employstatus_6 +
                               employstatus_7 +
                               employstatus_8 +
                               employstatus_9 +
                               employstatus_10 +
                               isoFriends_inPerson +
                               isoOthPpl_inPerson +
                               isoFriends_online +
                               isoOthPpl_online +
                               lone01 +
                               lone02 +
                               lone03 +
                               happy +
                               lifeSat +
                               MLQ +
                               bor01 +
                               bor02 +
                               bor03 +
                               consp01 +
                               consp02 +
                               consp03 +
                               rank_A +
                               rank_B +
                               rank_C +
                               rank_D +
                               rank_E +
                               rank_F +
                               c19perBeh01 +
                               c19perBeh02 +
                               c19perBeh03 +
                               c19RCA01 +
                               c19RCA02 +
                               c19RCA03 +
                               coronaClose_1 +
                               coronaClose_2 +
                               coronaClose_3 +
                               coronaClose_4 +
                               coronaClose_5 +
                               coronaClose_6 +
                               gender +
                               age +
                               edu,
                             data = clusterCountry_data)

#regression for otherCountry proso03
clusterCountry_c19ProSo03 = lm(c19ProSo03 ~
                               employstatus_1 +
                               employstatus_2 +
                               employstatus_3 +
                               employstatus_4 +
                               employstatus_5 +
                               employstatus_6 +
                               employstatus_7 +
                               employstatus_8 +
                               employstatus_9 +
                               employstatus_10 +
                               isoFriends_inPerson +
                               isoOthPpl_inPerson +
                               isoFriends_online +
                               isoOthPpl_online +
                               lone01 +
                               lone02 +
                               lone03 +
                               happy +
                               lifeSat +
                               MLQ +
                               bor01 +
                               bor02 +
                               bor03 +
                               consp01 +
                               consp02 +
                               consp03 +
                               rank_A +
                               rank_B +
                               rank_C +
                               rank_D +
                               rank_E +
                               rank_F +
                               c19perBeh01 +
                               c19perBeh02 +
                               c19perBeh03 +
                               c19RCA01 +
                               c19RCA02 +
                               c19RCA03 +
                               coronaClose_1 +
                               coronaClose_2 +
                               coronaClose_3 +
                               coronaClose_4 +
                               coronaClose_5 +
                               coronaClose_6 +
                               gender +
                               age +
                               edu,
                             data = clusterCountry_data)

#regression for otherCountry proso04
clusterCountry_c19ProSo04 = lm(c19ProSo04 ~
                               employstatus_1 +
                               employstatus_2 +
                               employstatus_3 +
                               employstatus_4 +
                               employstatus_5 +
                               employstatus_6 +
                               employstatus_7 +
                               employstatus_8 +
                               employstatus_9 +
                               employstatus_10 +
                               isoFriends_inPerson +
                               isoOthPpl_inPerson +
                               isoFriends_online +
                               isoOthPpl_online +
                               lone01 +
                               lone02 +
                               lone03 +
                               happy +
                               lifeSat +
                               MLQ +
                               bor01 +
                               bor02 +
                               bor03 +
                               consp01 +
                               consp02 +
                               consp03 +
                               rank_A +
                               rank_B +
                               rank_C +
                               rank_D +
                               rank_E +
                               rank_F +
                               c19perBeh01 +
                               c19perBeh02 +
                               c19perBeh03 +
                               c19RCA01 +
                               c19RCA02 +
                               c19RCA03 +
                               coronaClose_1 +
                               coronaClose_2 +
                               coronaClose_3 +
                               coronaClose_4 +
                               coronaClose_5 +
                               coronaClose_6 +
                               gender +
                               age +
                               edu,
                             data = clusterCountry_data)

#create otherCountry summaries
clusterCountry_proSo1_summary <- summary(clusterCountry_c19ProSo01)
clusterCountry_proSo2_summary <- summary(clusterCountry_c19ProSo02)
clusterCountry_proSo3_summary <- summary(clusterCountry_c19ProSo03)
clusterCountry_proSo4_summary <- summary(clusterCountry_c19ProSo04)

#show summaries
clusterCountry_proSo1_summary
clusterCountry_proSo2_summary
clusterCountry_proSo3_summary
clusterCountry_proSo4_summary
