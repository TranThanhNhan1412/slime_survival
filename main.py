import time
import arcade
from constain import *


class MyGame(arcade.Window):
    """Main application class."""

    def __init__(self):
        """
        Initializer
        """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

        # Tilemap Object
        self.tile_map = None
        self.scene = None

        # Set up the player
        self.player_sprite = None
        self.physics_engine = None

        # player
        self.player_action = None
        self.player_face_direction = None

        # Fps
        self.last_time = None
        self.frame_count = 0
        self.fps_message = None

        # Cameras
        self.camera = None
        self.gui_camera = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game and initialize the variables."""

        # Scene
        self.scene = arcade.Scene()

        self.create_map()
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
        self.scene.add_sprite_list_after("Player","river")
        self.scene.add_sprite_list_before("Player","river")
        self.scene.add_sprite_list_before("Player","river")

        self.create_player()
        self.scene.add_sprite("Player", self.player_sprite)

        obstructions = [self.tile_map.sprite_lists["river"],]

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            obstructions
        )

        # camera
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)
        self.pan_camera_to_player()

    def on_draw(self):
        """
        Render the screen.
        """
        self.clear()
        self.camera.use()
        self.scene.draw()
        self.gui_camera.use()
        self.calc_and_draw_fps()

    def calc_and_draw_fps(self):
        # Start counting frames
        self.frame_count += 1
        # Calculate FPS if conditions are met
        if self.last_time and self.frame_count % 60 == 0:
            fps = 1.0 / (time.time() - self.last_time) * 60
            self.fps_message = f"FPS: {fps:5.0f}"
        # Draw FPS text
        if self.fps_message:
            arcade.draw_text(
                self.fps_message,
                10,
                40,
                arcade.color.BLACK,
                14
            )
        # Get time for every 60 frames
        if self.frame_count % 60 == 0:
            self.last_time = time.time()

    def on_key_press(self, key, modifiers):
        self.player_action = "Walk"
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_face_direction = "LEFT"
            self.player_sprite.change_x = - MOVEMENT_SPEED
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_face_direction = "RIGHT"
            self.player_sprite.change_x = MOVEMENT_SPEED
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_face_direction = "UP"
            self.player_sprite.change_y = MOVEMENT_SPEED
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.player_face_direction = "DOWN"
            self.player_sprite.change_y = - MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a mouse button.
        """
        self.player_action = "Idle"
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Call update on all sprites
        self.physics_engine.update()
        # Pan to the user
        self.pan_camera_to_player()

    def create_player(self):
        #  player
        self.player_action = "Idle"
        self.player_face_direction = "DOWN"
        self.player_sprite = arcade.Sprite(
            PLAYER_PATH+self.player_action+"/tile000.png",
            PLAYER_SCALING,
        )
        self.player_sprite.center_x = SCREEN_WIDTH/2
        self.player_sprite.center_y = SCREEN_HEIGHT/2

    def create_map(self):
        #  maps
        layer_options = {
            "delta": {"use_spatial_hash": True},
            "bridge": {"use_spatial_hash": True},
            "river": {"use_spatial_hash": True},

        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(
            MAP_PATH, layer_options=layer_options,
            scaling=TILE_SCALING
        )

    def pan_camera_to_player(self):

        # This spot would center on the user
        screen_center_x = self.player_sprite.center_x - \
            (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )
        user_centered = screen_center_x, screen_center_y
        self.camera.move_to(user_centered)


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
