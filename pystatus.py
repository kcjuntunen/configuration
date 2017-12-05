#!/usr/bin/python3
"""
Create status output for sway.
"""

import sys
import json
import subprocess
import re
import colorsys
from datetime import datetime
from time import sleep
from scipy import interp

VERSION = {'version': 1}
LOADAVGFILE = '/proc/loadavg'
MEMFILE = '/proc/meminfo'
OK_CLR = '#55ff55ff'
WARN_CLR = '#ffff55ff'
ALERT_CLR = '#ff5555ff'
NORMAL_CLR = '#ffffffff'
BACKGROUND_CLR = '#292b2eff'


def get_load_avg():
    """
    Return the load avg.
    """
    with open(LOADAVGFILE, 'r') as la_fh:
        line = la_fh.readline()
        loadavg = float(line.split(' ')[0])
        color = NORMAL_CLR
        interp_val = interp(loadavg, [0, 4], [1/3, 0])
        color = hsv_rgbhex((interp_val, 1.0, 1))
        return {'full_text': "Load: {0:.2f}".format(loadavg),
                'background': BACKGROUND_CLR,
                'color': color}


def hsv_rgbhex(hsv):
    """
    Convert HSV values to RGB hex.
    """
    hexstr = '#'
    for num in colorsys.hsv_to_rgb(*hsv):
        val = num * 256
        if val > 255:
            val = 255
        hexstr += '{0:02x}'.format(int(val))
    return hexstr + 'ff'


def get_acpi():
    """
    Return acpi status.
    """
    output = subprocess.check_output(['acpi', '-i']).decode('utf-8')
    status = output.split()
    charging = status[2].split(',')[0]
    full_text = output.split('\n')[0].split(',')[2].strip()
    percentstr = status[3].split('%')[0]
    if percentstr == '':
        percentstr = '0'
    percent = float(percentstr)

    interp_val = interp(percent, [0, 100], [0, 1/3])
    color = hsv_rgbhex((interp_val, 1.0, 1))

    if 'Dis' not in charging:
        color = OK_CLR

    return {'full_text':
            "({0:.0f}%) {1}".format(percent, full_text),
            'background': BACKGROUND_CLR,
            'color': color}



def get_volume():
    """
    Return volume level.
    """
    output = subprocess.check_output(['amixer', 'get', 'Master'])
    line = output.decode("utf-8").split('\n')[5]
    regx = re.compile(r'\d*\%')
    mtch = regx.findall(line)
    status = mtch[0]
    muted = 'off' in line
    interp_val = interp(float(status[:-1]), [0, 100], [2/3, 1/3])
    color = hsv_rgbhex((interp_val, 1.0, 1))
    if muted:
        color = hsv_rgbhex((interp_val, 0.6, 0.5))

    return {'full_text': 'Vol: {}'.format(status),
            'background': BACKGROUND_CLR,
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
            return {'full_text': 'Home: {0}'.format(freespace),
                    'background': BACKGROUND_CLR, 'color': NORMAL_CLR}


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
            'background': BACKGROUND_CLR,
            'color': color}


def get_time():
    """
    Return formatted time.
    """
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    return {'full_text': '{}'.format(now),
            'background': BACKGROUND_CLR,
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
