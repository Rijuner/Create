# Import Modules & Libraries
import chess, random, time
import display_gui as gui
import global_vars as G

# Select Random Move
def select_random():
    # Step 1: Get All Possible Moves
    move_list = list(G.BOARD.legal_moves)
    # Step 2: Randint, SelectMove with number
    random_num = random.randint(0, len(move_list)-1)
    #Step 3: Return Move
    return move_list[random_num]

def random_improved():
    move_list = list(G.BOARD.legal_moves)
    optimal_move = None
    max_piece_value = 0
    piece_value_list = [1, 3, 3.2, 5, 9, 0]
    move_rank = 0
    for move in move_list:
        G.BOARD.push(move)
        if G.BOARD.is_checkmate():
            G.BOARD.pop()
            return move
        if move_rank < 2 and G.BOARD.is_check():
            optimal_move = move
            move_rank = 2
        G.BOARD.pop()
        if move_rank <= 3 and G.BOARD.is_capture(move):
            target_square = move.to_square
            piece_value = piece_value_list[G.BOARD.piece_at(target_square).piece_type-1]
            if piece_value > max_piece_value:
                optimal_move = move
                max_piece_value = piece_value
            move_rank = 3
        if move_rank < 1 and G.BOARD.is_castling(move):
            optimal_move = move
            move_rank = 1
    if optimal_move:
        return optimal_move
    else:
        return select_random()


# Get Game Status
def calc_game_status():
    if G.BOARD.is_checkmate():
        if G.BOARD.turn:
            return -9999
        else:
            return 9999
    elif G.BOARD.is_stalemate():
        return 0
    elif G.BOARD.is_insufficient_material():
        return 0
    elif G.BOARD.is_seventyfive_moves():
        return 0
    elif G.BOARD.is_fivefold_repetition():
        return 0
    else:
        return "CONTINUE"
# Get Board Score
def calc_board_score():
    game_status = calc_game_status()
    if game_status != "CONTINUE":
        return game_status

    w_pawns = G.BOARD.pieces(chess.PAWN, chess.WHITE)
    b_pawns = G.BOARD.pieces(chess.PAWN, chess.BLACK)
    w_knights = G.BOARD.pieces(chess.KNIGHT, chess.WHITE)
    b_knights = G.BOARD.pieces(chess.KNIGHT, chess.BLACK)
    w_bishops = G.BOARD.pieces(chess.BISHOP, chess.WHITE)
    b_bishops = G.BOARD.pieces(chess.BISHOP, chess.BLACK)
    w_rooks = G.BOARD.pieces(chess.ROOK, chess.WHITE)
    b_rooks = G.BOARD.pieces(chess.ROOK, chess.BLACK)
    w_queens = G.BOARD.pieces(chess.QUEEN, chess.WHITE)
    b_queens = G.BOARD.pieces(chess.QUEEN, chess.BLACK)
    w_kings = G.BOARD.pieces(chess.KING, chess.WHITE)
    b_kings = G.BOARD.pieces(chess.KING, chess.BLACK)

    w_score_p = sum([G.pawn_score[i] for i in w_pawns])
    b_score_p = sum([-G.pawn_score[chess.square_mirror(i)] for i in b_pawns])
    w_score_n = sum([G.knight_score[i] for i in w_knights])
    b_score_n = sum([-G.knight_score[chess.square_mirror(i)] for i in b_knights])
    w_score_b = sum([G.bishop_score[i] for i in w_bishops])
    b_score_b = sum([-G.bishop_score[chess.square_mirror(i)] for i in b_bishops])
    w_score_r = sum([G.rook_score[i] for i in w_rooks])
    b_score_r = sum([-G.rook_score[chess.square_mirror(i)] for i in b_rooks])
    w_score_q = sum([G.queen_score[i] for i in w_queens])
    b_score_q = sum([-G.queen_score[chess.square_mirror(i)] for i in b_queens])
    w_score_k = sum([G.king_score[i] for i in w_kings])
    b_score_k = sum([-G.king_score[chess.square_mirror(i)] for i in b_kings])

    pawns= len(w_pawns) - len(b_pawns)
    knights = len(w_knights) - len(b_knights)
    bishops = len(w_bishops) - len(b_bishops)
    rooks = len(w_rooks) - len(b_rooks)
    queens = len(w_queens) - len(b_queens)

    material = (100 * pawns) + (320 * knights) + (330 * bishops) + (500 * rooks) + (900 * queens)
    final = material + w_score_p + b_score_p + w_score_n + b_score_n + w_score_b + b_score_b + w_score_r + b_score_r + w_score_q + b_score_q + w_score_k + b_score_k

    if G.BOARD.turn:
        return final
    else:
        return -final

# Select Positional Move
def select_positional():
    best_move = chess.Move.null()
    best_score = -99999

    for move in G.BOARD.legal_moves:
        G.BOARD.push(move)
        score = -calc_board_score()
        G.BOARD.pop()

        if score > best_score:
            best_score = score
            best_move = move
    return best_move

# Negamax with Alpha-Beta Pruning

def make_ai_move(move, delay):
    time.sleep(delay)
    if move != chess.Move.null():
        gui.draw_board()
        gui.draw_select_square(move.from_square)
        gui.draw_select_square(move.to_square)
    gui.print_san(move)
    G.BOARD.push(move)