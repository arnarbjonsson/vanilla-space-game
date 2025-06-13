"""
Asteroid Renderer - handles rendering of asteroid entities
"""

import arcade


from rendering.base_renderer import BaseRenderer
from game_state.inventory_types import ORE_NAMES

# Mined item effect constants
ITEM_POPUP_LIFETIME = 60  # Frames
ITEM_POPUP_SPEED = 2
ITEM_POPUP_SIZE = 32  # Size of the item icon
ITEM_POPUP_FADE_START = 45  # When to start fading out

class AsteroidRenderer(BaseRenderer):
    """Handles rendering of asteroid entities with different textures"""
    
    # Mining gauge constants
    GAUGE_THICKNESS = 8
    GAUGE_COLOR = (255, 255, 255, 100)  # Semi-transparent white
    GAUGE_BG_COLOR = (255, 255, 255, 25)  # Very transparent white
    GAUGE_OFFSET = 30
    TEXT_COLOR = arcade.color.Color(255, 255, 255, 128)
    
    def __init__(self, asteroid_entity):
        """Initialize the asteroid renderer and load all asteroid textures"""
        self.asteroid_textures = {}
        self._load_textures()
        self.active_effects = []
        self.item_textures = {}  # Cache for loaded item textures
        
        # Connect to asteroid's inventory signals

    def _load_textures(self):
        """Load all asteroid textures"""
        for i in range(1, 7):  # asteroid1.png through asteroid6.png
            try:
                texture = arcade.load_texture(f"assets/asteroid{i}.png")
                self.asteroid_textures[i] = texture
            except FileNotFoundError:
                print(f"Warning: Could not load assets/asteroid{i}.png")
                self.asteroid_textures[i] = None
    
    def render_local(self, asteroid, transform):
        """Render an asteroid entity in local coordinates"""
        if not asteroid.active:
            return
            
        # Try to render with texture first
        texture = self.asteroid_textures.get(asteroid.asteroid_type)
        # Calculate the actual size based on the texture size and scale
        actual_width = texture.width * asteroid.scale
        actual_height = texture.height * asteroid.scale

        # Draw the texture at the entity's world position with subtle rotation
        arcade.draw_texture_rect(
            texture,
            arcade.XYWH(asteroid.x, asteroid.y, actual_width, actual_height),
            angle=asteroid.rotation
        )

        # Draw mining gauge if asteroid is being mined
        if asteroid.active_mining_module:
            self._draw_mining_gauge(asteroid)
        
        # Draw ore type label
        self._draw_ore_label(asteroid, asteroid.get_collision_radius())
    
    def _draw_mining_gauge(self, asteroid):
        """Draw the mining cycle gauge around the asteroid"""
        # Calculate gauge radius (slightly larger than asteroid)
        asteroid_radius = asteroid.get_collision_radius()
        # gauge_radius = asteroid_radius + self.GAUGE_OFFSET
        gauge_radius = 50
        
        # Draw background circle
        arcade.draw_arc_outline(
            asteroid.x,
            asteroid.y,
            gauge_radius * 2,
            gauge_radius * 2,
            self.GAUGE_BG_COLOR,
            0,
            360,
            self.GAUGE_THICKNESS
        )
        
        # Get progress from the mining module if available, otherwise use asteroid's progress
        progress = asteroid.active_mining_module.get_cycle_progress()
        angle = 360 * progress

        # Draw progress arc1
        arcade.draw_arc_outline(
            asteroid.x,
            asteroid.y,
            gauge_radius * 2,
            gauge_radius * 2,
            self.GAUGE_COLOR,
            0,  # Start from top
            angle,  # End based on progress
            self.GAUGE_THICKNESS
        )
        
    def _draw_ore_label(self, asteroid, radius):
        """Draw the ore type label above the asteroid, only if inventory is not full"""
        # Only show label if asteroid has been mined at least once (inventory not full)
        if asteroid.inventory.get_item_quantity(asteroid.ore_type) == asteroid.inventory.max_units:
            return
        # Get ore name
        ore_name = ORE_NAMES.get(asteroid.ore_type, asteroid.ore_type.name)
        # Draw ore name
        arcade.draw_text(
            ore_name,
            asteroid.x,
            asteroid.y + radius + 10,
            self.TEXT_COLOR,  # Semi-transparent white
            12,
            anchor_x="center",
            font_name="EveSansNeue-Regular",
        )
