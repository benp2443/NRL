import pandas as pd
import numpy as np

df = pd.read_csv('../data/NRL_cleaned.csv')

def losing_amount(row):
    if row['HomeWin'] == 1.0:
        return row['H_PTS'] - row['A_PTS']
    else:
        return row ['A_PTS'] - row['H_PTS']

df['losing_margin'] = df.apply(losing_amount, axis = 1)

# Find losing margin of bottom 5%, 10%, 20%
ordered_df = df.sort_values('losing_margin', ascending = False).reset_index()
df_length = len(ordered_df)

five_percent_idx = int(0.05*df_length)
ten_percent_idx = int(0.1*df_length)
twenty_percent_idx = int(0.2*df_length)

def x_percent_value(df, idx):
    percent_value = ordered_df.loc[idx, 'losing_margin']
    return percent_value

five_percent_value = x_percent_value(df, five_percent_idx)
ten_percent_value = x_percent_value(df, ten_percent_idx)
twenty_percent_value = x_percent_value(df, twenty_percent_idx)

def losing_thresehold(losing_column, thresehold):
    if losing_column > thresehold:
        return True
    else:
        return False

def bounce_back_win_percent(df, thresehold):
    ''' Add in code so it only goes 1 round not between seasons or even fortnights
    '''
    df['big_loss'] = np.vectorize(losing_thresehold)(df['losing_margin'], thresehold)
    
    big_loss_idx = df.loc[df['big_loss'] == True, :].index.values
    
    win_loss = {'W':0, 'L':0}
    
    for idx in big_loss_idx:
        if df.loc[idx, 'HomeWin'] == True:
            team = df.loc[idx, 'Away']
        else:
            team = df.loc[idx, 'Home']
        
        i = idx + 1
        next_game = False
        while next_game == False:

            if i == len(df):
                break

            h_team = df.loc[i, 'Home']
            a_team = df.loc[i, 'Away']
    
            if h_team == team:
                if df.loc[i, 'HomeWin'] == True:
                    win_loss['W'] += 1
                else:
                    win_loss['L'] += 1
    
                next_game = True
    
            elif a_team == team:
                if df.loc[i, 'HomeWin'] == False:
                    win_loss['W'] += 1
                else:
                    win_loss['L'] += 1
                
                next_game = True
    
            i += 1


    print(thresehold)
    print(win_loss['W'])
    print(win_loss['L'])
    print(round(float(win_loss['W'])/(float(win_loss['W']) + float(win_loss['L'])),2),'\n')
    
bounce_back_win_percent(df, five_percent_value)
bounce_back_win_percent(df, ten_percent_value)
bounce_back_win_percent(df, twenty_percent_value)

df.to_csv('losing_margin.csv', index = False)
