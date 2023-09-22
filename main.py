import os
import math
import time
import arcade
from constain import *

from player import Player


class MyGame(arcade.Window):
    """Main application class."""

    def __init__(self):
        """
        Initializer
        """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

        # Tilemap Object
        self.tile_map = None
        self.map_width = SCREEN_WIDTH
        self.map_height = SCREEN_HEIGHT
        self.teleport = None

        # scene
        self.scene = None

        # player
        self.player = None
        self.physics_engine = None

        # Fps
        self.last_time = None
        self.frame_count = 0
        self.fps_message = None

        # Cameras
        self.camera = None
        self.gui_camera = None
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # Load sounds
        self.teleport_sound = arcade.load_sound(SOUND_PATH+"teleport.wav")

    def setup(self):
        """Set up the game and initialize the variables."""

        # Scene
        self.scene = arcade.Scene()

        # Map
        self.create_map()
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
        self.scene.add_sprite_list_after("Player", "fence_wall")
        self.scene.add_sprite_list_before("Player", "tree")

        # player
        self.player = Player("Machine", self.map_width /2, self.map_height / 2)
        self.scene.add_sprite("Player", self.player)

        # obstructions
        obstructions = [self.tile_map.sprite_lists["fence_wall"],]
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player,
            obstructions
        )

        # camera
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

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

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Call update on all sprites
        self.physics_engine.update()
        self.camera.resize(self.width, self.height)
        self.gui_camera.resize(self.width, self.height)
        # Pan to the user
        self.player.pan_camera_arround(
            self.camera, self.map_width, self.map_height)
        self.player.update_animation_and_sound()

        is_in_teleport = arcade.check_for_collision_with_lists(
            self.player, self.teleport,
        )
        for _ in is_in_teleport:
            if (self.player.action != "TELEPORTING"):
                self.player.action = "TELEPORTING"
                arcade.play_sound(self.teleport_sound)

    def on_key_press(self, key, modifiers):
        if key in self.player.MOVE_KEY or key in self.player.ATTACK_KEY:
            self.player.on_key_press_action(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.player.on_key_release(key, modifiers)

    def create_map(self):
        #  maps
        layer_options = {
            "tree": {"use_spatial_hash": True},
            "fence_wall": {"use_spatial_hash": True},
            "background": {"use_spatial_hash": True},
            "ground": {"use_spatial_hash": True},
            "teleport": {"use_spatial_hash": True},
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(
            MAP['delta'], layer_options=layer_options,
            scaling=TILE_SCALING
        )
        self.map_width = self.tile_map.width * GRID_PIXEL_SIZE
        self.map_height = self.tile_map.height * GRID_PIXEL_SIZE

        self.teleport = [
            self.tile_map.sprite_lists["teleport"],
        ]


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
