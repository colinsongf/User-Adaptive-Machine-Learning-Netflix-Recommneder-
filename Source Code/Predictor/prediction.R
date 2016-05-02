dataset <- read.table('movie_data_normalized.txt', sep = ",")
meanstdval <- read.table('mean_std.txt', sep = ",")
orgdata <- read.table('movie_data.txt', sep = ",")

smp_size <- floor(0.7 * nrow(dataset))

## set the seed to make your partition reproductible
set.seed(123)
train_ind <- sample(seq_len(nrow(dataset)), size = smp_size)

train <- dataset[train_ind, ]
test <- dataset[-train_ind, ]
#train <- as.data.frame(train)

orgtest <- orgdata[-train_ind, ]
meantest <- meanstdval[-train_ind, ]

orgtrain <- orgdata[train_ind, ]
meantrain <- meanstdval[train_ind, ]

model <- lm(V3 ~ V1+V2, data=train)

predicted <- predict(model, test[,1:2])
predicted <- predicted*meantest[,2]
predicted <- predicted + meantest[,1]
predicted <- round(predicted, digits = 2)
write.csv(predicted, file = "predicted.csv", row.names = FALSE)
write.csv(orgtest[,3], file = "org.csv", row.names = FALSE)
testdiff <- abs(predicted - orgtest[,3])
err <- (predicted - orgtest[,3])^2
err1 <- predicted - orgtest[,3]
write.csv(err1, file = "error.csv", row.names = FALSE)
mse <- sqrt(sum(err)/length(err))

tpredicted <- predict(model, train[,1:2])
tpredicted <- tpredicted*meantrain[,2]
tpredicted <- tpredicted + meantrain[,1]
traindiff <- abs(tpredicted - orgtrain[,3])
terr <- (tpredicted - orgtrain[,3])^2
tmse <- sqrt(sum(terr)/length(terr))


