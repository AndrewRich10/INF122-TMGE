# Import necessary modules
import random
from enum import Enum
from typing import List, Callable, Optional, Any, Set
from abc import ABC, abstractmethod

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
    
    def rotateTileShape(self):
        if len(self.tiles) < 2:
            return

        pivot = self.tiles[0].position
        new_tiles = []
        
        for tile in self.tiles:
            row, col = tile.position
            relative_row, relative_col = row - pivot[0], col - pivot[1]
            
            new_row = pivot[0] - relative_col
            new_col = pivot[1] + relative_row
            
            if not self.board.isWithinBounds(new_row, new_col):
                return
            
            if self.board.isTileAt(new_row, new_col) and self.board.board[new_row][new_col] not in self.tiles:
                return
            
            new_tiles.append((new_row, new_col, tile.contents.content))
        
        for tile in self.tiles:
            self.board.board[tile.position[0]][tile.position[1]].contents.clearContent()

        for i, (tile, (new_row, new_col, content)) in enumerate(zip(self.tiles, new_tiles)):
            self.board.setTileAt(new_row, new_col, content)
            self.tiles[i] = self.board.getTileAt(new_row, new_col)


    def moveTileShape(self):
        if not self.tiles:
            return
        
        new_tiles = []
        
        for tile in self.tiles:
            new_row = tile.position[0] + 1
            new_col = tile.position[1]
            
            if not self.board.isWithinBounds(new_row, new_col):
                return
            
            if self.board.isTileAt(new_row, new_col) and self.board.board[new_row][new_col] not in self.tiles:
                return
            
            new_tiles.append((new_row, new_col, tile.contents.content))
        
        for tile in self.tiles:
            self.board.board[tile.position[0]][tile.position[1]].contents.clearContent()

        for i, (tile, (new_row, new_col, content)) in enumerate(zip(self.tiles, new_tiles)):
            self.board.setTileAt(new_row, new_col, content)
            self.tiles[i] = self.board.getTileAt(new_row, new_col)



    def shiftTileShape(self, direction: Direction):
        if direction == Direction.UP:
            self.rotateTileShape()
        elif direction == Direction.DOWN:
            self.moveTileShape()
        else:
            delta_col = -1 if direction == Direction.LEFT else 1
            new_tiles = []

            for tile in self.tiles:
                new_row, new_col = tile.position[0], tile.position[1] + delta_col
                
                if not self.board.isWithinBounds(new_row, new_col):
                    return
                
                if self.board.isTileAt(new_row, new_col) and self.board.board[new_row][new_col] not in self.tiles:
                    return
                
                new_tiles.append((new_row, new_col, tile.contents.content))
            
            for tile in self.tiles:
                self.board.board[tile.position[0]][tile.position[1]].contents.clearContent()

            for i, (tile, (new_row, new_col, content)) in enumerate(zip(self.tiles, new_tiles)):
                self.board.setTileAt(new_row, new_col, content)
                self.tiles[i] = self.board.getTileAt(new_row, new_col)

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
        return repr(self.contents.content) if self.contents.content is not None else "   "


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

    def clearBoard(self) -> None:
        for i in range(self.height):
            for j in range(self.width):
                self.board[i][j].contents.content = None
    
    def clearHorizontal(self) -> None:
        cleared_rows = 0
        for i in range(len(self.board)):
            if all(cell.contents.content for cell in self.board[i]):
                cleared_rows += 1
                for cell in self.board[i]:
                    cell.contents.clearContent()
                
                for j in range(i, 0, -1):
                    for k in range(len(self.board[j])):
                        self.board[j][k].contents.content = self.board[j-1][k].contents.content


    def clearMatches(self) -> None:
        matched = False
        to_clear = set()

        # Horizontal matches
        for i in range(self.height):
            for j in range(self.width - 2):
                if self.board[i][j] and self.board[i][j + 1] and self.board[i][j + 2]:
                    if self.board[i][j] == self.board[i][j + 1] and self.board[i][j + 1] == self.board[i][j + 2]:
                        to_clear.update({(i, j), (i, j + 1), (i, j + 2)})
                        matched = True

        # Vertical matches
        for j in range(self.width):
            for i in range(self.height - 2):
                if self.board[i][j] and self.board[i + 1][j] and self.board[i + 2][j]:
                    if self.board[i][j] == self.board[i + 1][j] and self.board[i + 1][j] == self.board[i + 2][j]:
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

    def setTileAt(self, x: int, y: int, content: Tile) -> None:
        if self.isWithinBounds(x, y):
            self.board[x][y].contents.content = content

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

# ShellGame class:
class ShellGame(ABC):
    @abstractmethod
    def playGame(self) -> Optional[dict[int, int]|None]:
        pass


'''
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
'''


def play_game():
    colors = ['R', 'B', 'Y']  # Red, Blue, Yellow
    player = PlayerProfile(player_id=1, colors=colors, height=10, width=10)
    player.board.clearBoard()
    current_tile_shape = TileShape(hasGravity=True, board=player.board)
    
    # Create an initial random tile shape for the player
    def spawnCurrentTileShape():
        # Define a flexible initial shape (e.g., 3 tiles in a row)
        initial_positions = [(0, 4), (1, 4), (0, 5)]  # Example: horizontal line
        initial_tiles = [
            Tile(position=pos, colors=colors, board=player.board) for pos in initial_positions
        ]
        for tile in initial_tiles:
            tile.contents.content = tile.contents.getRandomContent()  # Assign random content
        for tile in initial_tiles:
            player.board.board[tile.position[0]][tile.position[1]] = tile
        current_tile_shape.createTileShape(initial_tiles)
    
    spawnCurrentTileShape()

    print("Game Start!")
    while True:
        print("\nCurrent Board:")
        print(player.board.getBoardDisplay())

        # Ask the player for input to move or rotate the tile shape
        move = input("\nEnter your move (left, right, down, rotate, pass, exit): ").strip().lower()
        if move == "exit":
            print("Exiting game.")
            break
        elif move == "left":
            current_tile_shape.shiftTileShape(Direction.LEFT)
        elif move == "right":
            current_tile_shape.shiftTileShape(Direction.RIGHT)
        elif move == "down":
            current_tile_shape.shiftTileShape(Direction.DOWN)
        elif move == "rotate":
            current_tile_shape.shiftTileShape(Direction.UP)  # Use the updated rotation method

        # Move the tile shape down if possible (gravity effect)
        current_tile_shape.moveTileShape()

        # Check if the tile shape has landed or reached the bottom
        landed = False
        for tile in current_tile_shape.tiles:
            # Check if any tile is at the bottom of the grid
            if tile.position[0] == player.board.height - 1:
                landed = True
                break
            # # Check if any tile is directly above another tile
            # if player.board.isTileAt(tile.position[0] + 1, tile.position[1]):
            #     landed = True
            #     break
            
            # Check if the new position is occupied by a tile not in the current TileShape
            if player.board.isTileAt(tile.position[0] + 1, tile.position[1]) \
                  and player.board.board[tile.position[0] + 1][tile.position[1]] not in current_tile_shape.tiles:
                return  # Cancel movement if any tile is occupied by an external tile

        if landed:
            # Clear matching sets if any
            player.board.clearTileSet(player.board.getMatchingSets())
            # Check for game over condition
            if any(tile.position[0] == 0 for tile in current_tile_shape.tiles):
                print("Game Over!")
                break
            # Spawn a new tile shape
            spawnCurrentTileShape()

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
