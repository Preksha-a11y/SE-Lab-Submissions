SIZE = 8


def is_player_piece(piece, player):
    if player == "R":
        return piece in ("R", "RK")
    if player == "B":
        return piece in ("B", "BK")
    return False


def is_opponent_piece(piece, player):
    if player == "R":
        return piece in ("B", "BK")
    if player == "B":
        return piece in ("R", "RK")
    return False


def simple_move(board, player, start, end):
    sr, sc = start
    er, ec = end
    if not (0 <= sr < SIZE and 0 <= sc < SIZE and 0 <= er < SIZE and 0 <= ec < SIZE):
        return False
    piece = board[sr][sc]
    if not is_player_piece(piece, player) or board[er][ec] != ".":
        return False
    if abs(er - sr) != 1 or abs(ec - sc) != 1:
        return False
    if piece == "R" and (er - sr != -1):
        return False
    if piece == "B" and (er - sr != 1):
        return False
    return True


def capture_move(board, player, start, end):
    sr, sc = start
    er, ec = end
    if not (0 <= sr < SIZE and 0 <= sc < SIZE and 0 <= er < SIZE and 0 <= ec < SIZE):
        return False
    piece = board[sr][sc]
    if not is_player_piece(piece, player) or board[er][ec] != ".":
        return False
    if abs(er - sr) != 2 or abs(ec - sc) != 2:
        return False
    if piece == "R" and (er - sr != -2):
        return False
    if piece == "B" and (er - sr != 2):
        return False
    mr, mc = (sr + er) // 2, (sc + ec) // 2
    if not is_opponent_piece(board[mr][mc], player):
        return False
    return True


def promote(board, pos=None):
    """Promotes pieces at the back row.
    If pos is given, returns True if piece at pos was newly promoted."""
    promoted = False
    if pos is not None:
        r, c = pos
        if board[r][c] == "R" and r == 0:
            board[r][c] = "RK"
            return True
        if board[r][c] == "B" and r == SIZE - 1:
            board[r][c] = "BK"
            return True
        return False

    for c in range(SIZE):
        if board[0][c] == "R":
            board[0][c] = "RK"
            promoted = True
        if board[SIZE - 1][c] == "B":
            board[SIZE - 1][c] = "BK"
            promoted = True
    return promoted


def get_captures_for_square(board, player, r, c):
    """Returns list of valid capture end coordinates from (r, c)."""
    captures = []
    if not is_player_piece(board[r][c], player):
        return captures
    for dr in (-2, 2):
        for dc in (-2, 2):
            er, ec = r + dr, c + dc
            if capture_move(board, player, (r, c), (er, ec)):
                captures.append((er, ec))
    return captures


def get_all_captures(board, player):
    """Returns list of all ((sr, sc), (er, ec)) legal capture moves for player."""
    moves = []
    for r in range(SIZE):
        for c in range(SIZE):
            if is_player_piece(board[r][c], player):
                for dest in get_captures_for_square(board, player, r, c):
                    moves.append(((r, c), dest))
    return moves


def get_all_simple_moves(board, player):
    """Returns list of all ((sr, sc), (er, ec)) legal simple moves for player."""
    moves = []
    for r in range(SIZE):
        for c in range(SIZE):
            if is_player_piece(board[r][c], player):
                for dr in (-1, 1):
                    for dc in (-1, 1):
                        er, ec = r + dr, c + dc
                        if simple_move(board, player, (r, c), (er, ec)):
                            moves.append(((r, c), (er, ec)))
    return moves


def get_all_legal_moves(board, player):
    """Returns forced captures if available, otherwise simple moves."""
    captures = get_all_captures(board, player)
    if captures:
        return captures
    return get_all_simple_moves(board, player)
