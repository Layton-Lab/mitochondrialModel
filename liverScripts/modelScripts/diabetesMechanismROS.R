if (isFALSE(grepl("liverScripts/modelscripts", getwd()))) {
  setwd("liverScripts/modelscripts")
}

worstCaseOXPHOS <- list()

ks <- 1:42

files <- paste0("../results/resultsDiabetesComplexMechanismOXPHOS", ks, ".csv")
## Also compare resultsDiabetesComplexMechanism files from the script diabetesComplexMechanism2.py
files <- lapply(files, data.table::fread)

a <- function(x) tail(x$ATP_c, 1)
q <- function(x) tail(x$QH2_x, 1)
c <- function(x) tail(x$Cred_i, 1)

ATPs <- sapply(files, a)
Qs <- sapply(files, q)/(2.148e-3*0.2)
Cs <- sapply(files, c)/(1.956e-3*1.33)

hist(ATPs*1000)
hist(Qs)
hist(Cs)
## Give us a sense of the liver's response to these stimuli if you used CytC/CoQ values taken from the
## kidney, which indicates that these values explain the difference in the kidney's response.
