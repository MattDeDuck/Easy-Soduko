import pygame
import sys
from data import *
from puzzle import *
from button import *


class SudokuApp:
    pygame.display.set_caption('Easy Sudoku') 

    def __init__(self):

        pygame.init()
        pygame.font.init()

        # Set the window width and height
        self.window = pygame.display.set_mode((s_WIDTH, s_HEIGHT))
        # Set the font to be used
        self.font = pygame.font.SysFont("helvetica", 20)

        self.running = True
        self.selected = None
        self.mousePos = None
        self.grid = []
        self.finishedBoard = []
        self.filledCells = []
        self.wrongCells = []
        self.puzzleno = ""
        self.correct = 0
        self.correctCells = []
        self.spacescheck = 0

        self.greenbutton = button((40,40,40), s_WIDTH//2-75, 15, 150, 30,text="New Game")

        self.load()


    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
        pygame.quit()
        sys.exit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            posit = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEMOTION:
                if self.greenbutton.isOver(posit):
                    self.greenbutton.colour = (0,0,0)
                else:
                    self.greenbutton.colour = (40,40,40)

            if event.type == pygame.MOUSEBUTTONDOWN:

                if self.greenbutton.isOver(posit):
                    self.load()

                # Check if the mouse is on the grid
                selected = self.checkMouseOnGrid()
                if(selected):
                    # if on grid set the positions on the grid
                    self.selected = selected                 
                else:
                    # If user clicked outside the board
                    selected = None

            if event.type == pygame.KEYDOWN:
                # If user selects a square on the board that isn't filled already
                if self.selected != None and self.selected not in self.filledCells:
                    # Check to see if it's a number
                    if self.isDigit(event.unicode):
                        # Get the typed number
                        tNumber = int(event.unicode)
                        # Get the number to check against from the completed board
                        fNumber = int(self.finishedBoard[self.selected[1]][self.selected[0]])                        

                        # If it's 0 or higher than 9 then don't display it
                        if tNumber == int(0) or tNumber > int(9):
                            if (self.selected[0], self.selected[1]) in self.wrongCells:
                                    self.wrongCells.remove((self.selected[0], self.selected[1]))
                                    self.grid[self.selected[1]][self.selected[0]] = 0
                            pass
                        # If it's 1-9 that's typed
                        else:
                            # Check the number against correct board number
                            if tNumber == fNumber:
                                # Check to see if in wrong cell list
                                if (self.selected[0], self.selected[1]) in self.wrongCells:
                                    # In the list so need to remove it
                                    self.wrongCells.remove((self.selected[0], self.selected[1]))

                                    if (self.selected[0], self.selected[1]) in self.correctCells:
                                        #already added
                                        pass
                                    else:
                                        self.correctCells.append((self.selected[0], self.selected[1]))
                                        self.correct += 1
                                else:
                                    # Not in list, no need to add it
                                    if (self.selected[0], self.selected[1]) in self.correctCells:
                                        #already added
                                        pass
                                    else:
                                        self.correctCells.append((self.selected[0], self.selected[1]))
                                        self.correct += 1
                                    pass                        
                            else:
                                if (self.selected[0], self.selected[1]) in self.wrongCells:
                                    pass
                                else:                       
                                    self.wrongCells.append((self.selected[0], self.selected[1]))

                            
                            # Update the board with the number the user typed
                            self.grid[self.selected[1]][self.selected[0]] = int(event.unicode)

                            if len(self.correctCells) == self.spacescheck:
                                # player has completed the board
                                print("Woohoo board done!")

    # Get the mouse position
    def update(self):
        self.mousePos = pygame.mouse.get_pos()

    def draw(self):
        # Set window background to white
        self.window.fill((WHITE))

        self.greenbutton.draw(self.window, 1)
        
        # If a square on the grid is selected, draw it
        if(self.selected):
            self.drawSelectedSquare(self.window, self.selected)

        # Draw filled cells background
        self.drawFilled(self.window, self.filledCells)

        # Draw the cells that are wrong
        self.drawWrong(self.window, self.wrongCells)

        # Draw the numbers
        self.fillGrid(self.window)
        
        # Draw the grid outlines
        self.drawGrid()

        # Update the display
        pygame.display.update()


############

    # Cells that are filled
    def drawFilled(self, window, filled):
        for cell in filled:
            pygame.draw.rect(window, BLUE, (cell[0]*cellSize+gridPos[0], cell[1]*cellSize+gridPos[1], cellSize, cellSize))

    # Cells that are wrong
    def drawWrong(self, window, wrong):
        for cell in wrong:
            pygame.draw.rect(window, RED, (cell[0]*cellSize+gridPos[0], cell[1]*cellSize+gridPos[1], cellSize, cellSize))

    # Grid outlines
    def drawGrid(self):
        # Draw the main outside
        pygame.draw.rect(self.window, BLACK, (gridPos[0],gridPos[1],450,450), 2)

        # Draw the lines inside
        for x in range(9):
            if x % 3 != 0:
                # Normal lines
                pygame.draw.line(self.window, BLACK, (gridPos[0]+(x*cellSize),gridPos[1]), (gridPos[0]+(x*cellSize), gridPos[1]+450))
                pygame.draw.line(self.window, BLACK, (gridPos[0],gridPos[1]+(x*cellSize)), (gridPos[0]+450, gridPos[1]+(x*cellSize)))
            else:
                # Thicker lines
                pygame.draw.line(self.window, BLACK, (gridPos[0]+(x*cellSize),gridPos[1]), (gridPos[0]+(x*cellSize), gridPos[1]+450),2)
                pygame.draw.line(self.window, BLACK, (gridPos[0],gridPos[1]+(x*cellSize)), (gridPos[0]+450, gridPos[1]+(x*cellSize)),2)

    # Change square colour if the square is selected
    def drawSelectedSquare(self, window, pos):
        pygame.draw.rect(window, (200,200,200), ((pos[0]*cellSize)+gridPos[0], (pos[1]*cellSize)+gridPos[1], cellSize, cellSize))


    # If the mouse is outside our board position return false
    def checkMouseOnGrid(self):
        if self.mousePos[0] < gridPos[0] or self.mousePos[1] < gridPos[1]:
            return False
        if self.mousePos[0] > gridPos[0]+450 or self.mousePos[1] > gridPos[1]+450:
            return False
        
        # Return the position of the click on our grid
        xx = (self.mousePos[0]-gridPos[0])//cellSize
        yy = (self.mousePos[1]-gridPos[1])//cellSize
        
        return(xx, yy)

    # Prepare the text for the grid
    def drawText(self, window, text, pos):
        font = self.font.render(text, False, BLACK)
        fontWidth = font.get_width()
        fontHeight = font.get_height()
        pos[0] += (cellSize-fontWidth)//2
        pos[1] += (cellSize-fontHeight)//2
        window.blit(font, pos)

    # Grab the numbers from the grid array
    def fillGrid(self, window):
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num != int(0):
                    pos = [(xidx*cellSize)+gridPos[0], (yidx*cellSize+gridPos[1])]
                    self.drawText(window, str(num), pos)
                    
    # Load the board
    def load(self):
        self.filledCells = []
        self.correct = 0

        self.grid, self.puzzleno, self.spacescheck = get_Puzzle()
        self.finishedBoard = get_Puzzle_solution(self.puzzleno)

        # Setting locked cells from original board
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num != int(0):
                    self.filledCells.append([xidx, yidx])
                    


    # Check if it's a number or not
    def isDigit(self, string):
        try:
            int(string)
            return True
        except:
            return False