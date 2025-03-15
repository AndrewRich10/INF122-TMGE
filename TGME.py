# Import necessary modules
import random
from enum import Enum
from typing import List, Callable, Optional, Any, Set


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
    def __init__(self, colors: List[Any]):
        self.colors = colors
        self.content = self.getRandomContent()

    def getRandomContent(self) -> Any:
        return random.choice(self.colors)

    def swapPositions(self, tile: 'Tile') -> None:
        self.content, tile.contents.content = tile.contents.content, self.content

    def isEmpty(self) -> bool:
        return self.content is None

    def clearContent(self) -> None:
        self.content = None


# TileShape class
class TileShape:
    def __init__(self, hasGravity: bool, board: 'Board'):
        self.hasGravity = hasGravity
        self.board = board
        self.tiles = []
    
    def createTileShape(self, tiles: List['Tile']):
        self.tiles = tiles
        self.hasGravity = False
    
    def rotateTileShape(self): # row = position[0], column = position[1]
        # [ ,  ]
        # [R, Y] - Moves Y to be above R
        if self.tiles[1].position[0] == self.tiles[0].position[0]:
            if self.tiles[1].position[1] == self.tiles[0].position[1] + 1:
                new_position = (self.tiles[0].position[0] - 1, self.tiles[0].position[1])
                if not self.board.isTileAt(new_position[0], new_position[1]) and self.board.isWithinBounds(new_position[0], new_position[1]):
                    self.tiles[1].position = new_position
        # [Y,  ]
        # [R,  ] - Moves Y to be beside R and swaps their colors
        elif self.tiles[1].position[1] == self.tiles[0].position[1]:
            if self.tiles[1].position[0] == self.tiles[0].position[0] - 1:
                new_position = (self.tiles[0].position[0], self.tiles[0].position[1] + 1)
                if not self.board.isTileAt(new_position[0], new_position[1]) and self.board.isWithinBounds(new_position[0], new_position[1]):
                    self.tiles[1].position = new_position
                    self.board.swapPositions(self.tiles[0], self.tiles[1])
                    self.tiles = [self.tiles[1], self.tiles[0]]
    
    # Moves whole tile shape down 1 unit
    def moveTileShape(self):
        # If tile shape is horizontal
        if self.tiles[1].position[0] == self.tiles[0].position[0]:
            if self.tiles[1].position[1] == self.tiles[0].position[1] + 1:
                new_position1 = (self.tiles[0].position[0] + 1, self.tiles[0].position[1])
                new_position2 = (self.tiles[1].position[0] + 1, self.tiles[1].position[1])
                if not self.board.isTileAt(new_position1[0], new_position1[1]) and self.board.isWithinBounds(new_position[0], new_position[1]):
                    self.tiles[0].position = new_position1
                    self.tiles[1].position = new_position2
        # If tile shape is vertical
        elif self.tiles[1].position[1] == self.tiles[0].position[1]:
            if self.tiles[1].position[0] == self.tiles[0].position[0] - 1:
                new_position1 = (self.tiles[0].position[0] + 1, self.tiles[0].position[1])
                new_position2 = (self.tiles[1].position[0] + 1, self.tiles[1].position[1])
                if not self.board.isTileAt(new_position1[0], new_position1[1]) and not self.board.isTileAt(new_position2[0], new_position2[1]) and self.board.isWithinBounds(new_position[0], new_position[1]):
                    self.tiles[0].position = new_position1
                    self.tiles[1].position = new_position2

    def shiftTileShape(self, direction: Direction):
        match direction:
            case "UP":
                self.rotateTileShape()
            case "DOWN":
                self.moveTileShape()
            case "LEFT":
                # If tile shape is horizontal
                if self.tiles[1].position[0] == self.tiles[0].position[0]:
                    if self.tiles[1].position[1] == self.tiles[0].position[1] + 1:
                        new_position1 = (self.tiles[0].position[0], self.tiles[0].position[1] - 1)
                        new_position2 = (self.tiles[1].position[0], self.tiles[1].position[1] - 1)
                        if not self.board.isTileAt(new_position1[0], new_position1[1]) and self.board.isWithinBounds(new_position[0], new_position[1]):
                            self.tiles[0].position = new_position1
                            self.tiles[1].position = new_position2
                # If tile shape is vertical
                elif self.tiles[1].position[1] == self.tiles[0].position[1]:
                    if self.tiles[1].position[0] == self.tiles[0].position[0] - 1:
                        new_position1 = (self.tiles[0].position[0], self.tiles[0].position[1] - 1)
                        new_position2 = (self.tiles[1].position[0], self.tiles[1].position[1] - 1)
                        if not self.board.isTileAt(new_position1[0], new_position1[1]) and not self.board.isTileAt(new_position2[0], new_position2[1]) and self.board.isWithinBounds(new_position[0], new_position[1]):
                            self.tiles[0].position = new_position1
                            self.tiles[1].position = new_position2
            case "RIGHT":
                # If tile shape is horizontal
                if self.tiles[1].position[0] == self.tiles[0].position[0]:
                    if self.tiles[1].position[1] == self.tiles[0].position[1] + 1:
                        new_position1 = (self.tiles[0].position[0], self.tiles[0].position[1] + 1)
                        new_position2 = (self.tiles[1].position[0], self.tiles[1].position[1] + 1)
                        if not self.board.isTileAt(new_position1[0], new_position1[1]) and self.board.isWithinBounds(new_position[0], new_position[1]):
                            self.tiles[0].position = new_position1
                            self.tiles[1].position = new_position2
                # If tile shape is vertical
                elif self.tiles[1].position[1] == self.tiles[0].position[1]:
                    if self.tiles[1].position[0] == self.tiles[0].position[0] - 1:
                        new_position1 = (self.tiles[0].position[0], self.tiles[0].position[1] + 1)
                        new_position2 = (self.tiles[1].position[0], self.tiles[1].position[1] + 1)
                        if not self.board.isTileAt(new_position1[0], new_position1[1]) and not self.board.isTileAt(new_position2[0], new_position2[1]) and self.board.isWithinBounds(new_position[0], new_position[1]):
                            self.tiles[0].position = new_position1
                            self.tiles[1].position = new_position2

    def removeTileShape(self):
        self.unlinkAllTiles()
        self.tiles = []

    def unlinkAllTiles(self):
        self.hasGravity = True
        self.tiles[0].partOfShape = None
        self.tiles[1].partOfShape = None


# Tile class
class Tile:
    def __init__(self, position: tuple, colors: List[Any], board: 'Board'):
        self.position = position
        self.contents = TileContents(colors)
        self.board = board
        self.partOfShape = None

    def __repr__(self):
        return repr(self.contents.content) if self.contents.content is not None else " "


# Board class
class Board:
    def __init__(self, height: int, width: int, colors: List[Any]):
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
        if self.isWithinBounds(x, y):
            return not self.board[x][y].contents.isEmpty()
            

    def getTileAt(self, x: int, y: int) -> Optional[Tile]:
        if self.isTileAt(x, y):
            return self.board[x][y]
        return None

    def setTileAt(self, x: int, y: int, tile: Tile) -> None:
        if self.isWithinBounds(x, y):
            self.board[x][y] = tile

    def isWithinBounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.height and 0 <= y < self.width

    def getBoardDisplay(self) -> str:
        return "\n".join([" ".join([str(tile) for tile in row]) for row in self.board])
    
    def getMatchingSets(self) -> Set[Tile]:
        matched_tiles = set()

        # Horizontal matches
        for i in range(self.height):
            for j in range(self.width - 2):
                if (self.board[i][j].contents.content == self.board[i][j + 1].contents.content == 
                    self.board[i][j + 2].contents.content and self.board[i][j].contents.content is not None):
                    matched_tiles.update({self.board[i][j], self.board[i][j + 1], self.board[i][j + 2]})

        # Vertical matches
        for j in range(self.width):
            for i in range(self.height - 2):
                if (self.board[i][j].contents.content == self.board[i + 1][j].contents.content == 
                    self.board[i + 2][j].contents.content and self.board[i][j].contents.content is not None):
                    matched_tiles.update({self.board[i][j], self.board[i + 1][j], self.board[i + 2][j]})

        return matched_tiles

    def clearTileSet(self, ts: Set[Tile]) -> None:
        for tile in ts:
            tile.contents.clearContent()

    def getMatchingBoardDisplay(self) -> str:
        matched_tiles = self.getMatchingSets()

        return "\n".join([ 
            " ".join(
                str(tile.contents.content) if tile in matched_tiles else "." for tile in row
            )
            for row in self.board
        ])


# Player class
class PlayerProfile:
    def __init__(self, player_id: int, colors: List[str], height: int, width: int):
        self.player_id = player_id
        self.board = Board(height, width, colors)
        self.score = 0

    def __repr__(self):
        return f"Player {self.player_id}"


# Game logic to handle 2 players
def play_game():
    colors = ['R', 'G', 'B', 'Y']  # Red, Green, Blue, Yellow
    height = 5
    width = 5

    # Create two players with their respective boards
    player1 = PlayerProfile(1, colors, height, width)
    player2 = PlayerProfile(2, colors, height, width)
    current_player = player1  # Start with Player 1

    while True:
        print(f"\n{current_player}'s turn")
        print(current_player.board.getBoardDisplay())


        try:
            # Get first tile to swap
            first_tile_input = input("First tile (row col): ").strip()
            if first_tile_input.lower() == 'exit':
                print("Game Over!")
                break

            first_row, first_col = map(int, first_tile_input.split())
            first_tile = current_player.board.getTileAt(first_row, first_col)

            # Get second tile to swap
            second_tile_input = input("Second tile (row col): ").strip()
            if second_tile_input.lower() == 'exit':
                print("Game Over!")
                break

            second_row, second_col = map(int, second_tile_input.split())
            second_tile = current_player.board.getTileAt(second_row, second_col)

            if first_tile and second_tile:
                current_player.board.swapPositions(first_tile, second_tile)
                print(f"{current_player} Board after tile swaps:")
                print(current_player.board.getBoardDisplay())

                print(f"{current_player} Board matches:")
                print(current_player.board.getMatchingBoardDisplay())

                # After swapping, clear matches and apply gravity
                while current_player.board.clearTileSet(current_player.board.getMatchingSets()):
                    current_player.board.applyGravity()
                    current_player.board.fillMissingTiles()
                
                current_player.board.fillMissingTiles()
                print(f"{current_player} Board after matches cleared:")
                print(current_player.board.getBoardDisplay())

                # Switch players
                current_player = player2 if current_player == player1 else player1
            else:
                print("Invalid tile positions. Try again.")
        except ValueError:
            print("Invalid input. Please enter valid row and column numbers.")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    print("Welcome to TMGE! Input 'exit' at any time to quit the game for both users!")
    play_game()


# # Testing the enhanced Board class with match clearing, gravity, and refill
# if __name__ == "__main__":
#     colors = ['R', 'G', 'B', 'Y']  # Red, Green, Blue, Yellow
#     board = Board(5, 5, colors)
#     print("Initial Board:")
#     print(board.getBoardDisplay())

#     # Simulate a match-clear-fill cycle
#     while board.clearMatches():
#         board.applyGravity()
#         board.fillMissingTiles()

#     print("\nBoard After Clearing Matches, Applying Gravity, and Refilling:")
#     print(board.getBoardDisplay())
