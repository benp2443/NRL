library('ggplot2')

df <- read.csv('teams_refs.csv')

######### Manly ##########

df_manly <- df[df$team == 'Manly Warringah', ]
sorted_df <- df_manly[order(-df_manly$difference), ]
positions <- sorted_df$referee

ggplot(df_manly, aes(x = referee, y = difference)) +
	geom_bar(stat = 'identity', fill = 'steelblue') +
	scale_x_discrete(limits = positions) +
	scale_y_continuous(labels = seq(-20, 20, 5), breaks = seq(-20, 20, 5)) +
	theme(axis.text.x = element_text(angle = 90)) +
	labs(x = 'Referee', y = 'Win Percentage With - Win Percentage Without')
ggsave(filename = 'manly_refs.pdf')

########## Difference Distribution ##########

ggplot(df, aes(x = difference)) +
	geom_density() +
	scale_x_continuous(labels = seq(-30,30,10), breaks = seq(-30,30,10)) +
	labs(x = 'Wins Percentage With - Win Percentage Without', y = 'Density')
ggsave(filename = 'difference_density.pdf')

########## Teams which have a >= 30 difference ##########

df <- df[(df$difference <= -20 | df$difference >= 20), ]
df$team_ref <- paste(df$team, df$referee, sep = '-')

sorted_df <- df[order(df$difference), ]
positions <- sorted_df$team_ref

ggplot(df, aes(x = team_ref, y = difference)) +
	geom_bar(stat = 'identity', fill = 'steelblue') +
	scale_x_discrete(limits = positions) +
	#scale_y_continuous(labels = seq(-20, 20, 5), breaks = seq(-20, 20, 5)) +
	theme(axis.text.x = element_text(angle = 90)) +
	labs(x = 'Team-Referee', y = 'Win Percentage With - Win Percentage Without', title = 'Difference Extremes')
ggsave(filename = '20+-_difference.pdf')


