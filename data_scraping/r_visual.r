library('ggplot2')

df <- read.csv('overtime_counts.csv')

df$year <- as.factor(df$year)
ggplot(df, aes(x = year, y = count)) +
    geom_bar(stat = 'identity', fill = 'steelblue') +
    labs(x = 'Year',y =  'Count', title = 'Overtime Games Per Year')

ggsave('overtime_count.pdf')
