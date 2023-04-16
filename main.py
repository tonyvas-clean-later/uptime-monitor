#!/usr/bin/python3

from subprocess import run, PIPE
from datetime import datetime
from time import sleep

SCRIPT_DIR = path.normpath(path.dirname(__file__))
UPTIME_CSV = f'{SCRIPT_DIR}/uptime.csv'
LOG_FILE = f'{SCRIPT_DIR}/loggers.log'

def log(message):
    try:
        now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        line = f'{now} - {message}'

        print(line)
        with open(LOG_FILE, 'a') as f:
            f.write(line + '\n')
    except Exception as e:
        raise Exception(f'Failed to log: {e}')

def get_start():
    pass

def get_end():
    pass

def get_uptime():
    pass

def format_uptime():
    pass

def write_uptime():
    pass