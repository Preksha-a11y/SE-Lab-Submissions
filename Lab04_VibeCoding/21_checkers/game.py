from board import initial_board, move_piece, SIZE
from rules import (
    simple_move,
    capture_move,
    promote,
    get_all_legal_moves,
    get_all_captures,
    get_captures_for_square,
    is_player_piece,
)


class Checkers:
    def __init__(self):
        self.board = initial_board()
        self.player = "R"
        self.multi_capture_square = None
        self.turn_number = 1
        self.move_history = []

    def count_pieces(self):
        red_count = sum(row.count("R") + row.count("RK") for row in self.board)
        black_count = sum(row.count("B") + row.count("BK") for row in self.board)
        return red_count, black_count

    def print_board(self):
        red_count, black_count = self.count_pieces()
        print(f"\n--- Turn {self.turn_number} [{'Red' if self.player == 'R' else 'Black'}] ---")
        print("   " + " ".join(str(c) for c in range(SIZE)))
        for r, row in enumerate(self.board):
            print(f"{r}  " + " ".join(row))
        print(f"Pieces Remaining - Red: {red_count} | Black: {black_count}")

    def run(self):
        print("Checkers - commands: 'sr sc er ec' to move, 'hint' for legal moves, 'q' to quit, 'help' for instructions.")
        while True:
            # Check for Win / No legal moves condition
            if self.multi_capture_square is None:
                legal_moves = get_all_legal_moves(self.board, self.player)
                if not legal_moves:
                    self.print_board()
                    winner = "Black" if self.player == "R" else "Red"
                    player_name = "Red" if self.player == "R" else "Black"
                    print(f"\n*** Game Over! {player_name} has no legal moves left. {winner} WINS! ***")
                    return

            self.print_board()
            player_name = "Red" if self.player == "R" else "Black"

            if self.multi_capture_square:
                print(f"[{player_name}] Multi-capture required from piece at {self.multi_capture_square}!")

            raw_input_str = input(f"{self.player}> ").strip().lower()
            raw = raw_input_str.split()

            if not raw:
                continue

            if raw == ["q"]:
                print("Game ended by user.")
                return

            if raw == ["help"]:
                print("\n=== Checkers Game Controls ===")
                print("- Enter coordinates: 'sr sc er ec' (e.g., 5 2 4 3)")
                print("- 'hint': Show all legal moves for current player")
                print("- 'q': Quit game")
                print("- Regular pieces move forward diagonally. Kings (RK/BK) move both forward and backward.")
                print("- Captures are forced! Jumped pieces are removed.\n")
                continue

            if raw == ["hint"]:
                if self.multi_capture_square:
                    legal = [((self.multi_capture_square), dest) for dest in get_captures_for_square(self.board, self.player, *self.multi_capture_square)]
                else:
                    legal = get_all_legal_moves(self.board, self.player)

                print(f"\n[Hint] Legal moves for {player_name}:")
                for start_pos, end_pos in legal:
                    print(f"   {start_pos} -> {end_pos}")
                continue

            if len(raw) != 4:
                print("Invalid input. Enter four numbers ('sr sc er ec'), 'hint', or 'q'.")
                continue

            try:
                sr, sc, er, ec = map(int, raw)
            except ValueError:
                print("Coordinates must be numbers.")
                continue

            if not all(0 <= x < SIZE for x in (sr, sc, er, ec)):
                print("Outside board.")
                continue

            start, end = (sr, sc), (er, ec)

            # Multi-capture restriction
            if self.multi_capture_square and start != self.multi_capture_square:
                print(f"Must continue multi-capture with piece at {self.multi_capture_square}.")
                continue

            if not is_player_piece(self.board[sr][sc], self.player):
                print("That is not your piece.")
                continue

            all_captures = get_all_captures(self.board, self.player)
            if self.multi_capture_square:
                if not capture_move(self.board, self.player, start, end):
                    print("Invalid capture move.")
                    continue
            else:
                if all_captures:
                    if not capture_move(self.board, self.player, start, end):
                        print("Invalid move: Capture is forced!")
                        continue
                else:
                    if not simple_move(self.board, self.player, start, end):
                        print("Invalid move.")
                        continue

            # Execute move
            is_capture = abs(er - sr) == 2
            mr, mc = ((sr + er) // 2, (sc + ec) // 2) if is_capture else (None, None)
            move_piece(self.board, start, end)

            # Handle promotion
            was_promoted = promote(self.board, pos=end)

            # Feedback message
            if is_capture:
                msg = f"[Action] {player_name} captured opponent at ({mr}, {mc}) moving ({sr}, {sc}) -> ({er}, {ec})."
            else:
                msg = f"[Action] {player_name} moved from ({sr}, {sc}) to ({er}, {ec})."

            print(msg)
            self.move_history.append(msg)

            if was_promoted:
                p_msg = f"[Notice] {player_name} piece at ({er}, {ec}) promoted to King!"
                print(p_msg)
                self.move_history.append(p_msg)

            # Check for multi-capture continuation
            if is_capture and not was_promoted:
                further_captures = get_captures_for_square(self.board, self.player, er, ec)
                if further_captures:
                    self.multi_capture_square = (er, ec)
                    continue

            # End of turn
            self.multi_capture_square = None
            self.turn_number += 1
            self.player = "B" if self.player == "R" else "R"
