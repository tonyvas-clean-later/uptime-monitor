#!/usr/bin/python3

from subprocess import run, PIPE
from datetime import datetime
from time import sleep
from os import path

# File locations
SCRIPT_DIR = path.normpath(path.dirname(__file__))
UPTIME_CSV = f'{SCRIPT_DIR}/uptime.csv'
LOG_FILE = f'{SCRIPT_DIR}/loggers.log'

# Date formatting
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
UPTIME_DATE_FORMAT = LOG_DATE_FORMAT

CSV_SEPARATOR = ','
MONITOR_INTERVAL_S = 1

def log(message):
    try:
        # Prepend message with date
        now = datetime.today().strftime(LOG_DATE_FORMAT)
        line = f'{now} - {message}'

        # Print line to console
        print(line)
        # Append line to log file
        with open(LOG_FILE, 'a') as f:
            f.write(line + '\n')
    except Exception as e:
        raise Exception(f'Failed to log: {e}')

def get_start():
    try:
        # Get date the system has been up since
        proc = run(['uptime', '-s'], stdout=PIPE, stderr=PIPE)
        if proc.returncode != 0:
            # Raise exception with error output if something went wrong
            stderr = proc.stderr.decode('utf-8')
            raise Exception(f'Non-zero exit code: {stderr}')
        else:
            # Return the date output
            stdout = proc.stdout.decode('utf-8')
            return stdout.strip()
    except Exception as e:
        raise Exception(f'Failed to get start time: {e}')

def get_end():
    try:
        # Get the system has been up until (current time)
        return datetime.today().strftime(UPTIME_DATE_FORMAT)
    except Exception as e:
        raise Exception(f'Failed to get end time: {e}')

def get_uptime():
    try:
        # Get uptime in time the system has been up
        proc = run(['uptime', '-p'], stdout=PIPE, stderr=PIPE)
        if proc.returncode != 0:
            # Raise exception with error output if something went wrong
            stderr = proc.stderr.decode('utf-8')
            raise Exception(f'Non-zero exit code: {stderr}')
        else:
            # Return the time output
            stdout = proc.stdout.decode('utf-8')
            return stdout.strip()
    except Exception as e:
        raise Exception(f'Failed to get uptime: {e}')

def format_line(start, end, uptime):
    try:
        # Format values into csv line
        values = []
        for value in [start, end, uptime]:
            # Delete separator strings from values
            values.append(str(value).replace(CSV_SEPARATOR, ''))

        # Return values in csv line format
        return CSV_SEPARATOR.join(values)
    except Exception as e:
        raise Exception(f'Failed to format uptime: {e}')

def read_previous_lines():
    try:
        # Read csv values of previous uptimes
        if path.exists(UPTIME_CSV):
            # If there are previous runs, return all but the last (current)
            with open(UPTIME_CSV, 'r') as f:
                return f.read().strip().split('\n')[0:-1]
        else:
            # If first run, return empty list
            return []
    except Exception as e:
        raise Exception(f'Failed to read uptimes: {e}')

def write_line(line, overwriting):
    try:
        # Write csv line to file
        if overwriting:
            # If overwriting current line in fule
            # Get previous lines and append current line
            lines = read_previous_lines()
            lines.append(line)

            # Write lines to file
            with open(UPTIME_CSV, 'w') as f:
                f.write('\n'.join(lines) + '\n')
        else:
            # If not overwriting current line, simply append line to the end
            with open(UPTIME_CSV, 'a') as f:
                f.write(line + '\n')
    except Exception as e:
        raise Exception(f'Failed to write uptime: {e}')

try:
    # Overwriting flag, starts as false as there is nothing to overwrite
    # Gets set to true after first write
    overwriting = False
    log(f'Monitoring started!')

    while 1:
        formatted = None
        
        try:
            # Try getting the formatted csv line
            formatted = format_line(get_start(), get_end(), get_uptime())
        except Exception as e:
            # If something fails, simply try again next iteration
            log(f'Error: {e}')

        # If formatted line obtained successfully, write it
        if formatted is not None:
            write_line(formatted, overwriting)
            # Set flag
            if not overwriting:
                overwriting = True

        sleep(MONITOR_INTERVAL_S)
except Exception as e:
    log('Critical error: {e}')