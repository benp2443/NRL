library(ggplot2)
library(reshape2)

df <- read.csv('win_percentage.csv')

colnames(df) <- c('year', 'Premiers', 'Defending_Premiers')

df <- melt(df, id.vars = 'year')

ggplot(df, aes(x = year, y = value, fill = variable)) +
	geom_bar(stat = 'identity', position = 'dodge') +
	scale_fill_discrete(name = "", breaks = c('Premiers', 'Defending_Premiers'), labels = c('Premiers', 'Defending Premiers')) +
	scale_x_discrete(limits = c('2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016')) +
	theme(axis.text.x = element_text(angle = 90)) +
	ggtitle('Win Percentage')

