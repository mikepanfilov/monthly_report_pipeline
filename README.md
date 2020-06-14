# Monthly Report Pipeline

## Project description

*For confidentional purposes all inside names are changed.*

This is a full data collectioning and processing pipeline for sound department's monthly report. The following pipline is consists of sereral big processing stages:

1. *Data collection script* - surfing througth the local network, collecting info about special audio files and writes down to csv file.

2. *Csv processing part* - is used by several Jupyter Notebook files for post production studio load scheduling and by script which is collecting and preprocessing info for reports.

3. *Excel file processing part* - uses for parsing data from studio loads file, distributing it to personel working turns and summarizing the results for report.

4. *Final script* - takes all data together and saves another excel file for sending back.

## Installation

*Warning:* This script originally designed for MacOS (Windows paths will not work with this version)

Python version 3 should be installed. It's also recommended to use virtual environment.
To install all the reqiurements use:

```bash
pip install -r requirements.txt
```

## Special files and names decription

- `data_pipeline.py` - csv collecting script (for more info see inline comments).
- `utils.py` - utilities to preprocessing and processing information for report

## Crontab adjustments

Installation for MacOS. Just type `crontab -e` in terminal end type folowing line:

```bash
0 */3 * * * python3 /Users/{user_name}/{script_folder}/data_pipeline.py >> /Users/{user_name}/{script_folder}/logs/data.log
```

### Postproduction working file

- `sound_repository.csv` - main comma separated file (full of surprises)

### Program main titles

- "Active Environment"
- "Big country"
- "Hamburg Account"
- "House E"
- "For the cause"
- "Remember everything"
- "Truth?"
- "Figure of speech"
- "The calendar"
- "Sound"
- "MaMy"
- "Bedtime Stories"

### Program types

- 'to mix'
- '4-71a to mix'
- 'master'
- 'voiceover'

### Studio Block Personel names

- Console operator 1
- Mic operator 1
- Console operator 2
- Mic operator 2

### Postproduction staff

- 'Postproduction mixer 1'
- 'Postproduction mixer 2'

## Goals

This project helps to organize and automatize monthly routine and also shows the real working parameters for future KPI purposes (~if at all possible in a fully analog-bureaucratized company~).

## Future improvements

- Script would translit cyrillic(other symbolics) in programm names.
- Script would record date in correct form (YYYY-MM-DD HH:MM:SS)
- Path slashes will be replaced by unique substitutes (to impove multiplatformness).
