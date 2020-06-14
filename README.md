# Monthly Report Pipeline

## Project description

*For confidentional purposes all inside names are changed.*

This is a full data collectioning and processing pipeline for sound department's monthly report. The following pipline is consists of sereral big processing stages:

1. *Data collection script* - surfing througth the local network, collecting info about special audio files and writes down to csv file.

2. *Csv processing part* - is used by several Jupyter Notebook files for post production studio load scheduling and by script which is collecting and preprocessing info for reports.

3. *Excel file processing part* - uses for parsing data from studio loads file, distributing it to personel working turns and summarizing the results for report.

4. *Final script* - takes all data together and saves another excel file for sending back.

## Installation

## Special files and names decription

`utils.py`

### Postproduction working file

- `sound_repository.csv`

### Program names

- 'For Bussines'
- 'Big Country'
- 'Remember All'

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
