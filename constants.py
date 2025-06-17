GAME_STATE_START = 0
GAME_STATE_PLAYING = 1
GAME_STATE_GAME_OVER = 2

GRID_SIZE = 7
TILE_SIZE = 60
PADDING = 5
SCREEN_WIDTH = GRID_SIZE * (TILE_SIZE + PADDING) - PADDING
SCREEN_HEIGHT = GRID_SIZE * (TILE_SIZE + PADDING) + 100
GAME_BOARD_OFFSET_Y = 100

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)
LIGHT_GRAY = (200, 200, 200)
MUTED_BLUE = (173, 216, 230)
BORDER_COLOR = (100, 100, 100)
SELECTED_COLOR = (100, 149, 237)
SCORE_TEXT_COLOR = BLACK
TIME_TEXT_COLOR = BLACK

MODE_TIME = "Time"
MODE_MOVES = "Moves"
DEFAULT_TIME = 30
DEFAULT_MOVES = 15
BONUS_TIME_PER_MATCH = 2
BONUS_MOVES_PER_MATCH = 0

POINTS_PER_TILE = 10
POINTS_PER_SPECIAL_ACTIVATION = 50 # Bonus points for using a special tile

ANIM_SWAP_SPEED = 25
ANIM_REMOVAL_SPEED = 30
ANIM_DROP_SPEED = 70
ANIM_SHAKE_SPEED = 25

THEMES = {
    "Classic": ['visual/cone', 'visual/cross', 'visual/cube', 'visual/cylinder', 'visual/geometry'],
    "Pirates": ['visual/parrot', 'visual/pirates', 'visual/compass', 'visual/ship-wheel', 'visual/hook'],
    "Winter": ['visual/bonfire', 'visual/candy-cane', 'visual/cookie', 'visual/deer', 'visual/snow-globe'],
    "Summer": ['visual/starfish', 'visual/pamela-hat', 'visual/help', 'visual/coconut-drink', 'visual/watermelon'],
    "History": ['visual/mammoth', 'visual/moai', 'visual/fossil', 'visual/pharaoh', 'visual/mask'],
    "Heroes": ['visual/helmet', 'visual/eye-mask', 'visual/hammer', 'visual/nuclear', 'visual/regeneration'],
    "Haloween": ['visual/voodoo-doll', 'visual/cauldron', 'visual/pumpkin', 'visual/frankenstein', 'visual/decapitate']
}

# New special tile types
SPECIAL_H_LINE_TILE = "special/h_line"
SPECIAL_V_LINE_TILE = "special/v_line"
SPECIAL_BOMB_TILE = "special/bomb"
SPECIAL_COLOR_BOMB_TILE = "special/color_bomb"

# Map special tile types to their image paths
SPECIAL_TILE_IMAGES = {
    SPECIAL_H_LINE_TILE: "visual/line_h",
    SPECIAL_V_LINE_TILE: "visual/line_v",
    SPECIAL_BOMB_TILE: "visual/bomb",
    SPECIAL_COLOR_BOMB_TILE: "visual/color_bomb"
}

ALL_SPECIAL_TILE_TYPES = list(SPECIAL_TILE_IMAGES.keys())

HIGH_SCORE_FILE = "high_score.txt"

SOUNDS = {
    "match": "sounds/match.wav",
    "swap": "sounds/swap.wav",
    "invalid_swap": "sounds/invalid_swap.wav",
    "drop": "sounds/drop.wav",
    "game_over": "sounds/game_over.wav",
    "music": "sounds/background_music.mp3",
    "special_activate": "sounds/special_activate.wav" # New sound for special tile activation
}