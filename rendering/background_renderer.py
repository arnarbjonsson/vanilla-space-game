"""
Background Renderer - handles background image rendering
"""

import arcade
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class BackgroundRenderer:
    """Handles rendering of the game background"""
    
    def __init__(self):
        """Initialize the background renderer"""
        self.background_texture = None
        
    def initialize(self):
        """Initialize background renderer resources"""
        # Load background texture
        try:
            self.background_texture = arcade.load_texture("assets/background.png")
        except FileNotFoundError:
            print("Warning: Background texture not found at assets/background.png")
            self.background_texture = None
    
    def render(self):
        """Render the background image"""
        if self.background_texture:
            # Draw the background texture to fill the entire screen
            from arcade import XYWH
            arcade.draw_texture_rect(
                self.background_texture,
                XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT)
            ) 