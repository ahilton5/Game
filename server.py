#!/usr/bin/python3

from bottle import route, run, template, static_file, request, get, response, redirect
from time import sleep
import numpy as np
import webbrowser
import argparse
import json
import IPy
import sys
import os

# Constants
PLAYING = 1
PAUSED = 0
DONE = 2
LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3


states = {}
states['unclaimed'] = 0
states['blue'] = 1
states['blue_tail'] = 2
states['blue_current'] = 3
states['blue_current_tail'] = 4
states['green'] = 5
states['green_tail'] = 6
states['green_current'] = 7
states['green_current_tail'] = 8

pos = {}
pos['blue'] = (9, 2)
pos['green'] = (9, 47)

# Global variables
game_state = PAUSED
nrows = 20
ncols = 50
board = np.zeros((nrows, ncols))
for row in range(8, 11):
    for col in range(1, 4):
        board[row, col] = states['blue']
for row in range(8, 11):
    for col in range(46, 49):
        board[row, col] = states['green']
board[pos['blue']] = states['blue_current']
board[pos['green']] = states['green_current']

@route('/')
def index():
    return template('web_files/index', board=board, states=states)

@route('/move')
def move():
    player = request.query.color
    if player not in set('blue', 'green'):
        return redirect("/")
    direction = request.query.direction
    if direction not in set('left', 'right', 'up', 'down'):
        return redirect("/")
    if direction == 'left':
        row = pos[player][0]
        col = pos[player][1]
        pos[player] = (row, (col - 1) % ncols)
    elif direction == 'up':
        pass
    elif direction == 'right':
        pass
    elif direction == 'down':
        pass

# @route('/delete_host')
# def delete_host():
#     if started:
#         alerts.append("The scan has already started. To restart or terminate the scan, terminate the python script.")
#         return redirect("/")
#     host = request.query.hostNum
#     del scans[int(host)]
#     return redirect("/")

# # Handle so that the javascript can update the progress bar.
# @route('/progress')
# def get_progress():
#     response.content_type = 'application/json'
#     if not finished:
#         total = 0
#         for scan in scans:
#             total += len(scan['hosts']) * len(scan['ports'])
#         if total != 0:
#             return json.dumps({'progress': progress*100//total})
#         else:
#             return 0
#     else:
#         return json.dumps({'progress': 'DONE'})

# Only allow requests for files inside web_files directory.
allowed_files = set()
allowed_files.update(os.listdir('web_files'))

# Default file handler
@route('/:filename#.*#')
def serve_frontend(filename):
    if filename not in allowed_files:
        return redirect("/")
    else:
        return static_file(filename, os.getcwd() + "/web_files/")

if __name__ == "__main__":
    print('Program is listening on http://localhost:8088.',file=sys.stderr)
    run(host='localhost', port=8088, quiet=True)
    # with open('web_files/main.css', 'r') as f:
    #     style = "<style>" + f.read() + "</style>"
    # if args.host == '' or args.ports == '':
    #     print('Program is listening on http://localhost:8088.',file=sys.stderr)
    #     run(host='localhost', port=8088, quiet=True)
    # else:
    #     ports = parsePorts(args.ports)
    #     scans.append({'hosts': [args.host], 'hostStr': args.host, 'ports': ports, 'protocol': 'TCP'})
    #     runScan()
