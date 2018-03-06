library('ggplot2')

df <- read.csv('top_bot_5.csv')

ggplot(df, aes(x = Team, y = value, fill = variable)) +
	geom_bar(stat = 'identity', position = 'dodge') +
	theme(axis.text.x = element_text(angle = 90)) +
	labs(x = 'Team', y = 'Count', title = 'Cumulative binned rankings over last 10 seasons', fill = 'Binned Postion')
ggsave(filename = 'binned_rankings.pdf')

df <- read.csv('average_rank.csv')

sorted_df <- df[order(df$Average_rank), ]
positions <- sorted_df$Team

ggplot(df, aes(x = Team, y = Average_rank)) +
	geom_bar(stat = 'identity', fill = 'steelblue') +
	scale_x_discrete(limits = positions) +
	scale_y_continuous(labels = seq(1,12,1), breaks = seq(1,12,1)) +
	theme(axis.text.x = element_text(angle = 90)) +
	geom_hline(yintercept = 8.5) +
	labs(title = 'Teams Average Position Over Last 10 Years', x = 'Team', y = 'Average')
ggsave(filename = 'average_position.pdf')

##### Win Percentage #####

df <- read.csv('win_percentage.csv')

sorted_df <- df[order(-df$Win_Percentage), ]
positions <- sorted_df$Team

ggplot(df, aes(x = Team, y = Win_Percentage)) +
	geom_bar(stat = 'identity', fill = 'steelblue') +
	scale_x_discrete(limits = positions) +
	scale_y_continuous(labels = seq(0.1, 0.7, 0.1), breaks = seq(0.1, 0.7, 0.1)) +
	theme(axis.text.x = element_text(angle = 90)) +
	labs (x = 'Team', y = 'Win Percentage', title = 'Win Percentage over last 10 years')
ggsave(filename = 'win_percentage.pdf')


