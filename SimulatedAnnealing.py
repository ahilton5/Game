from random import randint, random
import math
import time

U = 0
R = 1
D = 2
L = 3


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
                    while next_move == solution[i-1]:
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
                        while next_move == solution[i - 1]:
                            next_move = randint(0, 3)
                    else:
                        while next_move == prev:
                            next_move = randint(0, 3)

                solution.append(next_move)

        return solution

    def cost(self, solution):
        # TODO: Implement
        for step in solution:
            self.state.apply_step(step, self.me)

        # factor 1: your area vs opponents area
        score = self.state.score(self.me)

        # factor 2: how close is the opponent to your trail

        # factor 3: how close are you to your opponents trail

        return score

    def anneal(self, board=None, time_allowance=1.0):
        # Simulated annealing!!
        results = {}
        if board:
            self.set_board(board)
        self.prev = self.state.get_prev(self.me)
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
                        self.b_score += 1

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

            if self.board[pos[0]][pos[1] - 1] == check:
                return U
            if self.board[pos[0]][pos[1] + 1] == check:
                return D
            if self.board[pos[0] - 1][pos[1]] == check:
                return L
            if self.board[pos[0] + 1][pos[1]] == check:
                return R

        def score(self, player):
            if player == self.BLUE_PLAYER:
                return self.b_score-self.g_score
            return self.g_score-self.b_score

        def apply_step(self, step, player):
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
                    pos[1] = (pos[1] + 1) % len(self.board[0])
                elif step == D:
                    pos[1] = (pos[1] - 1) % len(self.board[0])
                elif step == R:
                    pos[0] = (pos[0] + 1) % len(self.board)
                else:
                    pos[0] = (pos[0] - 1) % len(self.board)

                if self.board[pos[0]][pos[1]] == color:
                    self.board[pos[0]][pos[1]] = current

            else:
                self.board[pos[0]][pos[1]] = tail

                if step == U:
                    pos[1] = (pos[1] + 1) % len(self.board[0])
                elif step == D:
                    pos[1] = (pos[1] - 1) % len(self.board[0])
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

        def erase(self, player):
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

        def paint(self, player):
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



