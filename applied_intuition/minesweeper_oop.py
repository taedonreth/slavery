# design minesweeper

"""
Prompt:

Design the backend for a simplified Minesweeper game. Use a 2D matrix to represent the map, where 
certain cells contain mines and others are safe. Define and implement a class with at least two main APIs: 
initiate() to randomly generate a Minesweeper board and place mines (you can decide how to handle input such 
as board size and number of mines), and click(x, y) to reveal a cell. If the cell is a mine, the game ends. 
If it is not a mine, reveal the cell and, if the cell has no adjacent mines, recursively (or using BFS/DFS) 
reveal all connected empty cells, ensuring that revealed cells display the correct count of adjacent mines. 
You should explain your design choices (e.g., data structures used to represent the board, how you track 
revealed/hidden cells, and how you avoid re-processing cells). After coding, discuss how you might extend this 
to a real online game system: what logic should live on the backend vs. frontend, what tradeoffs exist 
(e.g., performance vs. security), and how your design could scale if millions of players were playing simultaneously.

Thoughts:
    - create minesweeper board
        - input: num rows m and num cols n
        - generate a minesweeper boardwith m rows and n columns
            - random num of mines
            - 
    - handle click input
        - reveal click
        - if mine, game ends
        - if not mine, reveal cell
            - if no adjacent mines, recursively reveal all connected empty cells
            - if adjacent mines, reveal num of adjacent mines
"""

import random

DIRECTIONS = [(-1, 0), (-1, -1), (-1, 1), (0, 1), (0, -1), (1, 1), (1, -1), (1, 0)]
class MinesweeperGame:
    """
    Manages the backend logic for a Minesweeper game, using a secure two-board system.
    """

    def __init__(self):
        self.rows = 0
        self.cols = 0
        self.board = []      # actual state of the board (user doesn't see all this)
        self.revealed = []   # A boolean mask of what the player can see
        self.game_over = False

    def initiate(self, rows: int, cols: int, num_mines: int):
        """Initializes the game board, places mines, and calculates numbers."""
        self.rows = rows
        self.cols = cols
        self.game_over = False
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
        self._place_mines(num_mines)
        self._calculate_numbers()

    def _place_mines(self, num_mines: int):
        """Helper to place mines randomly on the board."""
        mine_positions = set()
        while len(mine_positions) < num_mines:
            r, c = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            mine_positions.add((r, c))
        for r, c in mine_positions:
            self.board[r][c] = -1

    def _calculate_numbers(self):
        """Helper to pre-calculate adjacent mine counts for all non-mine cells."""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    continue
                mine_count = 0
                for i, j in DIRECTIONS:
                    nr, nc = r + i, c + j
                    if 0 <= nr < self.rows and 0 <= nc < self.cols and self.board[nr][nc] == -1:
                        mine_count += 1
                self.board[r][c] = mine_count

    def click(self, r: int, c: int) -> bool:
        """
        Handles a player's click using an iterative DFS to reveal cells.
        This is the adaptation of your provided code.
        """
        r -= 1
        c -= 1
        if not (0 <= r < self.rows and 0 <= c < self.cols) or self.revealed[r][c] or self.game_over:
            print("choose another!")
            return True

        # First, check if the clicked cell is a mine
        if self.board[r][c] == -1:
            self.game_over = True
            self.revealed[r][c] = True
            return False

        # Use a stack for iterative DFS, as in your logic
        stack = [(r, c)]

        while stack:
            curr_r, curr_c = stack.pop()

            # Process a cell only if it hasn't been revealed yet
            if not self.revealed[curr_r][curr_c]:
                self.revealed[curr_r][curr_c] = True

                # If the cell is empty (0), add all unrevealed neighbors to the stack to continue the cascade
                if self.board[curr_r][curr_c] == 0:
                    for dr, dc in DIRECTIONS:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols and not self.revealed[nr][nc]:
                            stack.append((nr, nc))
        return True

    def print_board(self) -> None:
        """Prints the board as the player would see it."""
        for r in range(self.rows):
            row_str = []
            for c in range(self.cols):
                if not self.revealed[r][c]:
                    row_str.append('#')  # Hidden
                elif self.board[r][c] == -1:
                    row_str.append('*')  # Mine
                elif self.board[r][c] > 0:
                    row_str.append(str(self.board[r][c]))
                else:  # board[r][c] == 0
                    row_str.append('.')  # Empty revealed cell
            print(" ".join(row_str))

# --- Example Usage ---
if __name__ == "__main__":
    game = MinesweeperGame()
    game.initiate(rows=10, cols=10, num_mines=15)

    print("Minesweeper Game Started!")
    print("Enter row and column to click (e.g., '5 5'), or 'q' to quit\n")
    
    while not game.game_over:
        game.print_board()
        
        user_input = input("\nEnter row col (or 'q' to quit): ").strip()
        
        if user_input.lower() == 'q':
            print("Thanks for playing!")
            break
            
        try:
            r, c = map(int, user_input.split())
            if not game.click(r, c):
                print("\n💥 BOOM! You hit a mine!")
                game.print_board()
                print("\nGame Over!")
                break
        except (ValueError, IndexError):
            print("Invalid input. Please enter two numbers separated by space.")


"""
============================================================
MINESWEEPER: COMPLETE DESIGN & FOLLOW-UP Q&A
============================================================

I. Design Choices Explained
--------------------------

    1. Board Data Structure:
        - A two-board system is used to securely separate the game's complete
          solution from the player's view.
        - `self.board` (The Ground Truth): This integer matrix stores the solution.
          Using -1 for mines and 0-8 for numbers is efficient. Numbers are
          pre-calculated at the start, making the critical `click` operation
          a fast O(1) lookup during gameplay.
        - `self.revealed` (The Visibility Mask): This boolean matrix tracks what the
          player is allowed to see. This provides a clean separation of concerns.

    2. Tracking Revealed/Hidden Cells:
        - The `self.revealed` boolean mask is the sole mechanism for tracking
          visibility. A value of `True` at `[r][c]` means the cell is visible.

    3. Avoiding Re-processing Cells:
        - An initial guard clause in the `click` method (`if self.revealed[r][c]: ...`)
          immediately stops any action on an already revealed cell.
        - During the cascading reveal, the `self.revealed` grid also functions as a
          "visited" set, preventing redundant processing and infinite loops.


II. Extending to a Real Online Game System
-------------------------------------------

    1. Frontend vs. Backend Logic:
        - Backend (Server): Must be the "single source of truth." It handles all
          critical game logic to prevent cheating: board generation, click
          validation, and managing the true game state.
        - Frontend (Client): Handles presentation and user input. It renders the
          board state sent by the backend and transmits user actions (like a click)
          to the server via API calls. It should never know mine locations.

    2. Performance vs. Security Tradeoffs:
        - The only secure model is an authoritative server. Every player action is an
          API call to the backend, which validates the move and returns only the
          necessary updates to the player's view.
        - The tradeoff is a small amount of network latency for each move, which is
          accepted in exchange for complete security against cheating.

    3. Scaling to Millions of Players:
        - The stateful design (holding game objects in server memory) does not scale.
          The solution is to use a stateless API architecture.
        - Backend servers hold no game data in memory. The state of every active
          game is stored in a fast, centralized, and distributed data store like Redis.
        - A player request containing a `game_id` can be handled by any available
          server. The server fetches the state from Redis, processes the move,
          saves the new state back, and returns the result.


III. Detailed Follow-Up Q&A
---------------------------

    1. Complexity:
       Q: What is the time complexity of your click() operation in the worst case?
       A: The worst-case time complexity is O(Rows * Cols). This occurs when a
          player clicks on a '0' cell that triggers a cascading reveal across
          the entire board, forcing a traversal of every cell.

       Q: How does board size or mine density affect performance?
       A: - Board Size: Performance is directly proportional to the number of
          cells (Rows * Cols). Larger boards have slower initial load times.
        - Mine Density: A higher mine density generally leads to a faster
          average click performance, as there are fewer large open areas,
          making cascading reveals smaller.

    2. API/Extensibility:
       Q: How would you extend your initiate() function to support difficulty levels?
       A: Modify the signature to accept a single difficulty string (e.g., 'easy').
          A dictionary would map these strings to configuration tuples.
          
          configs = {
              'easy':   {'rows': 9, 'cols': 9, 'mines': 10},
              'medium': {'rows': 16, 'cols': 16, 'mines': 40}
          }

       Q: How would you add a “flag” feature to your API?
       A: 1. Add a new 2D boolean grid: `self.flagged`.
          2. Create a new API method: `flag(r, c)`.
          3. Update the player view to display a flag character.

    3. Scalability:
       Q: Would you store the entire game state server-side, or push part of it to the client?
       A: The entire "ground truth" game state (with mine locations) must remain
          server-side for security reasons to prevent cheating.

       Q: How would you handle concurrent game sessions efficiently?
       A: The stateless API + Redis model handles this naturally. Each game session
          is a unique key-value pair in Redis. Stateless servers can process
          requests for thousands of different games simultaneously without conflict.

    4. Edge Cases:
       Q: What happens if a user clicks the same cell multiple times?
       A: The `click()` function has a guard clause that does nothing if a cell is
          already revealed.

       Q: How would your code behave if the user clicks on the very first move and it happens to be a mine?
       A: A user-friendly improvement is to guarantee the first move is safe. This is
          implemented by generating the board and placing the mines *after* the
          first click is known, ensuring the clicked cell is excluded from
          possible mine locations.

first click improvement:
def __init__(self):
    self.rows = 0
    self.cols = 0
    self.num_mines = 0      # ADDED
    self.board = []
    self.revealed = []
    self.game_over = False
    self.first_move = True  # ADDED

def initiate(self, rows: int, cols: int, num_mines: int):
    self.rows = rows
    self.cols = cols
    self.num_mines = num_mines # ADDED
    self.game_over = False
    self.first_move = True     # ADDED
    # Create empty boards; mines will be placed on the first click
    self.board = [[0 for _ in range(cols)] for _ in range(rows)]
    self.revealed = [[False for _ in range(cols)] for _ in range(rows)]

def _place_mines(self, first_r: int, first_c: int):
    # Create a safe zone around the first click (the cell and its neighbors)
    safe_zone = set([(first_r, first_c)]) # added
    for dr, dc in DIRECTIONS:
        nr, nc = first_r + dr, first_c + dc
        if 0 <= nr < self.rows and 0 <= nc < self.cols:
            safe_zone.add((nr, nc)) # added

    mine_positions = set()
    while len(mine_positions) < self.num_mines:
        r, c = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
        # Ensure the mine is not placed in the safe zone
        if (r, c) not in safe_zone:
            mine_positions.add((r, c))

    for r, c in mine_positions:
        self.board[r][c] = -1

def click(self, r: int, c: int) -> bool:

    # Convert 1-based user input to 0-based internal index
    r -= 1
    c -= 1

------ changed
    if not (0 <= r < self.rows and 0 <= c < self.cols) or self.game_over:
        print("Invalid move. Try again.")
        return True

    # If this is the first move, generate the board now
    if self.first_move:
        self._place_mines(r, c)
        self._calculate_numbers()
        self.first_move = False

    if self.revealed[r][c]:
        print("Cell already revealed. Try again.")
        return True
----- changed
    # Check if the clicked cell is a mine (impossible on first click now)
    if self.board[r][c] == -1:
        self.game_over = True
        self.revealed[r][c] = True
        return False

    # Use a stack for iterative DFS to reveal cells
    stack = [(r, c)]
    while stack:
        curr_r, curr_c = stack.pop()
        if not self.revealed[curr_r][curr_c]:
            self.revealed[curr_r][curr_c] = True
            if self.board[curr_r][curr_c] == 0:
                for dr, dc in DIRECTIONS:
                    nr, nc = curr_r + dr, curr_c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols and not self.revealed[nr][nc]:
                        stack.append((nr, nc))
    return True

"""