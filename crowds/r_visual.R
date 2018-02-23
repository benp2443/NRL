library('ggplot2')

df <- read.csv('test.csv')

ggplot(df, aes(x = Rank, y = test, color = Team)) +
	geom_point() +
	geom_smooth(method = 'lm', se = FALSE)
