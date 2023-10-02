import math
import arcade
import random
from constain import *


class Enemy(arcade.Sprite):

    def __init__(self, name, start_x, start_y, damage=1, health=10):
        super().__init__()

        # index
        self.name = name
        self.action = "Idle"  # IDLE,WALK,ATTACK,DIE
        self.speed = ENEMY_SPEED
        self.damage = damage
        self.health = health
        self.health_run_away = health//2
        self.target = None

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
        x_diff = end_x - self.center_x
        y_diff = end_y - self.center_y
        if (abs(y_diff) < self.height) or (abs(x_diff) < self.width):
            return
        if self.action not in ['Die']:
            self.action = "Walk"
            self.center_x += self.change_x
            self.center_y += self.change_y
            if random.randrange(100) == 0:
                angle = math.atan2(y_diff, x_diff)
                self.change_x = math.cos(angle) * self.speed
                self.change_y = math.sin(angle) * self.speed

    def is_attacking(self, target):
        if self.action not in ['Attack', 'Die']:
            arcade.play_sound(self.attack_sound)
            self.texture_frame_count = 0
            self.texture_frame = 1
            self.action = "Attack"
            self.target = target
        if (self.texture_frame == len(self.attack_textures)):
            self.target.health -= self.damage
            self.target = None
            self.is_idle()

    def is_idle(self):
        self.texture_frame_count = 0
        self.texture_frame = 1
        if self.action not in ['Die']:
            self.action = "Idle"

    def is_die(self):
        self.action = "Die"
        if (self.texture_frame == len(self.die_textures)):
            arcade.play_sound(self.die_sound)
            self.remove_from_sprite_lists()

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

        if self.action == "Die":
            ind = self.texture_frame % (len(self.die_textures))
            self.texture = self.die_textures[ind]
