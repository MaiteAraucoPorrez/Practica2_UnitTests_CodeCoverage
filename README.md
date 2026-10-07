# ChessPython

ChessPython is a terminal-based chess game written in Python. It runs in a loop, draws the board after each move, and alternates turns between White and Black until a king is captured.

## Motivation

This project is a lightweight way to play chess in the terminal while learning Python object-oriented design.

It focuses on:

- Clear piece-based movement logic
- A simple interactive game loop
- Readable code that is easy to extend with full chess rules later

## Quick Start

Run these commands from the project root:

```bash
# 1) Install uv (Linux/macOS)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2) Verify uv is installed
uv --version

# 3) Start the game
uv run main.py
```

## Requirements

- Python 3.14+
- uv
- A terminal that can display Unicode chess symbols

## Install uv

Install uv with one of the official methods below:

### Linux and macOS

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Verify Installation

```bash
uv --version
```

## Run The Game

From the project root:

```bash
uv run main.py
```

If this is your first run, uv will create and manage the environment automatically.

You should see:

- A welcome message
- `New Game Started`
- The current board
- A prompt for White, then Black

## Usage

Use algebraic square coordinates in a 4-character move format:

- First 2 characters: start square
- Last 2 characters: destination square

Examples:

```text
e2e4
g1f3
```

During the game:

- White enters a move
- Black enters a move
- The board redraws after every legal move
- Invalid moves prompt the same player again

When a game ends, enter:

- `y` to restart
- `n` to quit

## How Input Works

Enter moves in this exact format:

```text
<start_file><start_rank><end_file><end_rank>
```

Example:

```text
d2d4
```

Rules for valid input:

- Exactly 4 characters
- Files must be `a` through `h`
- Ranks must be `1` through `8`
- Input is case-insensitive (the game converts it to lowercase)

If input is invalid, the game prints an error and asks again.

## Turn Flow

Each turn does the following checks in order:

1. Validate move string format
2. Validate that the chosen start square contains the current player's piece
3. Validate that the move is legal for that piece
4. Apply the move and redraw the board

If any check fails, the same player is prompted again.

## Board Display

- The board is printed as 8 rows plus a file label row.
- Rows are printed from rank `1` to rank `8` (top to bottom in terminal output).
- Files are shown as `abcdefgh`.
- Empty squares are drawn as alternating `■` and `□`.
- Pieces are drawn with Unicode chess glyphs.

## Piece Movement Implemented

- King: one square in any direction
- Queen: straight or diagonal
- Rook: straight lines
- Bishop: diagonals
- Knight: standard L-shape
- Pawn:
	- forward 1
	- forward 2 on first move
	- diagonal capture when an enemy piece is present

## Win Condition

The game ends when a king piece is captured.

After game over, you can choose to restart:

- `y` to start a new game
- `n` to quit

## Current Limitations

This project currently models a simplified chess flow. The following standard rules are not implemented yet:

- Check and checkmate logic
- Stalemate and draw conditions
- Castling
- En passant capture
- Pawn promotion

Notes about current behavior:

- Most non-knight pieces treat any occupied destination square as blocked, so captures are very limited.
- Game over depends on direct king capture, not checkmate detection.

## Project Structure

- `main.py`: program entry point
- `game.py`: game loop, turn handling, restart flow
- `board.py`: board setup, drawing, turn validation, piece movement
- `pieces/`: movement rules and rendering per piece type

## Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes and keep code style consistent with the project.
4. Run the game locally with `uv run main.py` to verify behavior.
5. Open a pull request with a clear summary of what changed and why.
