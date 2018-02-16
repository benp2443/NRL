library("ggplot2")


df = read.csv('NRL_cleaned.csv')

ggplot(df, aes(HomeWin)) + geom_bar()
