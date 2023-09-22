import os
import math
import time
import arcade

from constain import *


class Player(arcade.Sprite):
    MOVE_KEY = [
        arcade.key.LEFT,
        arcade.key.A,
        arcade.key.RIGHT,
        arcade.key.D,
        arcade.key.UP,
        arcade.key.W,
        arcade.key.DOWN,
        arcade.key.S
    ]
    ATTACK_KEY = [arcade.key.SPACE]

    def __init__(self, name, start_x, start_y):
        super().__init__()

        self.name = name
        self.action = "Idle"  # IDLE,WALK,ATTACK,TELEPORTING
        self.face_direction = "DOWN"  # DOWN, LEFT, UP, RIGHT
        self.texture_frame = 0  # 0--> last texture --> 0->...
        self.texture_frame_count = 0  # 0--> last texture --> 0->...

        self.center_x = start_x
        self.center_y = start_y

        # Load sound
        self.attack_sound = arcade.load_sound(
            SOUND_PATH+"player_machine_hit.mp3")
        self.walk_sound = arcade.load_sound(SOUND_PATH+"player_walk.wav")

        # Load textures
        self.idle_textures = {
            "UP": get_texture_files("Idle/UP"),
            "RIGHT": get_texture_files("Idle/RIGHT"),
            "DOWN": get_texture_files("Idle/DOWN"),
            "LEFT": get_texture_files("Idle/LEFT"),
        }
        self.walk_textures = {
            "UP": get_texture_files("Walk/UP"),
            "RIGHT": get_texture_files("Walk/RIGHT"),
            "DOWN": get_texture_files("Walk/DOWN"),
            "LEFT": get_texture_files("Walk/LEFT"),
        }
        self.attack_textures = {
            "UP": get_texture_files("Attack/UP"),
            "RIGHT": get_texture_files("Attack/RIGHT"),
            "DOWN": get_texture_files("Attack/DOWN"),
            "LEFT": get_texture_files("Attack/LEFT"),
        }
        self.scale = PLAYER_SCALING
        self.texture = self.idle_textures[self.face_direction][0]
        self.len_idle_textures = len(self.idle_textures[self.face_direction])
        self.len_walk_textures = len(self.walk_textures[self.face_direction])
        self.len_attack_textures = len(
            self.attack_textures[self.face_direction])

    def pan_camera_arround(self, camera, map_width, map_height):
        # This spot would center on the user
        if (self.center_x - camera.viewport_width / 2) < 0:
            camera_x = 0
        elif (self.center_x+camera.viewport_width / 2) > map_width:
            camera_x = map_width - camera.viewport_width
        else:
            camera_x = self.center_x - camera.viewport_width / 2
        if (self.center_y - camera.viewport_height / 2) < 0:
            camera_y = 0
        elif (self.center_y + camera.viewport_height / 2) > map_height:
            camera_y = map_height - camera.viewport_height
        else:
            camera_y = self.center_y - camera.viewport_height / 2
        camera.move_to([camera_x, camera_y])

    def on_key_press_action(self, key, modifiers):
        self.texture_frame_count = 0
        self.texture_frame = 1

        if key in Player.ATTACK_KEY:
            self.is_attacking()
        if key in Player.MOVE_KEY:
            self.change_face_direction(key)
            self.is_walking(PLAYER_SPEED)

    def change_face_direction(self, key):
        if key in [arcade.key.LEFT, arcade.key.A]:
            self.face_direction = "LEFT"
        if key in [arcade.key.RIGHT, arcade.key.D]:
            self.face_direction = "RIGHT"
        if key in [arcade.key.UP, arcade.key.W]:
            self.face_direction = "UP"
        if key in [arcade.key.DOWN, arcade.key.S]:
            self.face_direction = "DOWN"

    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if key in Player.MOVE_KEY:
            self.is_idle()
            self.change_x = 0
            self.change_y = 0

    def is_walking(self, speed):
        self.action = "Walk"
        if self.face_direction == "LEFT":
            self.change_x = - speed
        if self.face_direction == "RIGHT":
            self.change_x = speed
        if self.face_direction == "UP":
            self.change_y = speed
        if self.face_direction == "DOWN":
            self.change_y = - speed

    def is_attacking(self):
        self.action = "Attack"
        arcade.play_sound(self.attack_sound)

    def is_idle(self):
        self.action = "Idle"

    def update_animation_and_sound(self):
        self.texture_frame_count += 1
        if self.texture_frame_count % PLAYER_FPS.get(self.action, 1) == 0:
            self.texture_frame += 1
            self.texture_frame_count = 0
            if self.action == "Walk":
                arcade.play_sound(self.walk_sound)

        if self.action == "Idle":
            ind = self.texture_frame % (self.len_idle_textures)
            self.texture = self.idle_textures[self.face_direction][ind]

        if self.action == "Walk":
            ind = self.texture_frame % (self.len_walk_textures)
            self.texture = self.walk_textures[self.face_direction][ind]

        if self.action == "Attack":
            ind = self.texture_frame % (self.len_attack_textures)
            self.texture = self.attack_textures[self.face_direction][ind]
            if (self.texture_frame == self.len_attack_textures):
                self.is_idle()
