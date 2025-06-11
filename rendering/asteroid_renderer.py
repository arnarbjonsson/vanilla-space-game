"""
Asteroid Renderer - handles rendering of asteroid entities
"""

import arcade
from rendering.base_renderer import BaseRenderer
from core.constants import *
from game_state.inventory_types import INVENTORY_ICONS

# Mined item effect constants
ITEM_POPUP_LIFETIME = 60  # Frames
ITEM_POPUP_SPEED = 2
ITEM_POPUP_SIZE = 32  # Size of the item icon
ITEM_POPUP_FADE_START = 45  # When to start fading out

class AsteroidRenderer(BaseRenderer):
    """Handles rendering of asteroid entities with different textures"""
    
    def __init__(self, asteroid_entity):
        """Initialize the asteroid renderer and load all asteroid textures"""
        self.asteroid_textures = {}
        self._load_textures()
        self.active_effects = []
        self.item_textures = {}  # Cache for loaded item textures
        
        # Connect to asteroid's inventory signals
        print(f"Created renderer for asteroid at ({asteroid_entity.x}, {asteroid_entity.y})")
    
    def _load_textures(self):
        """Load all asteroid textures"""
        for i in range(1, 7):  # asteroid1.png through asteroid6.png
            try:
                texture = arcade.load_texture(f"assets/asteroid{i}.png")
                self.asteroid_textures[i] = texture
                print(f"Loaded asteroid{i}.png")
            except FileNotFoundError:
                print(f"Warning: Could not load assets/asteroid{i}.png")
                self.asteroid_textures[i] = None
    
    def render(self, entity):
        """Render the asteroid entity directly (no coordinate transform needed)"""
        self._draw_asteroid_texture(entity)

    def render_local(self, entity, transform):
        """Render the asteroid entity - using world coordinates for simplicity"""
        self._draw_asteroid_texture(entity)

    def _draw_asteroid_texture(self, entity):
        """Draw the asteroid texture at the entity's world position"""
        # Get the appropriate texture for this asteroid
        texture = self.asteroid_textures.get(entity.asteroid_type)
        
        if texture:
            # Calculate the actual size based on the texture size and scale
            actual_width = texture.width * entity.scale
            actual_height = texture.height * entity.scale
            
            # Draw the texture at the entity's world position with subtle rotation
            arcade.draw_texture_rect(
                texture,
                arcade.XYWH(entity.x, entity.y, actual_width, actual_height),
                angle=entity.rotation
            )
        else:
            # Fallback: draw a simple circle if texture fails to load
            self._draw_asteroid_fallback(entity)
    
    def _draw_asteroid_fallback(self, entity):
        """Fallback circle drawing if texture is not available"""
        radius = entity.get_collision_radius()
        
        # Draw a colored circle based on ore type
        ore_colors = {
            'iron': (128, 128, 128),      # Gray
            'copper': (184, 115, 51),     # Brown
            'gold': (255, 215, 0),        # Gold
            'platinum': (229, 228, 226)   # Silver
        }
        
        color = ore_colors.get(entity.ore_type, WHITE)
        
        arcade.draw_circle_filled(entity.x, entity.y, radius, color)
        
        # Draw a simple outline
        arcade.draw_circle_outline(entity.x, entity.y, radius, WHITE, 2)
        
        # Draw ore remaining indicator (small text)
        arcade.draw_text(
            str(entity.ore_remaining),
            entity.x - 5, entity.y - 5,
            WHITE, 12
        )
