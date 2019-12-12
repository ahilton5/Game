#!/usr/bin/python3

from bottle import route, run, template, static_file, request, get, response, redirect
from threading import Thread
from time import sleep
# import webbrowser
import argparse
import random
import json
import sys
import os

# Set up command-line instructions
parser = argparse.ArgumentParser()
parser.add_argument('--nseconds', help='The number of seconds between turns. Defaults to 0.2.', default=0.2, type=float)
args = parser.parse_args()

PLAYING = 1
PAUSED = -1

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
pos['blue'] = (2, 9)
pos['green'] = (47, 9)
dirs = {}
dirs['blue'] = 'right'
dirs['green'] = 'left'

# Global variables
game_state = PAUSED
nrows = 20
ncols = 50
board = [[0 for _ in range(nrows)] for _ in range(ncols)]
for row in range(8, 11):
    for col in range(1, 4):
        board[col][row] = states['blue']
for row in range(8, 11):
    for col in range(46, 49):
        board[col][row] = states['green']
board[pos['blue'][0]][pos['blue'][1]] = states['blue_current']
board[pos['green'][0]][pos['green'][1]] = states['green_current']

@route('/')
def index():
    return template('web_files/index', board=board, states=states)

@route('/is_running')
def is_running():
    return json.dumps({'running': game_state == PLAYING})

@route('/sync')
def sync():
    response.content_type = 'application/json'
    return json.dumps({'board': board})

@route('/nseconds')
def nseconds():
    response.content_type = 'application/json'
    return json.dumps({'nseconds': args.nseconds})

@route('/pause')
def pause():
    global game_state
    game_state *= -1

@route('/change_dir')
def change_dir():
    response.content_type = 'application/json'
    player = request.query.player
    if player not in ['blue', 'green']:
       return json.dumps({'board': board})
    direction = request.query.direction
    if direction not in ['left', 'right', 'up', 'down']:
        return json.dumps({'board': board})
    dirs[player] = direction
    return json.dumps({'board': board})

@route('/reset')
def reset():
    global board, pos, dirs, game_state
    game_state = PAUSED
    pos['blue'] = (2, 9)
    pos['green'] = (47, 9)
    dirs['blue'] = 'right'
    dirs['green'] = 'left'
    board = [[0 for _ in range(nrows)] for _ in range(ncols)]
    for row in range(8, 11):
        for col in range(1, 4):
            board[col][row] = states['blue']
    for row in range(8, 11):
        for col in range(46, 49):
            board[col][row] = states['green']
    board[pos['blue'][0]][pos['blue'][1]] = states['blue_current']
    board[pos['green'][0]][pos['green'][1]] = states['green_current']
    return redirect("/")

def enclosed(col, row, player, depth):
    enclosedUp = False
    enclosedRight = False
    enclosedLeft = False
    enclosedDown = False
    if depth > 4:
        return True
    
    # Enclosed right
    for c in range(col, ncols):
        if board[c][row] == states[player] or board[c][row] == states[player + '_tail'] or board[c][row] == states[player + '_current'] or board[c][row] == states[player + '_current_tail']:
            enclosedRight = enclosed(c, row, player, depth + 1)
            break   
    if not enclosedRight:
        return False

    # Enclosed left
    for c in range(col, -1, -1):
        if board[c][row] == states[player] or board[c][row] == states[player + '_tail'] or board[c][row] == states[player + '_current'] or board[c][row] == states[player + '_current_tail']:
            enclosedLeft = enclosed(c, row, player, depth + 1)
            break   
    if not enclosedLeft:
        return False

    # Enclosed up
    for r in range(row, nrows):
        if board[col][r] == states[player] or board[col][r] == states[player + '_tail'] or board[col][r] == states[player + '_current'] or board[col][r] == states[player + '_current_tail']:
            enclosedUp = enclosed(col, r, player, depth + 1)
            break    
    if not enclosedUp:
        return False

    # Enclosed down
    for r in range(row, -1, -1):
        if board[col][r] == states[player] or board[col][r] == states[player + '_tail'] or board[col][r] == states[player + '_current'] or board[col][r] == states[player + '_current_tail']:
            enclosedDown = enclosed(col, r, player, depth + 1)
            break   
    if not enclosedDown:
        return False

    return enclosedDown and enclosedLeft and enclosedRight and enclosedUp

def claim(player):
    tail = set()
    for row in range(nrows):
        for col in range(ncols):
            if enclosed(col, row, player, 1):
                board[col][row] = states[player]
            if board[col][row] == states[player + '_tail']:
                board[col][row] = states[player]
    
def regenerate(player):
    for row in range(nrows):
        for col in range(ncols):
            if board[col][row] == states[player]:
                board[col][row] = states['unclaimed']
            elif board[col][row] == states[player + '_tail']:
                board[col][row] = states['unclaimed']
            elif board[col][row] == states[player + '_current']:
                board[col][row] = states['unclaimed']
            elif board[col][row] == states[player + '_current_tail']:
                board[col][row] = states['unclaimed']
            
    random_col = random.randint(1, 48)
    randow_row = random.randint(1, 18)
    for col in range(random_col - 1, random_col + 2):
        for row in range(randow_row - 1, randow_row + 2):
            board[col][row] = states[player]
    board[random_col][randow_row] = states[player + '_current']
    pos[player] = (random_col, randow_row)

def other(player):
    return 'green' if player == 'blue' else 'blue'

def advance():
    while True:
        if game_state != PAUSED:
            players = ['blue', 'green']
            random.shuffle(players)
            for player in players:
                # Set state of old spot
                last_pos = board[pos[player][0]][pos[player][1]]
                if board[pos[player][0]][pos[player][1]] == states[player + '_current']:
                    board[pos[player][0]][pos[player][1]] = states[player]
                else:
                    board[pos[player][0]][pos[player][1]] = states[player + '_tail']

                # Move to new spot
                if dirs[player] == 'left':
                    col = pos[player][0]
                    row = pos[player][1]
                    pos[player] = ((col - 1) % ncols, row)
                elif dirs[player] == 'up':
                    col = pos[player][0]
                    row = pos[player][1]
                    pos[player] = (col, (row - 1) % nrows)
                elif dirs[player] == 'right':
                    col = pos[player][0]
                    row = pos[player][1]
                    pos[player] = ((col + 1) % ncols, row)
                elif dirs[player] == 'down':
                    row = pos[player][1]
                    col = pos[player][0]
                    pos[player] = (col, (row + 1) % nrows)

                # Set state of new spot
                if board[pos[player][0]][pos[player][1]] == states[player + '_tail']:
                    # You ran over your own tail
                    if player == 'blue':
                        # AI, so choose a different move
                        # First go back 
                        if dirs[player] == 'left':
                            col = pos[player][0]
                            row = pos[player][1]
                            pos[player] = ((col + 1) % ncols, row)
                        elif dirs[player] == 'up':
                            col = pos[player][0]
                            row = pos[player][1]
                            pos[player] = (col, (row + 1) % nrows)
                        elif dirs[player] == 'right':
                            col = pos[player][0]
                            row = pos[player][1]
                            pos[player] = ((col - 1) % ncols, row)
                        elif dirs[player] == 'down':
                            row = pos[player][1]
                            col = pos[player][0]
                            pos[player] = (col, (row - 1) % nrows)
                        # Choose a new move at random
                        options = ['right', 'up', 'down', 'left']
                        options.remove(dirs[player])
                        dirs[player] = random.choice(options)
                        # Move to new spot
                        if dirs[player] == 'left':
                            col = pos[player][0]
                            row = pos[player][1]
                            pos[player] = ((col - 1) % ncols, row)
                        elif dirs[player] == 'up':
                            col = pos[player][0]
                            row = pos[player][1]
                            pos[player] = (col, (row - 1) % nrows)
                        elif dirs[player] == 'right':
                            col = pos[player][0]
                            row = pos[player][1]
                            pos[player] = ((col + 1) % ncols, row)
                        elif dirs[player] == 'down':
                            row = pos[player][1]
                            col = pos[player][0]
                            pos[player] = (col, (row + 1) % nrows)
                        # Check if the new move is on your tail, if so, regenerate
                        if board[pos[player][0]][pos[player][1]] == states[player + '_tail']:
                            regenerate(player)
                    else:
                        regenerate(player)
                if board[pos[player][0]][pos[player][1]] == states[other(player) + '_tail'] or board[pos[player][0]][pos[player][1]] == states[other(player) + '_current_tail']:
                    # You ran over your opponent
                    regenerate(other(player))
                if board[pos[player][0]][pos[player][1]] == states[player]:
                    if last_pos != states[player + '_current']:
                        claim(player)
                    board[pos[player][0]][pos[player][1]] = states[player + '_current']
                else:
                    board[pos[player][0]][pos[player][1]] = states[player + '_current_tail']
        sleep(args.nseconds)


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
    Thread(target = advance).start()
    run(host='localhost', port=8088, quiet=True)

