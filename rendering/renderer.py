"""
Renderer - handles all visual rendering using entity-specific renderers
"""

import arcade
from core.constants import *
from entities.player_entity import PlayerEntity
from rendering.player_renderer import PlayerRenderer
from ui.ui_renderer import UIRenderer


class Renderer:
    """Handles all visual rendering of the game using entity renderers"""
    
    def __init__(self):
        """Initialize the renderer with entity-specific renderers"""
        self.player_renderer = PlayerRenderer()
        self.ui_renderer = UIRenderer()
        
    def initialize(self):
        """Initialize renderer resources"""
        # Set up any textures, fonts, or other rendering resources here
        pass
        
    def render(self, game_state):
        """Render the current game state"""
        self._render_entities(game_state.entities)
        self.ui_renderer.render(game_state)
            
    def _render_entities(self, entities):
        """Render all entities using their specific renderers"""
        for entity in entities:
            if isinstance(entity, PlayerEntity):
                self.player_renderer.render(entity)
            # Add other entity types here as needed
        
    def _render_thrust_flames(self, player):
        """Render thrust flames for the player ship"""
        if not player or not player.is_thrusting:
            return
            
        # Draw simple thrust flame
        # Calculate flame position behind the ship
        import math
        
        # Get ship's rear position (opposite to thrust direction) 
        angle_rad = math.radians(player.angle)
        
        # Distance from ship center to rear edge
        rear_distance = 20
        
        # Rear position (opposite of thrust direction)
        rear_x = player.center_x - math.cos(angle_rad) * rear_distance
        rear_y = player.center_y - math.sin(angle_rad) * rear_distance
        
        # Flame length and width
        flame_length = 45  # Tripled from 15
        flame_width = 9    # Tripled from 3
        
        # Calculate flame end position
        flame_end_x = rear_x - math.cos(angle_rad) * flame_length
        flame_end_y = rear_y - math.sin(angle_rad) * flame_length
        
        # Draw flame as a thick line from ship rear to flame end
        arcade.draw_line(rear_x, rear_y, flame_end_x, flame_end_y, 
                        arcade.color.ORANGE, flame_width) 