library('ggplot2')

df <- read.csv('overal.csv')

print(df)
ggplot(df, aes_string(x = 'stategy', y = 'win.percentage')) +
        geom_bar(stat = 'identity', fill = 'steelblue') +
        #scale_y_continuous(labels = seq(0, 70, 10), breaks = seq(0, 70, 10)) +
        labs(x = 'Strategy', y = 'Win Percentage', title = 'BP vs Chum opening 4 rounds stategy')
ggsave(filename = 'overall.pdf')


df <- read.csv('yearly.csv')

print(head(df))

ggplot(df, aes_string(x = 'year', y = 'win.percentage', fill = 'strategy')) +
        geom_bar(stat = 'identity', position = position_dodge()) +
        scale_x_continuous(labels = seq(2008, 2017, 1), breaks = seq(2008, 2017, 1)) +
        labs(x = 'Year', y = 'Win Percentage', title = 'BP vs Chum Strategy')
ggsave(filename = 'yearly.pdf')




