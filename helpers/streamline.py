import os
import sys
from subprocess import Popen, PIPE
import datetime
import psutil
import time
from re import split, search


def listen_stream(hashtags, run_mode='normal'):
    """
    run_mode:
    - background: nothing is printed into console, runs as background process
    - normal: you get output into console, not a background process
    """

    token = ''
    token_secret = ''
    consumer_key = ''
    consumer_secret = ''

    location = os.path.dirname(os.path.realpath(__file__))
    args = []

    if 'background' in run_mode:
        args.append('nohup')

    args.extend(('python',
                location + '/../utils/open_stream.py',
                '-t=' + token,
                '-ts=' + token_secret,
                '-ck=' + consumer_key,
                '-cs=' + consumer_secret,
                '-tt=' + hashtags))

    process = Popen(args)
    pid = process.pid
    return pid

def get_open_streams():
    """
    Retrieves a list [] of Proc objects representing the active
    process list list
    """

    proc_list = []
    sub_proc = Popen(['ps', 'aux'], shell=False, stdout=PIPE)

    for line in sub_proc.stdout:
         if 'open_stream.py' in line:
            # Get hashtag from line
            hashtags = search('-tt=(.*)$', line).group(1)

            # The separator for splitting is 'variable number of spaces'
            proc_info = split(" *", line.strip())
            proc_list.append({
                'user': proc_info[0],
                'pid': proc_info[1],
                'cpu': proc_info[2],
                'mem': proc_info[3],
                'vsz': proc_info[4],
                'rss': proc_info[5],
                'tty': proc_info[6],
                'stat': proc_info[7],
                'start': proc_info[8],
                'time': proc_info[9],
                'cmd': proc_info[10],
                'hashtags': hashtags
            })

    return proc_list

def kill_stream(pid=None):
    sub_proc = Popen(['kill', '-9', pid], shell=False, stdout=PIPE, stderr=PIPE)

    stderr = sub_proc.stderr.read()
    stdout = sub_proc.stdout.read()

    if stderr:
        return 'Process "%s" does not exist!' % pid
    else:
        return 'Process "%s" killed!' % pid


"""
TODOS:
- only one stream can be opened per token key / consumer (check which!)
- if stream already opened, don't make another one
- error logging & put silen output into log files also
"""
