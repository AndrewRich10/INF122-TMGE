# Import necessary modules
import random
from enum import Enum
from typing import List, Callable, Optional, Any


# Enum for Direction
class Direction(Enum):
    UP = "UP"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    DOWN = "DOWN"
    UL = "UL"  # Upper Left
    UR = "UR"  # Upper Right
    DL = "DL"  # Down Left
    DR = "DR"  # Down Right


# TileContents class
class TileContents:
    def __init__(self, colors: List[str]):
        self.colors = colors
        self.content = random.choice(colors)

    def getRandomColor(self) -> str:
        return random.choice(self.colors)

    def matchHorizontal(self, x: int) -> bool:
        return self.content == x

    def matchVertical(self, x: int) -> bool:
        return self.content == x

    def matchDiagonal(self, x: int) -> bool:
        return self.content == x

    def matchAllDirections(self, x: int) -> bool:
        return self.content == x

    def swapPositions(self, tile: 'Tile') -> None:
        self.content, tile.contents.content = tile.contents.content, self.content

    def isEmpty(self) -> bool:
        return self.content == ""

    def clearContent(self) -> None:
        self.content = ""


# Tile class
class Tile:
    def __init__(self, position: tuple, colors: List[str], board: 'Board'):
        self.position = position
        self.contents = TileContents(colors)
        self.board = board
        self.partOfShape = None  # To be used with TileShape

    def __repr__(self):
        return self.contents.content or " "


# Board class
class Board:
    def __init__(self, height: int, width: int, colors: List[str]):
        self.height = height
        self.width = width
        self.board = [[Tile((i, j), colors, self) for j in range(width)] for i in range(height)]
        self.matchingFunction: Optional[Callable] = None
        self.colors = colors

    def swapPositions(self, t1: Tile, t2: Tile) -> None:
        t1.contents.swapPositions(t2)

    def clearMatches(self) -> None:
        matched = False
        to_clear = set()

        # Horizontal matches
        for i in range(self.height):
            for j in range(self.width - 2):
                if self.board[i][j].contents.content == self.board[i][j + 1].contents.content == self.board[i][j + 2].contents.content != "":
                    to_clear.update({(i, j), (i, j + 1), (i, j + 2)})
                    matched = True

        # Vertical matches
        for j in range(self.width):
            for i in range(self.height - 2):
                if self.board[i][j].contents.content == self.board[i + 1][j].contents.content == self.board[i + 2][j].contents.content != "":
                    to_clear.update({(i, j), (i + 1, j), (i + 2, j)})
                    matched = True

        # Clear matched tiles
        for x, y in to_clear:
            self.board[x][y].contents.clearContent()

        return matched

    def applyGravity(self) -> None:
        # Make tiles fall down to fill empty spaces
        for j in range(self.width):
            empty_slots = []
            for i in range(self.height - 1, -1, -1):
                if self.board[i][j].contents.isEmpty():
                    empty_slots.append(i)
                elif empty_slots:
                    # Move tile down to the first available empty slot
                    empty_slot = empty_slots.pop(0)
                    self.board[empty_slot][j].contents.content = self.board[i][j].contents.content
                    self.board[i][j].contents.clearContent()
                    empty_slots.append(i)

    def fillMissingTiles(self) -> None:
        # Replace empty tiles with new random tiles
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j].contents.isEmpty():
                    self.board[i][j].contents.content = random.choice(self.colors)

    def isTileAt(self, x: int, y: int) -> bool:
        return 0 <= x < self.height and 0 <= y < self.width

    def getTileAt(self, x: int, y: int) -> Optional[Tile]:
        if self.isTileAt(x, y):
            return self.board[x][y]
        return None

    def setTileAt(self, x: int, y: int, tile: Tile) -> None:
        if self.isTileAt(x, y):
            self.board[x][y] = tile

    def isWithinBounds(self, x: int, y: int) -> bool:
        return self.isTileAt(x, y)

    def getBoardDisplay(self) -> str:
        return "\n".join([" ".join([str(tile) for tile in row]) for row in self.board])


# Testing the enhanced Board class with match clearing, gravity, and refill
if __name__ == "__main__":
    colors = ['R', 'G', 'B', 'Y']  # Red, Green, Blue, Yellow
    board = Board(5, 5, colors)
    print("Initial Board:")
    print(board.getBoardDisplay())

    # Simulate a match-clear-fill cycle
    while board.clearMatches():
        board.applyGravity()
        board.fillMissingTiles()

    print("\nBoard After Clearing Matches, Applying Gravity, and Refilling:")
    print(board.getBoardDisplay())
