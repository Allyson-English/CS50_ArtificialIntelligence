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
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        
        if len(self.cell) == self.count:
            self.mines = self.cells
        
        self.mines = set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        
        if self.count == 0:
            self.safes = self.cells
        
        self.safes = set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        
        if not cell in self.safes:
            self.mines.add(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        
        if not cell in self.mines:
            self.safes.add(cell)
        
            


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
        
        # AE Additions
        
        # List of all cells 
        self.allcells = [[(row, col) for col in range(0,width)] for row in range(0,height)]

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
        
        # update knowledge base
        
        print("Move: ", cell)
        knowledgedict = [x for x in self.knowledge if isinstance(x, dict)]
        if not knowledgedict:
            knowledgedict = {}
            self.knowledge.append(knowledgedict)
            
        if knowledgedict:
            knowledgedict = knowledgedict[0]
            
        if not cell in knowledgedict.keys():
            knowledgedict[cell] = count
            
        nbrs = self.neighbors((cell))
                    
        
        if count == 0:
            for ea in nbrs:
                self.safes.add(ea)

        for k in knowledgedict.keys():

            if knowledgedict[k] > 0:

                nbrs_originalcell = self.neighbors(k)

                check = [x for x in nbrs_originalcell if not x in knowledgedict.keys()]

                if len(check) == 1:

                    x, y = check[0]

                    nbrs_potentialmine = self.neighbors(check[0])

                    for ea in nbrs_potentialmine:
                        if not ea in knowledgedict.keys() or knowledgedict[ea] > 0:
                            continue
                        else:
                            x, y = None, None

                    if x and y:
                        self.mines.add(check[0])
                        
                foundmines = [x for x in nbrs_originalcell if x in self.mines]
                
                if len(foundmines) != knowledgedict[k]:
                    
                    if knowledgedict[k] == len(check):
                        
                        for c in check:
                            self.mines.add(c)
                    
                        
        for ea in self.mines:
            nbrs = self.neighbors(ea)
            
            only_one = [x for x in nbrs if x in knowledgedict.keys() and knowledgedict[x] == 1]
            
            
            for each_cell in only_one:
                
                already_touching_one_mine = self.neighbors(each_cell)
                
                for c in already_touching_one_mine:
                    if not c in self.mines:
                        self.safes.add(c)

        print("Safe Cells Identified: ", self.safes)
        print("Mines Identified: ", self.mines, "\n\n")
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

        x, y = cell
        nbrs = [(x+i, y+j) for i in (-1,0,1) for j in (-1,0,1)]
        nbrs = [x for x in nbrs if x[0] >= 0 and x[-1] >= 0 and x[0] < self.height and x[-1] < self.width]

        return set(nbrs)
