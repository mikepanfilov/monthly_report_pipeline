import os
from shutil import copy2 as copy
import datetime
import pandas as pd
    
WEEKS = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
COLUMNS = ('block', 'type', 'name', 'weekday', 'datetime', 'size')
TYPES = ('voiceover', 'master', 'to mix', '4-71a to mix')
CSV_FILE_MAIN = 'dataset/sound_repository.csv'
CSV_FILE_ALT = 'dataset/sound_repository.csv' # alternative path for catching exceptions

COPY_PATH = '/data_mine_mirror'

# Local network folders are here. Iside each programm folder there is three
# another folders:

# /Volumes/Active Environment/voiceover

# /Volumes/Active Environment/master

# /Volumes/Active Environment/to mix 
# or /Volumes/Active Environment/4-71a to mix (if it's special issue)

# And also inside all of folders staff leaves DONE folder to get new files visible and organised.

BLOCK_PATHS = ('/Volumes/Active Environment',
                 '/Volumes/Big country',
                 '/Volumes/Hamburg Account',
                 '/Volumes/House E',
                 '/Volumes/For the cause',
                 '/Volumes/Remember everything',
                 '/Volumes/Truth?',
                 '/Volumes/Figure of speech',
                 '/Volumes/The calendar',
                 '/Volumes/Sound',
                 '/Volumes/MaMy',
                 '/Volumes/Bedtime Stories')

BLOCK_NAMES =   ('Active Environment',
                 'Big country',
                 'Hamburg Account',
                 'House E',
                 'For the cause',
                 'Remember everything',
                 'Truth?',
                 'Figure of speech',
                 'The calendar',
                 'Sound',
                 'MaMy',
                 'Bedtime Stories')

def extract_info(path, prog_name, prog_type):
        current_lines = []
        current_name = []
        s = ','  # csv separator type

        # VOICEOVERS SEARCH'n'LIST
        vo_path = path
        vo_list = []
        for root, dirs, files in os.walk(vo_path):
            for file in files:
                if not file.startswith('._') and (file.endswith('.wav') or file.endswith('.aaf') or file.endswith('.omf')) \
                        and root.find('AAF Media')==-1:
                    # print('ROOT:\t', root, 'FILE:\t',file)  # SPECIAL FOR TESTING FILTERS!!!
                    vo_list.append([root, file])

        for vo in vo_list:
            vo_f_path = vo[0] + '/' + vo[1]
            vo_stat = os.stat(vo_f_path)
            vo_dt = datetime.datetime.fromtimestamp(vo_stat.st_birthtime).timetuple()
            vo_name = vo[1][:-4]
            vo_week = str(vo_dt.tm_wday)
            vo_date = '{:02d}'.format(vo_dt.tm_mday) + '/' + '{:02d}'.format(vo_dt.tm_mon) + '/' \
                    + '{:02d}'.format(vo_dt.tm_year)
            vo_time = '{:02d}'.format(vo_dt.tm_hour) + ':' + '{:02d}'.format(vo_dt.tm_min) + ':' \
                    + '{:02d}'.format(vo_dt.tm_sec)
            vo_size = str(vo_stat.st_size)

            vo_line = prog_name + s + prog_type + s + vo_name + s + vo_week + s + vo_date + ' ' + vo_time + s + vo_size + s \
                    + vo[0] + '/' + vo[1] +'\n'
            current_lines.append(vo_line)
            current_name.append(vo_name)
        return current_lines, current_name

def main():
    try:
        csv_f = open(CSV_FILE_MAIN, 'r', encoding='UTF-8')
        CSV_FILE = CSV_FILE_MAIN
    except:
        csv_f = open(CSV_FILE_ALT, 'r', encoding='UTF-8')
        CSV_FILE = CSV_FILE_ALT
    csv_old_list = csv_f.readlines()
    csv_old_names = []
    for line in csv_old_list:
        csv_old_names.append(line.split(sep=',')[2])
    csv_f.close()

    print(pd.to_datetime('today'))
    new_list = []
    for j in range(len(BLOCK_PATHS)):
        for i in range(len(TYPES)):
            recs, p_names = extract_info(BLOCK_PATHS[j]+'/'+TYPES[i], BLOCK_NAMES[j], TYPES[i])
            for ii in range(len(recs)):
                if p_names[ii] in csv_old_names:
                    pass
                else:
                    print('ADDED:\t', recs[ii][:-1])
                    csv_f = open(CSV_FILE, 'a', encoding='UTF-8')
                    csv_f.write(recs[ii])
                    new_list.append(recs[ii])
                    csv_f.close()                  

    copy(CSV_FILE, COPY_PATH)

if __name__=='__main__':
    main()