library('ggplot2')

df <- read.csv('losing_margin.csv')

ggplot(df, aes(x = losing_margin)) +
    geom_density()
ggsave('losing_margin_density.pdf')

ggplot(df, aes(x = losing_margin)) +
    geom_histogram(binwidth = 2 )
ggsave('losing_margin_hist.pdf')

df$Year <- as.factor(df$Year)
ggplot(df, aes(x = Year, y = losing_margin)) +
    geom_boxplot()
ggsave('losing_margin_ByYear.pdf')
