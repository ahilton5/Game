from pprint import pprint
import requests 
import random
import time

from SimulatedAnnealing import SimulatedAnnealing


# globals
board = None
anneal = None
nrows = 20
ncols = 50

BLUE_PLAYER = 0
GREEN_PLAYER = 1

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

steps = {0: 'up', 1: 'right', 2: 'down', 3: 'left'}
col = 0
row = 0

def player_score(player):
    score = 0
    for row in range(nrows):
        for col in range(ncols):
            if board[col][row] == states[player] or board[col][row] == states[player + '_current']:
                score += 1
    return score


def isRunning():
    return requests.get('http://localhost:8088/is_running').json()['running']


sleeptime = requests.get('http://localhost:8088/nseconds').json()['nseconds']


def sync():
    global board
    board = requests.get('http://localhost:8088/sync').json()['board']
    for c in range(ncols):
        for r in range(nrows):
            if board[c][r] == states['blue_current_tail'] or board[c][r] == states['blue_current']:
                col = c
                row = c

def get_move():
    anneal = SimulatedAnnealing(BLUE_PLAYER, board)
    # pprint(board)
    return  steps[anneal.anneal(board, time_allowance=sleeptime)]

    # return random.choice(['left', 'right', 'up', 'down'])


def change_dir(direction):
    params = {'player': 'blue', 'direction': direction}
    board = requests.get(url='http://localhost:8088/change_dir', params=params).json()['board']


while True:
    if isRunning():
        sync()
        # print(f'Green\'s score: {player_score("green")}')
        # print(f'Blue (AI)\'s score: {player_score("blue")}')
        change_dir(get_move())
    # time.sleep(sleeptime)
