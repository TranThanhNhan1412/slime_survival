import os
import arcade

SCREEN_TITLE = "Slime Survival"

# ---Sizing & Scaling
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900

TILE_PIXEL_SIZE = 32
TILE_SCALING = 2

PLAYER_PIXEL_SIZE = 16
PLAYER_SCALING = 2
GRID_PIXEL_SIZE = TILE_PIXEL_SIZE * TILE_SCALING

# --- Margin
VIEWPORT_MARGIN_TOP = 60
VIEWPORT_MARGIN_BOTTOM = 60
VIEWPORT_RIGHT_MARGIN = 270
VIEWPORT_LEFT_MARGIN = 270

# --- Player
PLAYER_SPEED = 10
PLAYER_FPS = {
    "Idle": 30,
    "Walk": 15,
    "Attack": 15,
}


# ----- Enemy
ENEMY_FPS = 15
ENEMY_SPEED = 1
ENEMY_VIEW_PADDING = 5 * TILE_PIXEL_SIZE
ENEMY_DAME = 5
# --- Path

MAP_PATH = "./slime_survival/tile_world/"
MAP = {
    "delta": os.path.join(MAP_PATH, "map_delta.json")
}

SPRITE_PATH = "./slime_survival/sprite/"

SOUND_PATH = "./slime_survival/sound/"


# common function
def get_texture_files(name_folder):
    # Load textures for walking
    textures = []
    full_path = os.path.join(SPRITE_PATH, name_folder)+"/"
    if os.path.exists(full_path):
        all_file = os.listdir(full_path)
        for f in all_file:
            textures.append(arcade.load_texture(os.path.join(full_path, f)))
    return textures
