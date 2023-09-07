"""
Platformer Game
"""
import arcade
from arcade.application import Window

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Slime Survival"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
CHARACTER_SIZE = 16

TILE_SCALING = 1
TILE_SCALING = 32
# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 10


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        
    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

    def on_draw(self, delta_time: float):
        pass

    def on_update(self, delta_time: float):
        pass




def main():
    """Main function"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE,resizable=True)
    game_view = GameView()
    window.show_view(game_view)
    arcade.run()


if __name__ == "__main__":
    main()