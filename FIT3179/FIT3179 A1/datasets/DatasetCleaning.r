library("tidyr")

#######################
# Clean Ped Count Data
#######################

data <- read.csv("pedestrian-counting-system-monthly-counts-per-hour.csv")

data <- separate(data, timestamp, into = c("date", "time"), sep = "T")

write.csv(data, "cleanedPedCount.csv")

########################
# Clean Climate Data
########################

data <- read.csv("meshed-sensor-type-2.csv")

data <- separate(data, time, into = c("date", "time"), sep = "T")

write.csv(data, "cleanedClimate.csv")