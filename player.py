import random
import math

class Player:
    def __init__(self, letter):
        self.letter = letter

    def get_name(self):
        return self.letter

    def get_move(self, game):
        pass
    
class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
        
    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square
    
class ComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def minimax(self, state, letter):
        max_player = self.letter
        other_player = 'O' if letter == 'X' else 'X'
        # check if the previous move is the winnner
        if state.current_winner == other_player:
            return {'position': None,
                    'score': 1*(state.num_empty_squares() + 1) 
                    if other_player == max_player else -1 * (
                state.num_empty_squares() + 1
                    )}
        elif not state.num_empty_squares():
            return {'position': None,
                    'score': 0}
        if letter == max_player:
            best = {'position': None,
                    'score': -math.inf}
        else:
            best = {'position': None,
                   'score': math.inf}
        
        for possible_move in state.available_moves():
            state.make_move(possible_move, letter)
            sim_score = self.minimax(state, other_player)
            state.board[possible_move] = ' '
            state.current_winner = None
            
            sim_score['position'] = possible_move

            if letter == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best


    def get_move(self, game):
        if len(game.available_moves()) == 9:
             square = random.choice(game.available_moves())
        else:
            square = self.minimax(game, self.letter)['position']
        return square

    
    
class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
        
    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (1-9): ')
            try:
                val = int(square) - 1
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print("Invalid square. Try again.")
        return val