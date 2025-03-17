from TMGE import *
import random

shapes = {0 : ((1, 4), (1, 5), (1, 6), (1, 7)), 1 : ((0, 5), (0, 6), (1, 5), (1, 6)), 2 : ((0, 4), (1, 4), (1, 5), (1, 6)),\
          3 : ((1, 5), (1, 6), (1, 7), (0, 7)), 4 : ((0, 5), (1, 4), (1, 5), (1, 6)), 5: ((1, 5), (1, 6), (0, 6), (0, 7)),\
            6 : ((0, 5), (0, 6), (1, 6), (1, 7))}

class Tetris:
    def __init__(self):
        self.colors = ['R', 'G', 'B']
        self.player = PlayerProfile(1, self.colors, 20, 10)
        self.player.board.clearBoard()
        self.current_tile_shape = TileShape(True, self.player.board)

    def spawn_shape(self):
        shape = shapes[random.randint(0, 6)]
        tiles = [Tile(pos, self.colors, self.player.board) for pos in shape]
        for tile in tiles:
            self.player.board.board[tile.position[0]][tile.position[1]] = tile
        self.current_tile_shape.createTileShape(tiles)

    def play_game(self):
        self.spawn_shape()

        print("Game Start!")
        while True:
            print("\nCurrent Board:")
            print(self.player.board.getBoardDisplay())

            move = input("\nEnter your move (left, right, down, rotate, pass, exit): ").strip().lower()
            if move == "exit":
                print("Exiting game.")
                break
            elif move == "left":
                self.current_tile_shape.shiftTileShape(Direction.LEFT)
            elif move == "right":
                self.current_tile_shape.shiftTileShape(Direction.RIGHT)
            elif move == "down":
                self.current_tile_shape.shiftTileShape(Direction.DOWN)
            elif move == "rotate":
                self.current_tile_shape.shiftTileShape(Direction.UP)

            self.current_tile_shape.moveTileShape()

            landed = False
            for tile in self.current_tile_shape.tiles:
                if tile.position[0] == self.player.board.height - 1:
                    landed = True
                    break
                
                if self.player.board.isTileAt(tile.position[0] + 1, tile.position[1]) \
                    and self.player.board.board[tile.position[0] + 1][tile.position[1]] not in self.current_tile_shape.tiles:
                    landed = True
                    break

            if landed:
                self.player.board.clearHorizontal()
                if any(tile.position[0] == 0 for tile in self.current_tile_shape.tiles):
                    print("Game Over!")
                    break
                self.spawn_shape()
            
if __name__ == '__main__':
    tetris = Tetris()
    tetris.play_game()