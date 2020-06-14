import pandas as pd
from collections import defaultdict

def assign_timedeltas_mix(block_name):
    '''
    Appending timedeltas by block names (only for mixing)
    '''
    if block_name in ['For Bussines']:
        return pd.Timedelta(5, unit='H')
    elif block_name in ['Big Country', 'Remember All']:
        return pd.Timedelta(3, unit='H')
    else:
        return pd.Timedelta(1.5, unit='H')
    
def assign_timedeltas_master(bytes):
    '''
    Assigning timedeltas to master columns.
    Awaiting bytes as atgument.
    '''
    secs = bytes*8/2304000
    delta = pd.Timedelta(secs, unit='s')
    return delta/8

def assign_timedeltas_voiceover(bytes):
    '''
    Assigning timedeltas to voiceover columns.
    Awaiting bytes as atgument.
    '''
    secs = bytes*8/2304000
    delta = pd.Timedelta(secs, unit='s')
    return delta*10

def make_timedeltas(df):
    '''
    Adds all timedeltas
    '''
    df['datetime'] = pd.to_datetime(df['datetime'], format = '%d/%m/%Y %H:%M:%S')
    df['mix_delta'] = df[df['type']=='to mix']['block'].apply(assign_timedeltas_mix)
    df['master_delta'] = df[df['type']=='master']['size'].apply(assign_timedeltas_master)
    df['voice_delta'] = df[df['type']=='voiceover']['size'].apply(assign_timedeltas_voiceover)
    return df

def count_sum_turns(from_date, to_date):
    df = pd.read_csv('sound_repository.csv')
    df = df.drop_duplicates()
    df = make_timedeltas(df)
    df = df[(df['datetime'] >= from_date)&(df['datetime'] <= to_date)&(df['type'] != '4-71a to mix')]
    total = df.groupby('block').agg({
    'mix_delta':'sum',
    'master_delta':'sum',
    'voice_delta':'sum'
    })
    total['sum_delta'] = total.sum(axis=1)
    total['sum_turns'] = total['sum_delta'] / pd.Timedelta(11, unit='H')
    return total.reset_index()

def sb_working_calendar():
    '''Returns calendar dataframe from Studio Block's workers
    (Starts from date 2019-12-01 because it's a latest working schedule update)
    Working scheme is Work, Work, Day off, Day off, Work, Day off. Fully approx. 15 turn in month.
    '''
    working_calendar = {}
    date_range = pd.date_range(start='2019-12-01', end='today')
    for i in range(len(date_range)):
        if i%6 == 0 or i%6 == 3:
            working_calendar[date_range[i]] = [False, False, True, True]
        elif i%6 == 1 or i%6 == 4:
            working_calendar[date_range[i]] = [True, True, False, False]
        elif i%6 == 2:
            working_calendar[date_range[i]] = [False, True, True, False]
        elif i%6 == 5:
            working_calendar[date_range[i]] = [True, False, False, True]
    return pd.DataFrame.from_dict(working_calendar, 
                                  orient='index', 
                                 columns = ['Console operator 1','Mic operator 1','Console operator 2','Mic operator 2']
                                 )

def sb_report_equal(excel_file):
    '''
    Making report depending on odd/even working turns. Artificial way of turns distribution.
    '''
    df = pd.read_excel(excel_file, header=1, index_col=0)
    df = df.fillna(0)
    turn_dict = {}
    turn_dict['Studio Block'] = ['Console operator 1','Mic operator 1','Console operator 2','Mic operator 2']
    for column in df.columns:
        table_total = df[column].iloc[-1]
        if table_total != 0 and column != 'Total':
            series = df[column].iloc[:-1]
            odds_sum = series.iloc[1::2].sum()
            evens_sum = series.iloc[::2].sum()
            turn_dict[column.strip()] = [odds_sum, odds_sum, evens_sum, evens_sum]
            new_df = pd.DataFrame.from_dict(turn_dict)
            new_df['Total'] = new_df.sum(axis=1)
    return new_df

def sb_report_true(excel_file):
    '''
    Making report depending on real working turns. Function will get 
    '''
    source_df = pd.read_excel(excel_file, header=1, index_col=0)
    df = source_df.join(sb_working_calendar())
    turn_dict = defaultdict(list)
    turn_dict['Personel'] = ['Console operator 1','Mic operator 1','Console operator 2','Mic operator 2']
    workers = ['Console operator 1','Mic operator 1','Console operator 2','Mic operator 2']
    for worker in workers:
        for column in df.columns:
            table_total = df[column].iloc[-1]
            if table_total != 0 and column not in ['Console operator 1','Mic operator 1','Console operator 2','Mic operator 2', 'Total']:
                total = df.loc[:,[column, worker]][df[worker]==True].sum()[0]
                turn_dict[column.strip().title()].append(total)
    new_df = pd.DataFrame.from_dict(turn_dict)
    return new_df

def amf_report_equal(from_date, to_date):
    '''
    Sorting report for amf according to number of days in months
    and parts taken by programms
    Date format: ('2020-02-01','2020-02-29')
    '''
    df = pd.read_csv('sound_repository.csv')
    df = df.drop_duplicates()
    df['datetime'] = pd.to_datetime(df['datetime'], format = '%d/%m/%Y %H:%M:%S')
    month = df[(df['datetime'] >= from_date)&(df['datetime'] <= to_date)&(df['type'] != '4-71a to mix')]
    delta = abs(pd.to_datetime(to_date) - pd.to_datetime(from_date)).days
    month_group = month.groupby('block').agg({'name':'count'})
    month_group['part'] = month_group['name'] / month_group['name'].sum()
    month_group['days'] = round(month_group['part'] * delta)
    month_group['Postproduction mixer 1'] = month_group['days'] / 2
    month_group['Postproduction mixer 2'] = month_group['days'] / 2
    month_group = month_group.loc[:,['Postproduction mixer 1','Postproduction mixer 2']].transpose()
    month_group = month_group.reset_index().rename({'index':'Personel'}, axis=1)
    month_group.columns = month_group.columns.str.title()
    return month_group

def total_report(excel_file, from_date, to_date):
    '''Making total report'''
    asb = sb_report_true(excel_file)
    amf = amf_report_equal(from_date, to_date)
    total_report = asb.append(amf).fillna('-')
    total_report['Summary'] = total_report.sum(axis=1)
    return total_report

if __name__ == "__main__":
    pass