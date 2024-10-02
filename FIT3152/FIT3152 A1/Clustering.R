library(dplyr)
library(dendextend)
library(circlize)

###############################
#Data Gathering and Cleaning
###############################

#load cvbase
cvbase = read.csv("PsyCoronaBaselineExtract.csv")

#extract countries
countryList <- data.frame("coded_country" = cvbase$coded_country)

#remove duplicates
clustering_data <- unique(countryList)

#remove NA values and blanks
clustering_data <- clustering_data %>%
  filter_all(any_vars(!is.na(.) & . != ""))

#load ghs data
ghs_data <- read.csv("2021-GHS-Index-April-2022.csv")

#rename columns
ghs_data <- data.frame(
    "coded_country" = ghs_data$"Country", 
    "ghs_overall_score" = ghs_data$"OVERALL.SCORE")

#rename countries to match original data country names
ghs_data <- ghs_data %>%
  transform(coded_country = case_when
            (
              coded_country == "Bosnia and Hercegovina" ~ "Bosnia and Herzegovina",
              coded_country == "Kyrgyz Republic" ~ "Kyrgyzstan",
              coded_country == "Serbia" ~ "Republic of Serbia",
              TRUE ~ coded_country
            )
  )

#merge by country
clustering_data <- merge(clustering_data, ghs_data, by = "coded_country")

#load gdp per capita data (worldbank)
gdpPC2021_data <-read.csv("API_NY.GDP.PCAP.CD_DS2_en_csv_v2_133.csv")

#rename columns
gdpPC2021_data <- data.frame(
  "coded_country" = gdpPC2021_data$"Country.Name", 
  "GDP_per_capita_2021" = gdpPC2021_data$"X2021")

#rename countries to match original dataframe country names
gdpPC2021_data <- gdpPC2021_data %>%
  transform(coded_country = case_when
            (
              coded_country == "Egypt, Arab Rep." ~ "Egypt",
              coded_country == "Venezuela, RB" ~ "Venezuela",
              coded_country == "Lao PDR" ~ "Laos",
              coded_country == "Iran, Islamic Rep." ~ "Iran",
              coded_country == "Kyrgyz Republic" ~ "Kyrgyzstan",
              coded_country == "Viet Nam" ~ "Vietnam",
              coded_country == "Brunei Darussalam" ~ "Brunei",
              coded_country == "Serbia" ~ "Republic of Serbia",
              coded_country == "Russian Federation" ~ "Russia",
              coded_country == "Turkiye" ~ "Turkey",
              coded_country == "Czechia" ~ "Czech Republic",
              coded_country == "Slovak Republic" ~ "Slovakia",
              coded_country == "Korea, Rep." ~ "South Korea",
              coded_country == "United States" ~ "United States of America",
              TRUE ~ coded_country
            )
  )

#add data to the clustering table
clustering_data <- merge(clustering_data, gdpPC2021_data, by = "coded_country")

#load unemployment rate data (worldbank)
unemployment2021_data <-read.csv("world bank unemployment.csv")

#rename columns
unemployment2021_data <- data.frame(
  "coded_country" = unemployment2021_data$"Country.Name", 
  "unemployment rate 2021" = unemployment2021_data$"X2021")

#rename countries to match original dataframe country names
unemployment2021_data <- unemployment2021_data %>%
  transform(coded_country = case_when
            (
              coded_country == "Egypt, Arab Rep." ~ "Egypt",
              coded_country == "Venezuela, RB" ~ "Venezuela",
              coded_country == "Lao PDR" ~ "Laos",
              coded_country == "Iran, Islamic Rep." ~ "Iran",
              coded_country == "Kyrgyz Republic" ~ "Kyrgyzstan",
              coded_country == "Viet Nam" ~ "Vietnam",
              coded_country == "Brunei Darussalam" ~ "Brunei",
              coded_country == "Serbia" ~ "Republic of Serbia",
              coded_country == "Russian Federation" ~ "Russia",
              coded_country == "Turkiye" ~ "Turkey",
              coded_country == "Czechia" ~ "Czech Republic",
              coded_country == "Slovak Republic" ~ "Slovakia",
              coded_country == "Korea, Rep." ~ "South Korea",
              coded_country == "United States" ~ "United States of America",
              TRUE ~ coded_country
            )
  )

clustering_data <- merge(clustering_data, unemployment2021_data, by = "coded_country")

#load world happiness index data
happiness_data_2019 <- read.csv("World Happiness Index 2019.csv")

#rename columns
happiness_data_2019 <- data.frame(
  "coded_country" = happiness_data_2019$"Country.or.region", 
  "happiness_score_2019" = happiness_data_2019$"Score")

#rename countries to match existing ones in data
happiness_data_2019 <- happiness_data_2019 %>%
  transform(coded_country = case_when
            (
              coded_country == "United States" ~ "United States of America",
              coded_country == "Trinidad & Tobago" ~ "Trinidad and Tobago",
              coded_country == "Serbia" ~ "Republic of Serbia",
              TRUE ~ coded_country
            )
  )

#add to clustering table
clustering_data <- merge(clustering_data, happiness_data_2019, by = "coded_country")

#load birth rate per 1000 data (worldbank)
birthRate_per_1000 <- read.csv("birthRate per 1000.csv")

#rename columns
birthRate_per_1000 <- data.frame(
  "coded_country" = birthRate_per_1000$"Country.Name", 
  "birth_rate_per_1000_2021" = birthRate_per_1000$"X2021")

#rename countries to match original dataframe country names
birthRate_per_1000 <- birthRate_per_1000 %>%
  transform(coded_country = case_when
            (
              coded_country == "Egypt, Arab Rep." ~ "Egypt",
              coded_country == "Venezuela, RB" ~ "Venezuela",
              coded_country == "Lao PDR" ~ "Laos",
              coded_country == "Iran, Islamic Rep." ~ "Iran",
              coded_country == "Kyrgyz Republic" ~ "Kyrgyzstan",
              coded_country == "Viet Nam" ~ "Vietnam",
              coded_country == "Brunei Darussalam" ~ "Brunei",
              coded_country == "Serbia" ~ "Republic of Serbia",
              coded_country == "Russian Federation" ~ "Russia",
              coded_country == "Turkiye" ~ "Turkey",
              coded_country == "Czechia" ~ "Czech Republic",
              coded_country == "Slovak Republic" ~ "Slovakia",
              coded_country == "Korea, Rep." ~ "South Korea",
              coded_country == "United States" ~ "United States of America",
              TRUE ~ coded_country
            )
  )

#add to clustering table
clustering_data <- merge(clustering_data, birthRate_per_1000, by = "coded_country")

#load birth rate per 1000 data (worldbank)
press_freedom_2021_data <- read.csv("press-freedom-index-rsf.csv")

#take only 2021 data
press_freedom_2021_data <- press_freedom_2021_data %>%
  filter(Year == 2021)

#remove year and code columns
press_freedom_2021_data$Year <- NULL
press_freedom_2021_data$Code <- NULL

#rename columns
press_freedom_2021_data <- data.frame(
  "coded_country" = press_freedom_2021_data$"Entity", 
  "press_freedom_score_2021" = press_freedom_2021_data$"Press.Freedom.Score")

#rename countries to match original dataframe country names
press_freedom_2021_data <- press_freedom_2021_data %>%
  transform(coded_country = case_when
            (
              coded_country == "Serbia" ~ "Republic of Serbia",
              coded_country == "Czechia" ~ "Czech Republic",
              coded_country == "United States" ~ "United States of America",
              TRUE ~ coded_country
            )
  )

#add to clustering table
clustering_data <- merge(clustering_data, press_freedom_2021_data, by = "coded_country")

#load corruption perception data, and trim whitespace (why is this dataset like this lol)
corruption_perception_2021_data <- read.csv("corruption_data.csv", strip.white=TRUE)

#rename columns
corruption_perception_2021_data <- data.frame(
  "coded_country" = corruption_perception_2021_data$"region_name", 
  "CPI_score_2021" = corruption_perception_2021_data$"X2021")

#rename countries
corruption_perception_2021_data <- corruption_perception_2021_data %>%
  transform(coded_country = case_when
            (
              coded_country == "Serbia" ~ "Republic of Serbia",
              coded_country == "United States" ~ "United States of America",
              TRUE ~ coded_country
            )
  )

#add to clustering table
clustering_data <- merge(clustering_data, corruption_perception_2021_data, by = "coded_country")

####################################################################################
#Hierarchical Clustering
#for the marker:
#If it is possible I will include all relevant csv files in a zip in the submission,
#otherwise please save the table of values and load it as clustering_data
####################################################################################


#omit NA Values
clustering_data <- na.omit(clustering_data)

#convert country column into rownames
rownames(clustering_data) <- clustering_data[,1]

#remove country column
clustering_data <- clustering_data[, -1]

#normalise values
clustering_data <- as.data.frame(scale(clustering_data))

#create distance matrix
distance_matrix <- dist(clustering_data, method = "euclidean")

#create cluster
cluster <- hclust(distance_matrix, method = "average")

#create dendrogram object
dendrogram <- as.dendrogram(cluster)

#customize the dendrogram
dendrogram <- dendrogram %>%
  color_branches(k = 12) %>%
  set("branches_lwd", 2)

#adjust margins so labels are not cutoff
par(mar = c(5, 4, 4, 2))

#plot the dendrogram
circlize_dendrogram(dendrogram, labels_track_height = 0.3)
