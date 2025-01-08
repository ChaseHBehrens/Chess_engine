'''
import lichess.api
from lichess.format import PYCHESS

game = lichess.api.game('Qa7FJNk2', format=PYCHESS)
print(game.end().board())
'''

import chess
import chess.pgn

def analyze_game(game):
    board = game.board()
    for move in game.mainline_moves():
        board.push(move)
        #print(board)

pgn_file = r"C:\Users\chase\Downloads\chess_com_games_2023-12-11.pgn"

with open(pgn_file) as file:
    while True:
        game = chess.pgn.read_game(file)
        if game is None:
            break  # No more games in the file

        print("Event:", game.headers["Event"])
        print("Result:", game.headers["Result"])
        analyze_game(game)
            

