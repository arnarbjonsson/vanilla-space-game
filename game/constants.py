"""
Game constants and configuration settings
"""

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Vanilla Space Game"

# Game settings
FPS = 60
PLAYER_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 2

# Sprite scaling
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_BULLET = 0.5
SPRITE_SCALING_ENEMY = 0.5

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game mechanics
BULLET_DAMAGE = 1
ENEMY_HEALTH = 1
ENEMY_SPAWN_RATE = 1.5  # seconds between enemy spawns 