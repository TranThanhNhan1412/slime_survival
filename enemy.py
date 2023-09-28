import math
import arcade
import random
from constain import *


class Enemy(arcade.Sprite):

    def __init__(self, name, start_x, start_y):
        super().__init__()

        self.name = name
        self.action = "Idle"  # IDLE,WALK,ATTACK,TELEPORTING
        self.speed = ENEMY_SPEED
        self.is_stuck = False
        self.texture_frame = 0  # 0--> last texture --> 0->...
        self.texture_frame_count = 0  # 0--> last texture --> 0->...

        self.init_x = start_x
        self.init_y = start_y

        self.center_x = start_x
        self.center_y = start_y

        # Load sound
        self.attack_sound = arcade.load_sound(SOUND_PATH+"slime_attack.mp3")
        self.walk_sound = arcade.load_sound(SOUND_PATH+"player_walk.wav")
        self.die_sound = arcade.load_sound(SOUND_PATH+"slime_die.wav")

        # Load textures
        self.idle_textures = get_texture_files("Plan_slime/Idle")
        self.walk_textures = get_texture_files("Plan_slime/Walk")
        self.attack_textures = get_texture_files("Plan_slime/Attack")
        self.die_textures = get_texture_files("Plan_slime/Die")

        self.scale = PLAYER_SCALING
        self.texture = self.idle_textures[0]

    def auto_walking(self, end_x, end_y):
        self.texture_frame_count = 0
        self.texture_frame = 1
        self.action = "Walk"
        self.center_x += self.change_x
        self.center_y += self.change_y
        diff_x = end_x - self.center_x
        diff_y = end_y - self.center_y
        
        if random.randrange(100) == 0:
            if (diff_x<15 and diff_y<15):
                self.is_attacking()
            else:
                if (diff_x > diff_y):
                    self.change_x = self.speed
                else:
                    self.change_y = self.speed
                

    def is_attacking(self):
        if self.action!='Attack':
            arcade.play_sound(self.attack_sound)
            self.texture_frame_count = 0
            self.texture_frame = 1
            self.action = "Attack"

    def is_idle(self):
        self.texture_frame_count = 0
        self.texture_frame = 1
        self.action = "Idle"

    def update_animation_and_sound(self):
        self.texture_frame_count += 1
        if self.texture_frame_count % ENEMY_FPS == 0:
            self.texture_frame += 1
            self.texture_frame_count = 0
            if self.action == "Walk":
                arcade.play_sound(self.walk_sound)

        if self.action == "Idle":
            ind = self.texture_frame % (len(self.idle_textures))
            self.texture = self.idle_textures[ind]

        if self.action == "Walk":
            ind = self.texture_frame % (len(self.walk_textures))
            self.texture = self.walk_textures[ind]

        if self.action == "Attack":
            ind = self.texture_frame % (len(self.attack_textures))
            self.texture = self.attack_textures[ind]
            if (self.texture_frame == len(self.attack_textures)):
                self.is_idle()
