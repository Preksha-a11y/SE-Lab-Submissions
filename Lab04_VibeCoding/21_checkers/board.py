SIZE = 8


def initial_board():
    board = [["."] * SIZE for _ in range(SIZE)]
    for r in range(3):
        for c in range(SIZE):
            if (r + c) % 2 == 1:
                board[r][c] = "B"
    for r in range(5, 8):
        for c in range(SIZE):
            if (r + c) % 2 == 1:
                board[r][c] = "R"
    return board


def move_piece(board, start, end):
    sr, sc = start
    er, ec = end
    captured = None
    if abs(er - sr) == 2 and abs(ec - sc) == 2:
        mr, mc = (sr + er) // 2, (sc + ec) // 2
        captured = board[mr][mc]
        board[mr][mc] = "."
    board[er][ec] = board[sr][sc]
    board[sr][sc] = "."
    return captured

