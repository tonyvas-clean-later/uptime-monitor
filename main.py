#!/usr/bin/python3

from subprocess import run, PIPE
from datetime import datetime
from time import sleep
from os import path

SCRIPT_DIR = path.normpath(path.dirname(__file__))
UPTIME_CSV = f'{SCRIPT_DIR}/uptime.csv'
LOG_FILE = f'{SCRIPT_DIR}/loggers.log'

LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
UPTIME_DATE_FORMAT = LOG_DATE_FORMAT

CSV_SEPARATOR = ','
MONITOR_INTERVAL_S = 1

def log(message):
    try:
        now = datetime.today().strftime(LOG_DATE_FORMAT)
        line = f'{now} - {message}'

        print(line)
        with open(LOG_FILE, 'a') as f:
            f.write(line + '\n')
    except Exception as e:
        raise Exception(f'Failed to log: {e}')

def get_start():
    try:
        proc = run(['uptime', '-s'], stdout=PIPE, stderr=PIPE)
        if proc.returncode != 0:
            stderr = proc.stderr.decode('utf-8')
            raise Exception(f'Non-zero exit code: {stderr}')
        else:
            stdout = proc.stdout.decode('utf-8')
            return stdout.strip()
    except Exception as e:
        raise Exception(f'Failed to get start time: {e}')

def get_end():
    try:
        return datetime.today().strftime(UPTIME_DATE_FORMAT)
    except Exception as e:
        raise Exception(f'Failed to get end time: {e}')

def get_uptime():
    try:
        proc = run(['uptime', '-p'], stdout=PIPE, stderr=PIPE)
        if proc.returncode != 0:
            stderr = proc.stderr.decode('utf-8')
            raise Exception(f'Non-zero exit code: {stderr}')
        else:
            stdout = proc.stdout.decode('utf-8')
            return stdout.strip()
    except Exception as e:
        raise Exception(f'Failed to get uptime: {e}')

def format_line(start, end, uptime):
    try:
        values = []
        for value in [start, end, uptime]:
            values.append(str(value).replace(CSV_SEPARATOR, ''))

        return CSV_SEPARATOR.join(values)
    except Exception as e:
        raise Exception(f'Failed to format uptime: {e}')

def read_previous_lines():
    try:
        if path.exists(UPTIME_CSV):
            print('exists')
            with open(UPTIME_CSV, 'r') as f:
                return f.read().strip().split('\n')[0:-1]
        else:
            print('no exist')
            return []
    except Exception as e:
        raise Exception(f'Failed to read uptimes: {e}')

def write_line(line, overwriting):
    try:
        if overwriting:
            lines = read_previous_lines()
            lines.append(line)

            with open(UPTIME_CSV, 'w') as f:
                f.write('\n'.join(lines) + '\n')
        else:
            with open(UPTIME_CSV, 'a') as f:
                f.write(line + '\n')
    except Exception as e:
        raise Exception(f'Failed to write uptime: {e}')

try:
    overwriting = False
    log(f'Monitoring started!')

    while 1:
        formatted = None
        
        try:
            formatted = format_line(get_start(), get_end(), get_uptime())
        except Exception as e:
            log(f'Error: {e}')

        if formatted is not None:
            write_line(formatted, overwriting)
            if not overwriting:
                overwriting = True

        sleep(MONITOR_INTERVAL_S)
except Exception as e:
    log('Critical error: {e}')