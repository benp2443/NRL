library('ggplot2')
library('scales')

df <- read.csv('data/yearly_crowds.csv')

ggplot(df, aes(x = Year, y = sum)) +
	geom_bar(stat = 'identity', fill = 'steelblue') +
	scale_y_continuous(labels = comma) +
	scale_x_continuous(breaks = seq(2007, 2017, 1))
ggsave(filename = 'graphs/yearly_crowds.pdf')

ggplot(df, aes(x = Year, y = base_growth)) +
	geom_line() +
	geom_point() +
	scale_x_continuous(breaks = seq(2007, 2017, 1))
ggsave(filename = 'graphs/base_growth.pdf')

ggplot(df, aes(x = Year, yearly_growth)) +
	geom_line() +
	geom_point() +
	scale_x_continuous(breaks = seq(2007, 2017, 1))
ggsave(filename = 'graphs/yearly_growth.pdf')

ggplot(df, aes(x = Year, y = yearly_change)) +
	geom_bar(stat = 'identity', fill = 'steelblue') +
	scale_y_continuous(labels = comma) +
	scale_x_continuous(breaks = seq(2007, 2017, 1))
ggsave(filename = 'graphs/yearly_change.pdf')

df <- read.csv('data/period_crowd.csv')

ggplot(df, aes(x = Period, y = mean)) +
	geom_bar(stat = "identity", fill = 'steelblue') +
	labs(y = 'Average Attendance Per Game')
ggsave(filename = 'graphs/period_change.pdf')

df <- read.csv('data/test.csv')

teams_list <- unique(df$Team)

bandwagon <- function(team) {
	temp <- df[df$Team == team, ]

	ggplot(temp, aes(x = Rank, y = mean)) +
		geom_point() +
		geom_smooth(method = lm, se = FALSE) +
		geom_text(label = temp$Year, hjust = 0)
	ggsave(paste('graphs/teams/',team,'_bandwagon.pdf', sep = ""))
}


for (team in teams_list) {
	bandwagon(team)
}

df <- read.csv('data/teams_average.csv')

sorted_df <- df[order(-df$Crowd), ]
positions <- sorted_df$Home

ggplot(df, aes(x = Home, y = Crowd)) +
	geom_bar(stat = "identity", fill = 'steelblue') +
	scale_y_continuous(breaks = seq(0,30000,5000)) +
	scale_x_discrete(limits = positions) +
	theme(axis.text.x = element_text(angle = 90)) +
	labs(title = 'Average Home Crowd 2008-2017', y = 'Average', x = 'Team')
ggsave(filename = 'graphs/teams_average.pdf')

########## Broncos ##########

df <- read.csv('data/broncs_days.csv')

ggplot(df, aes(x = Day, y = count)) +
	geom_bar(stat = 'identity', fill = 'steelblue')
ggsave(filename = 'graphs/broncos_days.pdf')


df <- read.csv('data/broncs_fri_other.csv')

ggplot(df, aes(x = fri_other, y = Crowd)) +
	geom_bar(stat = 'identity', fill = 'steelblue')
ggsave(filename = 'graphs/broncos_fri_other.pdf')


########## Day of week ##########

df <- read.csv('data/days_crowds.csv')

positions <- c('Thu', 'Fri', 'Sat', 'Sun', 'Mon')

ggplot(df, aes(x = Day, y = Crowd)) +
	geom_bar(stat = "identity", fill = "steelblue") +
	scale_x_discrete(limits = positions) +
	labs(title = 'Average Crowd By Day', y = 'Average Crowd', x = 'Day')
ggsave(filename = 'graphs/days.pdf')




