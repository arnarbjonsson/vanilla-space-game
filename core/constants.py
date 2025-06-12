"""
Core constants and configuration settings
"""

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1200
SCREEN_TITLE = "Vanilla Space Game"

# Game settings
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Asteroid colors by type
ASTEROID_COLORS = {
    1: (128, 128, 128),  # Gray
    2: (184, 115, 51),   # Brown
    3: (255, 215, 0),    # Gold
    4: (229, 228, 226),  # Silver
    5: (139, 69, 19),    # Dark Brown
    6: (169, 169, 169)   # Dark Gray
}
