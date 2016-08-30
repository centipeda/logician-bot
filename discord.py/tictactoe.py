"""Tic-tac-toe model. AI assumes AI_SYMBOL. """
import copy
import random

AI_SYMBOL = "X"
OPPONENT_SYMBOL = "O"
BLANK_SYMBOL = "_"

def check_win(board):
    """Accepts a 3x3 iterable full of AI_SYMBOL, OPPONENT_SYMBOL, or BLANK_SYMBOL characters.
    Returns 10 if AI_SYMBOL would have won, -10 if OPPONENT_SYMBOL would have won, 0 if the board is full and resulted in a draw, and None if the game hasnot finished yet."""
    winConditions = [board[0], # rows
                    board[1],
                    board[2],
                    [board[0][0],board[1][0],board[2][0]], # columns
                    [board[0][1],board[1][1],board[2][1]],
                    [board[0][2],board[1][2],board[2][2]],
                    [board[0][0],board[1][1],board[2][2]], # diagonals
                    [board[0][2],board[1][1],board[2][0]]]

    for winCondition in winConditions:
        if winCondition == [AI_SYMBOL] * 3:
            return 10
        elif winCondition == [OPPONENT_SYMBOL] * 3:
            return -10
    # None means the game hasn't ended yet

        full = True
    for row in board:
        for square in row:
            if square == BLANK_SYMBOL:
                full = False
    if full:
        return 0

    return None

class GameState(object):
    """Represents the state of the board at any given turn.
    self.board is a two-dimensional list containing lists of AI_SYMBOLs or OPPONENT_SYMBOLs.
    self.points is a value dependent on the 'win-state' of the board. X winning
    makes the board worth 10 points, O winning makes the board worth -10 points, and
    all other states (including draws) are worth 0 points.
    self.nextStates is a list of references to other GameState objects, created by calling GameState.iterate().
    self.prevState is a reference to the GameState which created the current instance. In the case of a blank board,
    prevState is equal to None.
    """

    def __init__(self, last_state, board, symbol):
        self.symbol = symbol
        self.board = board
        self.points = None
        self.nextStates = []
        self.prevState = last_state

    def __str__(self):
        """Prints the board in a visually appealing way."""
        rows = []
        rows.append("+-------+")
        for row in self.board:
            temp = row[::]
            temp.insert(0,"|")
            temp.append("|")
            rows.append(" ".join(temp))
        rows.append("+-------+")
        return "\n".join(rows)

    def iterate(self):
        """Generates all possible legal board states one move ahead from the current position,
        and stores each state in self.nextStates."""
        if self.symbol == AI_SYMBOL:
            nSymbol = OPPONENT_SYMBOL
        else:
            nSymbol = AI_SYMBOL
        r = 0
        c = 0
        for row in self.board:
            for square in row:
                if square == BLANK_SYMBOL:
                    temp = copy.deepcopy(self.board)
                    temp[r][c] = self.symbol
                    self.nextStates.append(GameState(self,temp,nSymbol))
                c+= 1
            r+= 1
            c = 0

class BeginningState(GameState):
    """Represents the initial state of the board. self.board is all BLANK_SYMBOL, points is 0, and prevState is None. """
    def __init__(self):
        self.board = [[BLANK_SYMBOL,BLANK_SYMBOL,BLANK_SYMBOL],[BLANK_SYMBOL,BLANK_SYMBOL,BLANK_SYMBOL],[BLANK_SYMBOL,BLANK_SYMBOL,BLANK_SYMBOL]]
        self.points = 0
        self.prevState = None
        self.nextStates = []

class SelfIteratingState(GameState):
    """Like GameState, but this version calls self.iterate() upon creation, so it'll create
    all valid game positions from its current state automatically. May take some time."""

    def __init__(self, last_state, board, symbol):
        self.board = board
        self.nextStates = []
        self.prevState = last_state
        self.symbol = symbol
        self.points = None
        self.iterate()

    def minimax(self):
        score = check_win(self.board)
        if score is not None:
            self.points = score
            # print self
            # print "mini-max endstate: " + str(self.points)
        else:
            scores = []
            for nextState in self.nextStates:
                nextState.minimax()
                scores.append(nextState.points)
            scores.sort()
            # print "scores at state: " + str(scores)
            # print self
            self.points = scores[-1]
            """
            if self.symbol == AI_SYMBOL:
                self.points = scores[0]
            elif self.symbol == OPPONENT_SYMBOL:
                self.points = scores[-1]
            """

    def iterate(self):
        if self.symbol == AI_SYMBOL:
            nSymbol = OPPONENT_SYMBOL
        else:
            nSymbol = AI_SYMBOL
        r = 0
        c = 0
        for row in self.board:
            for square in row:
                if square == BLANK_SYMBOL:
                    temp = copy.deepcopy(self.board)
                    temp[r][c] = self.symbol
                    self.nextStates.append(SelfIteratingState(self,temp,nSymbol))
                c+= 1
            r+= 1
            c = 0

class AIPlayer(object):
    """Represents an AI player that decides the optimal move for any given
    position in a game of tic-tac-toe."""

    def __init__(self):
        self.symbol = AI_SYMBOL

    def random_move(self, game_board):
        """Makes a random valid move on the board."""
        # print "Making random move!"
        game_board.iterate(self.symbol)
        return random.choice(game_board.nextStates)

    def starter_move(self, game_board):
        """Tries to take the corners. In the case of all corners taken, makes a random move."""
        b = copy.deepcopy(game_board.board)
        optimals = [(0,0),
                    (0,2),
                    (2,0),
                    (2,2)]
        for optimalMove in optimals:
            if b[optimalMove[0]][optimalMove[1]] == BLANK_SYMBOL:
                b[optimalMove[0]][optimalMove[1]] = self.symbol
                game_board.board = copy.deepcopy(b)
                return game_board
        return self.random_move(game_board)

    def move(self, game_board):
        """Accepts a GameState, then returns one with the optimal move made.""" # ...ideally
        moveTree = self.predict(game_board)
        bestMove = moveTree.nextStates[0]
        bestScore = -100
        for state in moveTree.nextStates:
            state.minimax()
            # print "Points: " + str(state.points)
            # print state
            if state.points >= bestScore:
                # print "Points: " + str(state.points)
                # print state
                bestScore = state.points
                bestMove = state
        # print "Top score: " + str(bestScore)
        return bestMove

    def predict(self, game_board):
        """Accepts a GameState, then returns a SelfIteratingState with all
        possible states placed in the GameState tree. Assumes that in the board given,
        it is its own turn."""
        return SelfIteratingState(None,game_board.board,self.symbol)


def test():
    b = BeginningState()
    b.board[0][0] = "O"
    b.board[2][2] = "X"
    b.board[2][0] = "O"
    player = AIPlayer()
    opponent = AIPlayer()
    opponent.symbol = OPPONENT_SYMBOL
    b = player.predict(b)
    print(b)

    b = player.move(b)
    print(b)

    b = opponent.move(b)
    print(b)

    b = player.move(b)
    print(b)

def parse():
    msg = input("Your move: ")
    e = True
    while e:
        try:
            if msg == "game":
                return msg
            coords = msg.split(" ")
            coords[0] = int(coords[0])
            coords[1] = int(coords[1])
            assert coords[0] in range(0,3)
            assert coords[1] in range(0,3)
            return [coords[0],coords[1]]
        except Exception:
            print("Invalid move!")
            msg = input("Your move: ")
            continue

def play():
    game = BeginningState()
    ai = AIPlayer()
    print("You move first. It's not like you're going to win.")
    print(game)
    invalid = True
    coords = parse()
    game.board[coords[0]][coords[1]] = OPPONENT_SYMBOL
    print(game)
    print("Now, my move.")
    game = ai.starter_move(game)
    print(game)
    print("Your turn.")

    while True:
        invalidInput = True
        coords = parse()
        while invalidInput:
            if coords == "game":
                print("Current state: ")
                print(game)
                coords = parse()
            elif game.board[coords[0]][coords[1]] == BLANK_SYMBOL:
                game.board[coords[0]][coords[1]] = OPPONENT_SYMBOL
                invalid = False
                break
            else:
                print("Not there, you imbecile!")
                coords = parse()

        if check_win(game.board) == -10:
            print("What?! How?!")
            print(game)
            break
        elif check_win(game.board) == 0:
            print("It's a draw, then.")
            print(game)
            break

        print(game)
        print("Now, my move...")
        game = ai.move(game)
        print(game)

        if check_win(game.board) == 10:
            print("Hah! See, I knew I'd win!")
            break

        print("Your turn.")
    print("GAME OVER")

# play()
# test()

