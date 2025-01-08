import requests
import chess.pgn
from chessdotcom import get_player_game_archives

print(1)

def get_game_pgn(username):
    data = get_player_game_archives(username).json
    url = data['archives'][-1]
    games = requests.get(url).json()
    game_url = games['games'][-1]['url']
    pgn = requests.get(game_url).content.decode('utf-8')
    parsed_game = chess.pgn.read_game(io.StringIO(pgn))
    return parsed_game

# Example usage
game = get_game_pgn('bhb2572')
print(game)  # This will print the PGN of the latest game played by the user
