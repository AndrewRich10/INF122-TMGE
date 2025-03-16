from TMGE import *
import copy
from time import sleep

RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"
ORANGE = "\033[38;5;214m"
YELLOW = "\033[33m"
BLUE = "\033[34m"    
WHITE = "\033[37m"   
PURPLE = "\033[35m"   

class Jewel:
    def __init__(self, letter: str, color_code: str):
        self.body = letter
        self.color_code = color_code
        self.matching = False
    def __repr__(self):
        border: str
        if self.matching:
            border = '!'
        else:
            border = ' '
        return self.color_code + border + self.body + border + RESET
    
class BejeweledGameOver(Exception):
    pass
    
class Bejeweled:
    def __init__(self, players: list[PlayerProfile]):
        self._board: Board = Board(8, 8, [Jewel('R', RED), Jewel('G', GREEN), Jewel('B', BLUE), Jewel('Y', YELLOW), Jewel('O', ORANGE), Jewel('P', PURPLE), Jewel('W', WHITE)])
        self._makeInitialBoard()
        self._turnsToPlay: int = len(players) * 5
        self._player_turn = 0
        self._currentTurnNumber = 1
        self._players: list[PlayerProfile] = players
        self._scores: dict[int, int] = {}
        for player in players:
            self._scores[player.player_id] = 0

    def playGame(self)-> dict[int, int]:
        try:
            self._runGame()
        except BejeweledGameOver:
            pass
        return self._scores
    
    def _runGame(self):
        self._showBoardAndScore()
        while (self._currentTurnNumber <= self._turnsToPlay):
            jewel1, jewel2 = self._collectMovePhase() # Collect moves until valid

            self._handleMovePhase(jewel1, jewel2) # Handle the move provided

            self._cascadePhase() # Cascading phase / Match Failure, game over

            self._currentTurnNumber += 1 # End of Turn
            self._player_turn = (self._currentTurnNumber - 1) % len(self._players)
            self._showBoardAndScore()
        self._concludeGame() # Game Complete Phase
        return
    
    def _concludeGame(self):
        print("\nGAME OVER!\n\nTotal Score:")
        for player in self._players:
            print("Player " + str(player.player_id) + ": " + str(self._scores[player.player_id]))
    
    def _gameOver(self):
        print("\nYour move failed to cause a match. Player " + str(self._players[self._player_turn].player_id) + " loses.\n\nGAME OVER!")
        raise BejeweledGameOver()
    
    def _showBoardAndScore(self):
        print("\n" * 20)
        print(self._board.getBoardDisplay())
        print("\nPlayer " + str(self._players[self._player_turn].player_id) + ", Turn " + str(self._currentTurnNumber) + "/" + str(self._turnsToPlay))
        print("Score " + str(self._scores[self._players[self._player_turn].player_id]))
    
    def _cascadePhase(self):
        matchSet = self._board.getMatchingSets()
        if (len(matchSet) == 0):
            self._gameOver()
        while (len(matchSet) != 0):
            self._showBoardAndScore() # Board after move or refill
            sleep(1)

            self._markMatchers(matchSet) # Board During Matches
            self._scores[self._player_turn] += len(matchSet)
            self._showBoardAndScore()
            sleep(1)

            self._board.clearTileSet(matchSet) # Board after matches
            self._showBoardAndScore()
            sleep(1)

            self._board.applyGravity() # Board after gravity
            self._showBoardAndScore()
            sleep(1)

            self._refillBoard() # Perform refill        
            matchSet = self._board.getMatchingSets()

    def _markMatchers(self, matchers: Set[Tile]):
        for tile in matchers:
            tile.contents.content = copy.deepcopy(tile.contents.content)
            tile.contents.content.matching = True

    def _handleMovePhase(self, jewel1: Tile, jewel2: Tile):
        self._board.swapPositions(jewel1, jewel2)
        self._showBoardAndScore()
    
    def _collectMovePhase(self) -> tuple[Tile, Tile]:
        while (True):
            try:
                # Get first tile to swap
                first_tile_input = input("First jewel (row col): ").strip()

                first_row, first_col = map(int, first_tile_input.split())
                first_row -= 1
                first_col -= 1
                first_tile = self._board.getTileAt(first_row, first_col)
                if not self._board.isWithinBounds(first_row, first_col):
                    raise ValueError()

                # Get second tile to swap
                second_tile_input = input("Swap up, left, down, or right? (W/A/S/D): ").strip().lower()
                input_to_offset = {"w": (-1, 0), "a": (0, -1), "s": (1, 0), "d": (0, 1)}

                x, y = input_to_offset[second_tile_input] # Translate direction into move
                second_tile = self._board.getTileAt(first_row + x, first_col + y)
                if not self._board.isWithinBounds(first_row + x, first_col + y):
                    raise ValueError()
                return (first_tile, second_tile)
            except ValueError:
                self._showBoardAndScore()
                print("Invalid input. Please enter a valid position.")
            except Exception as e:
                print(f"An error occurred: {e}")
    
    def _refillBoard(self):
        replacementBoard: Board
        attempts = 0
        while (True):
            attempts += 1
            replacementBoard = copy.deepcopy(self._board)
            replacementBoard.fillMissingTiles()
            if (self._futureMatchesExist(replacementBoard)): 
                break
            if attempts > 100:
                self._makeInitialBoard()
                return
        self._board = replacementBoard

    def _makeInitialBoard(self):
        while (True):
            while (True):
                self._board.fillMissingTiles()
                matchset = self._board.getMatchingSets()
                if (len(matchset) == 0):
                    break
                else:
                    self._board.clearTileSet(matchset)
            if (self._futureMatchesExist(self._board)):
                break
            else:
                self._board = Board(8, 8, [Jewel('R', RED), Jewel('G', GREEN), Jewel('B', BLUE), Jewel('Y', YELLOW), Jewel('O', ORANGE), Jewel('P', PURPLE), Jewel('W', WHITE)])
            
    def _matchesExist(self, board: Board):
        return len(board.getMatchingSets()) > 0

    def _futureMatchesExist(self, board: Board) -> bool:
        def hasMatchingMove(x: int, y: int, board: Board):
            for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                xb = x + i
                yb = y + j
                if not board.isWithinBounds(xb, yb):
                    continue
                tile1 = board.getTileAt(x, y)
                tile2 = board.getTileAt(xb, yb)
                board.swapPositions(tile1, tile2)
                if (self._matchesExist(board)):
                    return True
                else:
                    board.swapPositions(tile1, tile2)
            return False

        scenarioBoard = copy.deepcopy(board)
        for x in range(0, self._board.width):
            for y in range(0, self._board.height):
                if hasMatchingMove(x, y, scenarioBoard):
                    return True
        return False

if __name__ == '__main__':
    game = Bejeweled([PlayerProfile(0, [], 0, 0), PlayerProfile(1, [], 0, 0)])
    game = Bejeweled([PlayerProfile(0, [], 0, 0)]) # Current setting: Play Bejeweled with 1 player
    game.playGame()