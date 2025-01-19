#Game settings
WIDTH,HEIGHT = 900,900
FPS = 20
GRID_SIZE = 30
GRID_SIZE_WIDTH = GRID_SIZE/WIDTH
GRID_SIZE_HEIGHT = GRID_SIZE/HEIGHT
MAX_EQUIPPED_TOWERS = 5
START_MARBIES = 250
CASTLE_MAX_HEALTH = 40
MAX_TOWERS = 15

#Game global variables
grid = []
level = 1
sprites = []
buttons = []
towers = []
equippedTowers = []
enemies = []
enemiesOnMap = []
placedTowers = []
marbies = START_MARBIES
gold = 0
game_state = "menu"
hotbar_opened = False
selected_tower = None
wave = 0
spawnCenterX = 0
spawnCenterY = 0
castle_health = CASTLE_MAX_HEALTH
grass_color = (0,0,0)
way_color = (0,0,0)

#Directories
ASSETS_DIR = rf"assets"
IMAGES_DIR = rf"assets\images"
LEVELS_DIR = rf"assets\levels"
SAVES_DIR = rf"assets\saves"

#Colors
MENU_BG_COLOR = (59, 64, 130)
GAME_BG_COLOR = (93,161,48)
PLAY_BUTTON_COLOR = (180,0,0)
WAY_COLOR = (133,122,100)
CASTLE_COLOR = (181,191,187)
HOTBAR_COLOR = (76,76,76)
WHITE = (255,255,255)