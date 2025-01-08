import chess.engine, chessdotcom, requests, chess.pgn
from io import StringIO

import tensorflow as tf
try:
    model = tf.keras.models.load_model(r'C:\Users\chase\OneDrive\Desktop\chess engine\Network Files 6')
except:
    print('could not load data')
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(768, input_shape=(768,), activation='relu'))
    model.add(tf.keras.layers.Dense(5000, activation='relu'))
    model.add(tf.keras.layers.Dense(5000, activation='relu'))
    model.add(tf.keras.layers.Dense(5000, activation='relu'))
    model.add(tf.keras.layers.Dense(5000, activation='relu'))
    model.add(tf.keras.layers.Dense(5000, activation='relu'))
    model.add(tf.keras.layers.Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

stockfish = chess.engine.SimpleEngine.popen_uci(r'C:\Users\chase\OneDrive\Desktop\chess engine\stockfish\stockfish-windows-x86-64-avx2.exe')

running = True
board = chess.Board()
score = stockfish.analyse(board, chess.engine.Limit(time=2.0))['score']
USERNAME = 'sheca42513'
count = 0
n1 = 40
n2 = 0

def get_game_pgn():
    global n1
    global n2
    data = chessdotcom.get_player_game_archives(USERNAME)
    url = data.json['archives'][n1]  # pylint: disable=E1101
    export_response = requests.get(url, timeout=10)
    export_response.raise_for_status()
    if export_response.json()['games'][n2]['rules'] == 'chess':
        pgn = export_response.json()['games'][n2]['pgn']
        if n2 == len(export_response.json()['games'])-1:
            if n1 == len(data.json['archives'])-1:
                return False
            else:
                n1 += 1
                n2 = 0
        else:
            n2 += 1
        return(pgn)
    else:
        if n2 == len(export_response.json()['games'])-1:
            if n1 == len(data.json['archives'])-1:
                return False
            else:
                n1 += 1
                n2 = 0
        else:
            n2 += 1
        return None

key = {0:'P',1:'N',2:'B',3:'R',4:'Q',5:'K',6:'p',7:'n',8:'b',9:'r',10:'q',11:'k'}
def generate_input(color):
    global board
    if color:
        inputs = [1 if str(board.piece_at(chess.square(i%64,0))) == key[i//64] else 0 for i in range(768)]     
    else:
        inputs = [1 if str(board.piece_at(chess.square(i%64,0))) == key[i//64] else 0 for i in range(767,-1,-1)]
    return inputs

def extract_score():
    global board, score
    if score.is_mate():
        if str(score)[14] == '+':
            score_value = 100
        else:
            score_value = -100
    else:
        score_value = int(score.relative.score())
    return score_value



while running:
    board = chess.Board()
    pgn = get_game_pgn()
    if pgn:
        if pgn.splitlines()[0][8:-2] == 'Live Chess' and pgn.splitlines()[7][1:6] != 'SetUp':
            game = chess.pgn.read_game(StringIO(pgn))
            x_train = []
            y_train = []

            for i, move in enumerate(game.mainline_moves()):
                evaluation = -1 * extract_score()
                board.push(move)
                x_train.append(generate_input(i%2==0))
                y_train.append([((evaluation-extract_score())/200)+0.5])
            if x_train and y_train:
                model.fit(x_train, y_train, epochs=1)
                tf.keras.models.save_model(model, r'C:\Users\chase\OneDrive\Desktop\chess engine\Network Files 6')
            count += 1
        print(str(n1)+','+str(n2))
        print(count)
    elif pgn == None:
        pass
    else:
        running = False

stockfish.quit()

