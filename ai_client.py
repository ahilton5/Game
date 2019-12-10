import requests 
import random
import time

# globals
board = None
nrows = 20
ncols = 50
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

def player_score(player):
    score = 0
    for row in range(nrows):
        for col in range(ncols):
            if board[col][row] == states[player] or board[col][row] == states[player + '_current']:
                score += 1
    return score

def isRunning():
    return requests.get('http://localhost:8088/is_running').json()['running']
    
nseconds = requests.get('http://localhost:8088/nseconds').json()['nseconds']

def sync():
    global board
    board = requests.get('http://localhost:8088/sync').json()['board']

def get_move():
    # TODO
    return random.choice(['left', 'right', 'up', 'down'])

def change_dir(direction):
    params = {'player': 'blue', 'direction': direction}
    board = requests.get(url='http://localhost:8088/change_dir', params=params).json()['board']

while True:
    if isRunning():
        sync()
        print(f'Green\'s score: {player_score("green")}')
        print(f'Blue (AI)\'s score: {player_score("blue")}')
        change_dir(get_move())
    time.sleep(nseconds)