import os

SCREEN_TITLE = "Slime Survival"

# ---Sizing & Scaling 
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900

TILE_PIXEL_SIZE = 32
TILE_SCALING = 1

PLAYER_PIXEL_SIZE = 16
PLAYER_SCALING = 2
GRID_PIXEL_SIZE = TILE_PIXEL_SIZE * TILE_SCALING

# --- Margin 
VIEWPORT_MARGIN_TOP = 60
VIEWPORT_MARGIN_BOTTOM = 60
VIEWPORT_RIGHT_MARGIN = 270
VIEWPORT_LEFT_MARGIN = 270

# --- Player
MOVEMENT_SPEED = 10

# --- Path 

MAP_PATH = "./slime_survival/tile_world/"
MAP = {
    "delta": os.path.join(MAP_PATH, "map_delta.json")
}

PLAYER_PATH = "./slime_survival/sprite/Player/"