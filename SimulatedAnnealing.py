from random import randint, random
import math
import time

U = 0
R = 1
D = 2
L = 3

nrows = 20
ncols = 50

steps = {0: 'up', 1: 'right', 2: 'down', 3: 'left'}

class SimulatedAnnealing:

    def __init__(self, me, board):
        self.num_moves = 5
        self.walk_chance = 0.5
        self.me = me
        self.state = self.State(board)
        self.prev = self.state.get_prev(self.me)

    def set_board(self, board):
        self.state.set_board(board)

    # do a random series of x moves
    def random_solution(self, prev, current=None):
        solution = []
        if not current:
            for i in range(self.num_moves):
                next_move = randint(0, 3)
                # choose a move that is not backwards
                if i:
                    while next_move == (solution[i-1] + 2) % 4:
                        next_move = randint(0, 3)
                else:
                    while next_move == prev:
                        next_move = randint(0, 3)

                solution.append(next_move)

        else:
            for i in range(len(current)):
                next_move = current[i]

                if random() < self.walk_chance:
                    next_move = randint(0, 3)
                    # choose a move that is not backwards
                    if i:
                        while next_move == (solution[i-1] + 2) % 4:
                            next_move = randint(0, 3)
                    else:
                        while next_move == prev:
                            next_move = randint(0, 3)

                solution.append(next_move)

        return solution

    def cost(self, solution):
        # TODO: Implement
        for step in solution:
            # self.state.apply_step(step, self.me)
            BLUE_PLAYER = 0
            GREEN_PLAYER = 1
            if self.me == BLUE_PLAYER:
                self.state.advance(step, 'blue')
            else:
                self.state.advance(step, 'green')

        # factor 1: your area vs opponents area
        score = self.state.score(self.me)

        # factor 2: how close is the opponent to your trail

        # factor 3: how close are you to your opponents trail

        return score

    def anneal(self, board=None, time_allowance=0.1):
        # Simulated annealing!!
        results = {}
        if board:
            self.set_board(board)
        # self.prev = self.state.get_prev(self.me)
        # if self.prev:
            # print(f"\nprevious = {steps[self.prev]}")
        num_solutions = 0
        # Just copied the values off one of the tutorials for the initial temp and cooling rate;
        # feel free to play with these
        temp = 10000.0
        # .0003 was good for < 100 cities, use .00003 for larger problem sizes.
        cooling_rate = 0.0003

        bssf = self.random_solution(self.prev)
        current = bssf
        start_time = time.time()

        while temp > 1 and (time.time() - start_time <= time_allowance):
            candidate = self.random_solution(current)
            prob = self.calculate_acceptance_probability(self.cost(current), self.cost(candidate), temp)

            # If the returned probability is greater than a random number between 0 and 1, this is our new current route
            if random() < prob:
                current = candidate

            if self.cost(current) < self.cost(bssf):
                # This is our new bssf
                bssf = current
                num_solutions += 1

            temp *= 1 - cooling_rate

        # end_time = time.time()
        # results['cost'] = bssf.cost
        # results['time'] = end_time - start_time
        # results['count'] = num_solutions
        # results['soln'] = bssf
        # results['max'] = None
        # results['total'] = None
        # results['pruned'] = None

        i = 0
        while not self.state.checkmove(bssf[0], self.me) and i < 4:
            bssf[0] = (bssf[0] + 1) % 4
            i += 1

        # if i < 4:
        #     print(f"{steps[bssf[0]]} is a good move")
        # else:
        #     print(f"{steps[bssf[0]]} is a BAD move")

        self.prev = (bssf[0] + 2) % 4
        return bssf[0]

    # This calculates the odds that we'll accept this
    @staticmethod
    def calculate_acceptance_probability(old_cost, new_cost, temp):
        if new_cost < old_cost:
            # If new route is cheaper, accept no matter what (return 100% chance of acceptance)
            return 1.0
        # There's still a chance we'll accept this, if the temp is high (I got this probability formula from one of the
        # online tutorials)
        ratio = (old_cost - new_cost) / temp
        prob = math.exp(ratio)
        return prob

    class State:

        def __init__(self, board):
            self.states = {'unclaimed': 0, 'blue': 1, 'blue_tail': 2, 'blue_current': 3, 'blue_current_tail': 4,
                           'green': 5, 'green_tail': 6, 'green_current': 7, 'green_current_tail': 8}

            self.BLUE_PLAYER = 0
            self.GREEN_PLAYER = 1

            self.board = board.copy()
            self.b_score = 0
            self.g_score = 0
            self.b_pos = [0, 0]
            self.g_pos = [0, 0]

            self.set_board(board)

        def checkmove(self, move, player):
            if player == self.BLUE_PLAYER:
                pos = self.b_pos
                check = self.states['blue_tail']
            else:
                pos = self.g_pos
                check = self.states['green_tail']

            if move == U and self.board[pos[0]][(pos[1] - 1) % len(self.board[0])] == check:
                return False
            if move == D and self.board[pos[0]][(pos[1] + 1) % len(self.board[0])] == check:
                return False
            if move == R and self.board[(pos[0] + 1) % len(self.board)][pos[1]] == check:
                return False
            if move == L and self.board[(pos[0] - 1) % len(self.board)][pos[1]] == check:
                return False

            return True

        def set_board(self, board):
            self.board = board.copy()

            for x in range(len(self.board)):
                row = self.board[x]
                for y in range(len(row)):
                    if self.board[x][y] == self.states['blue'] \
                            or self.board[x][y] == self.states['blue_current']:
                        self.b_score += 1
                    elif self.board[x][y] == self.states['green'] \
                            or self.board[x][y] == self.states['green_current']:
                        self.g_score += 1

                    if self.board[x][y] == self.states['blue_current_tail'] \
                            or self.board[x][y] == self.states['blue_current']:
                        self.b_pos = [x, y]

                    if self.board[x][y] == self.states['green_current_tail'] \
                            or self.board[x][y] == self.states['green_current']:
                        self.g_pos = [x, y]

        def get_prev(self, player):
            if player == self.BLUE_PLAYER:
                pos = self.b_pos
                check = self.states['blue_tail']
            else:
                pos = self.g_pos
                check = self.states['green_tail']

            if self.board[pos[0]][(pos[1] - 1) % len(self.board[0])] == check:
                return U
            if self.board[pos[0]][(pos[1] + 1) % len(self.board[0])] == check:
                return D
            if self.board[(pos[0] - 1) % len(self.board)][pos[1]] == check:
                return L
            if self.board[(pos[0] + 1) % len(self.board)][pos[1]] == check:
                return R

        def score(self, player):
            if player == self.BLUE_PLAYER:
                return self.b_score-self.g_score
            return self.g_score-self.b_score

        # def apply_step(self, step, player):
            if player == self.BLUE_PLAYER:
                color = self.states['blue']
                pos = self.b_pos
                current = self.states['blue_current']
                current_tail = self.states['blue_current_tail']
                tail = self.states['blue_tail']
            else:
                color = self.states['green']
                pos = self.g_pos
                current = self.states['green_current']
                current_tail = self.states['green_current_tail']
                tail = self.states['green_tail']

            if self.board[pos[0]][pos[1]] == current:
                self.board[pos[0]][pos[1]] = color

                if step == U:
                    pos[1] = (pos[1] - 1) % len(self.board[0])
                elif step == D:
                    pos[1] = (pos[1] + 1) % len(self.board[0])
                elif step == R:
                    pos[0] = (pos[0] + 1) % len(self.board)
                else:
                    pos[0] = (pos[0] - 1) % len(self.board)

                if self.board[pos[0]][pos[1]] == color:
                    self.board[pos[0]][pos[1]] = current

            else:
                self.board[pos[0]][pos[1]] = tail

                if step == U:
                    pos[1] = (pos[1] - 1) % len(self.board[0])
                elif step == D:
                    pos[1] = (pos[1] + 1) % len(self.board[0])
                elif step == R:
                    pos[0] = (pos[0] + 1) % len(self.board)
                else:
                    pos[0] = (pos[0] - 1) % len(self.board)

                if self.board[pos[0]][pos[1]] == color:
                    self.paint(player)
                    self.board[pos[0]][pos[1]] = current

            if self.board[pos[0]][pos[1]] == self.states['unclaimed']:
                self.board[pos[0]][pos[1]] = current_tail

            if self.board[pos[0]][pos[1]] == self.states['green_tail']:
                self.erase(self.GREEN_PLAYER)
            elif self.board[pos[0]][pos[1]] == self.states['blue_tail']:
                self.erase(self.BLUE_PLAYER)

        # def erase(self, player):
            if player == self.BLUE_PLAYER:
                color = self.states['blue']
                pos = self.b_pos
                self.b_score = 9
            else:
                color = self.states['green']
                pos = self.g_pos
                self.g_score = 9

            for x in self.board:
                for y in x:
                    if y == color or y == color+1:
                        y = self.states['unclaimed']

            for x in range(-1, 2):
                for y in range(-1, 2):
                    if 0 <= pos[0]+x < len(self.board) and 0 <= pos[1]+y < len(self.board[0]):
                        self.board[pos[0]+x][pos[1]+y] = color

            self.board[pos[0]][pos[1]] = color+2

        # def paint(self, player):
            if player == self.BLUE_PLAYER:
                paint = self.states['blue']
                check = self.states['blue_tail']
                score = self.b_score
            else:
                paint = self.states['green']
                check = self.states['green_tail']
                score = self.g_score

            for x in range(len(self.board)):
                row = self.board[x]
                for y in range(len(row)):
                    if self.board[x][y] == check:
                        self.board[x][y] = paint
                        score += 1

                    elif self.board[x][y] == self.states['unclaimed']:
                        # check up
                        for y1 in range(y, 0):
                            if self.board[x][y1] == paint\
                                    or self.board[x][y1] == check:

                                # check down
                                for y2 in range(y+1, len(self.board[x])):
                                    if self.board[x][y2] == paint \
                                            or self.board[x][y2] == check:

                                        # check right
                                        for x1 in range(x, 0):
                                            if self.board[x1][y] == paint \
                                                    or self.board[x1][y] == check:

                                                # check left
                                                for x2 in range(x, len(self.board)):
                                                    if self.board[x2][y] == paint \
                                                            or self.board[x2][y] == check:
                                                        self.board[x][y] = paint
                                                        score += 1
                                                        break
                                                break
                                        break
                                break

            if player == self.BLUE_PLAYER:
                self.b_score = score
            else:
                self.g_score = score



        def enclosed(self, col, row, player, depth):
            enclosedUp = False
            enclosedRight = False
            enclosedLeft = False
            enclosedDown = False
            if depth > 4:
                return True
            
            # Enclosed right
            for c in range(col, ncols):
                if self.board[c][row] == self.states[player] or self.board[c][row] == self.states[player + '_tail'] or self.board[c][row] == self.states[player + '_current'] or self.board[c][row] == self.states[player + '_current_tail']:
                    enclosedRight = self.enclosed(c, row, player, depth + 1)
                    break   
            if not enclosedRight:
                return False

            # Enclosed left
            for c in range(col, -1, -1):
                if self.board[c][row] == self.states[player] or self.board[c][row] == self.states[player + '_tail'] or self.board[c][row] == self.states[player + '_current'] or self.board[c][row] == self.states[player + '_current_tail']:
                    enclosedLeft = self.enclosed(c, row, player, depth + 1)
                    break   
            if not enclosedLeft:
                return False

            # Enclosed up
            for r in range(row, nrows):
                if self.board[col][r] == self.states[player] or self.board[col][r] == self.states[player + '_tail'] or self.board[col][r] == self.states[player + '_current'] or self.board[col][r] == self.states[player + '_current_tail']:
                    enclosedUp = self.enclosed(col, r, player, depth + 1)
                    break    
            if not enclosedUp:
                return False

            # Enclosed down
            for r in range(row, -1, -1):
                if self.board[col][r] == self.states[player] or self.board[col][r] == self.states[player + '_tail'] or self.board[col][r] == self.states[player + '_current'] or self.board[col][r] == self.states[player + '_current_tail']:
                    enclosedDown = self.enclosed(col, r, player, depth + 1)
                    break   
            if not enclosedDown:
                return False

            return enclosedDown and enclosedLeft and enclosedRight and enclosedUp

        def claim(self, player):
            tail = set()
            for row in range(nrows):
                for col in range(ncols):
                    if self.enclosed(col, row, player, 1):
                        self.board[col][row] = self.states[player]
                    if self.board[col][row] == self.states[player + '_tail']:
                        self.board[col][row] = self.states[player]
            b_score = 0
            g_score = 0
            for r in range(nrows):
                for c in range(ncols):
                    if self.board[c][r] == self.states['blue'] or self.board[c][r] == self.states['blue_current']:
                        b_score += 1
                    if self.board[c][r] == self.states['green'] or self.board[c][r] == self.states['green_current']:
                        g_score += 1
            self.b_score = b_score
            self.g_score = g_score

        def regenerate(self, player):
            for row in range(nrows):
                for col in range(ncols):
                    if self.board[col][row] == self.states[player]:
                        self.board[col][row] = self.states['unclaimed']
                    elif self.board[col][row] == self.states[player + '_tail']:
                        self.board[col][row] = self.states['unclaimed']
                    elif self.board[col][row] == self.states[player + '_current']:
                        self.board[col][row] = self.states['unclaimed']
                    elif self.board[col][row] == self.states[player + '_current_tail']:
                        self.board[col][row] = self.states['unclaimed']
                    
            random_col = randint(1, 48)
            randow_row = randint(1, 18)
            for col in range(random_col - 1, random_col + 2):
                for row in range(randow_row - 1, randow_row + 2):
                    self.board[col][row] = self.states[player]
            self.board[random_col][randow_row] = self.states[player + '_current']
            if player == 'green':
                self.g_pos = [random_col, randow_row]
                self.g_score = 9
            else:
                self.b_pos = [random_col, randow_row]
                self.b_score = 9

        def other(self, player):
            return 'green' if player == 'blue' else 'blue'

        def advance(self, step, player):
            if player == 'green':
                pos = self.g_pos
            else:
                pos = self.b_pos
            direction = steps[step]
            # Set state of old spot
            last_pos = self.board[pos[0]][pos[1]]
            if self.board[pos[0]][pos[1]] == self.states[player + '_current']:
                self.board[pos[0]][pos[1]] = self.states[player]
            else:
                self.board[pos[0]][pos[1]] = self.states[player + '_tail']

            # Move to new spot
            if direction == 'left':
                col = pos[0]
                row = pos[1]
                pos = [(col - 1) % ncols, row]
            elif direction == 'up':
                col = pos[0]
                row = pos[1]
                pos = [col, (row - 1) % nrows]
            elif direction == 'right':
                col = pos[0]
                row = pos[1]
                pos = [(col + 1) % ncols, row]
            elif direction == 'down':
                row = pos[1]
                col = pos[0]
                pos = [col, (row + 1) % nrows]

            # Set state of new spot
            if self.board[pos[0]][pos[1]] == self.states[player + '_tail']:
                # You ran over your own tail
                self.regenerate(player)
            if self.board[pos[0]][pos[1]] == self.states[self.other(player) + '_tail'] or self.board[pos[0]][pos[1]] == self.states[self.other(player) + '_current_tail']:
                # You ran over your opponent
                self.regenerate(self.other(player))
            if self.board[pos[0]][pos[1]] == self.states[player]:
                if last_pos != self.states[player + '_current']:
                    self.claim(player)
                self.board[pos[0]][pos[1]] = self.states[player + '_current']
            else:
                self.board[pos[0]][pos[1]] = self.states[player + '_current_tail']

            if player == 'green':
                self.g_pos = pos
            else:
                self.b_pos = pos
