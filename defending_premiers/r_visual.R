library(ggplot2)
library(reshape2)

df <- read.csv('prem_wl.csv')

print(df)

df$Prem.Def = factor(df$Prem.Def, levels = c('Premiers', 'Defending'))

ggplot(df, aes(x = Year_Premier, y = Win_Percent, fill = Prem.Def)) +
	geom_bar(stat = 'identity', position = position_dodge()) +
	theme(axis.text.x = element_text(angle = 90)) +
	labs(title = 'Win Percentage - Premiership Year Vs Defending Year', x = 'Premiers', y = 'Win Percentage (regular season)', fill = "")
ggsave(filename = 'win_lose_premVdef.pdf')


df <- read.csv('prems_df.csv')

ggplot(df, aes(x = year_prem, y = wins_change)) +
	geom_bar(stat = 'identity', fill = 'steelblue') +
	labs(title = 'Reduction in Wins as Defending Premiers', y = 'Number of Wins Less in Defending Season', x = 'Premiers') +
	theme(axis.text.x = element_text(angle = 90))
ggsave(filename = 'win_reduction.pdf')

########## Win percentage comparsion during periods ##########

df <- read.csv('period_change.csv')

ggplot(df, aes(x = Period, y = Change)) +
	geom_bar(stat = 'identity', fill = 'steelblue') +
	scale_x_discrete(limits = c('Pre', 'Origin', 'Post')) +
	labs(title = 'Average Change in Win Percentage', x = 'Period', y = 'Win Percentage Change')
ggsave(filename = 'change.pdf')

win_percent <- function(csv_name, prem_col, def_col, title_, saveas) {

	df <- read.csv(csv_name)

	df$variable <- factor(df$variable, levels = c(prem_col, def_col))

	ggplot(df, aes(x = year_prem, y = value, fill = variable)) +
		geom_bar(stat = 'identity', position = 'dodge') +
		theme(axis.text.x = element_text(angle = 90)) +
		labs(x = 'Premiers', y = 'Win Percentage', title = title_, fill = '')
	ggsave(filename = saveas)
}

win_percent('pre_win_percent.csv', 'prem_w_pre_%', 'def_w_pre_%', 'Win Percentage Pre Origin', 'pre_win_percent.pdf') 
win_percent('origin_win_percent.csv', 'prem_w_origin_%', 'def_w_origin_%', 'Win Percentage During Origin', 'origin_win_percent.pdf') 
win_percent('post_win_percent.csv', 'prem_w_post_%', 'def_w_post_%', 'Win Percentage Post Origin', 'post_win_percent.pdf') 
