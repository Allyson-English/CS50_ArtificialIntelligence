import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = cells
        self.count = count
        

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        
        if len(self.cells) == self.count:
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        
        if cell in self.cells:
            self.cells.remove(cell)
        
            


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        
        # mark cell as a move that has been made
        self.moves_made.add(cell)
        
        # mark the cell as safe
        self.safes.add(cell)
        
        # update knowledge base with cell just uncovered and the count of that cell
        new_statement = Sentence(cell, count)
        self.knowledge.append(new_statement)
        
        # if the count is zero, all neighbors are safe
        if count == 0:
            nbrs = self.neighbors(cell)
            
            for each_nbr in nbrs:
                self.safes.add(each_nbr)
        
        # if the count is not zero
        if count != 0:
            nbrs = self.neighbors(cell)
            
            # check all neighbors to see if they are safe or not
            potential_mines = [x for x in nbrs if not x in self.safes]
            
            # if the number of unsafe neighbors equals the number of mines the cell is touching, all those cells are assuradelly mines
            if len(potential_mines) == count:
                for each_mine in potential_mines:
                    self.mark_mine(each_mine)
            
            # check all neighbors to see which have already been identified as mines
            nearby_mines = [x for x in nbrs if x in self.mines]
            
            # if the number of mines identified in neighbors is equal to the count, then all other cells touching the cell in question, are safe
            if len(nearby_mines) == count:
                for safecells in nbrs:
                    if not safecells in nearby_mines:
                        self.safes.add(cell)
        
        # loop through knowledge and apply logic above for non-zero counts
        for statement in self.knowledge:
           
            if statement.count != 0:
                nbrs = self.neighbors(statement.cells)
                
                check_mines_for_neighbor = [x for x in nbrs if x in self.mines]
                
                if len(check_mines_for_neighbor) == statement.count:
                    for each_cell in nbrs:
                        if not each_cell in check_mines_for_neighbor:
                            self.safes.add(each_cell)
                            
                
                check_safes_for_neighbor = [x for x in nbrs if not x in self.safes]
                
                if len(check_safes_for_neighbor) == statement.count:
                    for each_cell in check_safes_for_neighbor:
                        self.mines.add(each_cell)
                        
                
                
        
#         print(cell)
#         print("Mines: ", self.mines)
#         print("Safes: ", self.safes, "\n")
#         print("\n")
        return None
        raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        
        possible_moves = [x for x in list(self.safes) if not x in self.moves_made]
        
        if not possible_moves:
            return None
        
        return possible_moves[0]

        
        #raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        x, y = random.choice(range(8)), random.choice(range(8))
        
        print(x, y)
        return (x, y)

    
    def neighbors(self, cell):
        
        if not isinstance(cell, tuple):
            print(cell)
            print("Not a tuple")

        x, y = cell
        nbrs = [(x+i, y+j) for i in (-1,0,1) for j in (-1,0,1)]
        nbrs = [x for x in nbrs if x[0] >= 0 and x[-1] >= 0 and x[0] < self.height and x[-1] < self.width]

        return set(nbrs)
