#!/usr/bin/python3
"""
Create status output for sway.
"""

import sys
import json
import subprocess
from datetime import datetime
from time import sleep

VERSION = {'version': 1}
LOADAVGFILE = '/proc/loadavg'
MEMFILE = '/proc/meminfo'
OK_CLR = '#55ff55'
WARN_CLR = '#ffff55'
ALERT_CLR = '#ff5555'
NORMAL_CLR = '#ffffff'


def get_load_avg():
    """
    Return the load avg.
    """
    with open(LOADAVGFILE, 'r') as la_fh:
        line = la_fh.readline()
        loadavg = float(line.split(' ')[0])
        color = NORMAL_CLR
        if loadavg > 3:
            color = WARN_CLR

        if loadavg > 4:
            color = ALERT_CLR
        return {'full_text': "Load: {0:.2f}".format(loadavg),
                'color': color}

def get_acpi():
    """
    Return acpi status.
    """
    status = subprocess.check_output(['acpi', '-i']).split()
    charging = status[2].decode('utf-8').split(',')[0]
    percent = float(status[3].decode('utf-8').split('%')[0])
    color = NORMAL_CLR
    if percent < 55:
        color = WARN_CLR

    if percent < 50:
        color = ALERT_CLR

    if 'Dis' not in charging:
        color = OK_CLR

    return {'full_text':
            "{0}: {1:.0f}%".format(charging, percent),
            'color': color}


def get_volume():
    """
    Return volume level.
    """
    output = subprocess.check_output(['amixer', 'get', 'Master'])
    line = output.decode("utf-8").split('\n')[5]
    status = line.split()[4]
    muted = 'off' in line
    color = NORMAL_CLR
    if muted:
        color = WARN_CLR
    return {'full_text': 'Vol: {}'.format(status),
            'color': color}


def get_free_hd():
    """
    Return free hd space.
    """
    output = subprocess.check_output(['df', '-h'])
    lines = output.decode("utf-8").split('\n')
    for line in lines:
        if 'home' in line:
            freespace = line.split()[3]
            return {'full_text': 'Home: {0}'.format(freespace), 'color': NORMAL_CLR}


def get_free_ram():
    """
    Return free memory.
    """
    freemem = 0
    freeswap = 0
    color = NORMAL_CLR
    with open(MEMFILE, 'r') as mem_fh:
        for line in mem_fh.readlines():
            if 'MemFree' in line:
                freemem = int(line.split()[1])
            if 'SwapFree' in line:
                freeswap = int(line.split()[1])
    return {'full_text': 'RAM: {}M Swap: {}M'.format(freemem // 1024, freeswap // 1024),
            'color': color}


def get_time():
    """
    Return formatted time.
    """
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    return {'full_text': '{}'.format(now),
            'color': NORMAL_CLR}


if __name__ == "__main__":
    LOOP = True
    DELAY = 30
    if len(sys.argv) > 1:
        DELAY = int(sys.argv[1])
    else:
        LOOP = False

    print(json.dumps(VERSION))
    print("[")
    print("[]")
    while True:
        STAT = [get_volume(), get_free_hd(), get_free_ram(),
                get_load_avg(), get_acpi(), get_time(),]
        print(",{0}".format(json.dumps(STAT)))
        sys.stdout.flush()
        if not LOOP:
            break
        sleep(DELAY)
    print("]")
