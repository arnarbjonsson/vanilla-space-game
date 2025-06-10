"""
Player Renderer - handles rendering of player entities
"""

import arcade
import math
from rendering.base_renderer import BaseRenderer, CoordinateTransform
from core.constants import *

TEXTURE_SCALE = 0.5

class PlayerRenderer(BaseRenderer):
    """Handles rendering of player entities"""
    
    def __init__(self):
        """Initialize the player renderer"""
        self.spaceship_texture = None
        self._load_textures()
    
    def _load_textures(self):
        """Load the spaceship texture"""
        try:
            self.spaceship_texture = arcade.load_texture("assets/spaceship.png")
        except FileNotFoundError:
            print("Warning: Could not load assets/spaceship.png")
            self.spaceship_texture = None
    
    def render_local(self, entity, transform):
        """Render the player entity in local coordinates (0,0 with 0 rotation)"""
        # Draw ship texture at world position
        self._draw_ship_texture(entity)
        
        # Draw thrust flame if thrusting (still using local coordinates)
        if entity.is_thrusting:
            self._draw_thrust_flame_local(transform)
    
    def _draw_ship_texture(self, entity):
        """Draw the spaceship texture at the entity's world position"""
        if self.spaceship_texture:
            # Draw the texture at the entity's world position with its rotation
            # Add 90 degrees to correct the texture orientation (90° clockwise)
            arcade.draw_texture_rect(
                self.spaceship_texture,
                arcade.XYWH(entity.x, entity.y, 
                           self.spaceship_texture.width * TEXTURE_SCALE, 
                           self.spaceship_texture.height * TEXTURE_SCALE),
                angle=90 -entity.rotation,
            )
        else:
            # Fallback: draw the original triangle if texture fails to load
            self._draw_ship_local_fallback(entity)
    
    def _draw_ship_local_fallback(self, entity):
        """Fallback triangle drawing if texture is not available"""
        # Create transform for fallback triangle
        transform = CoordinateTransform(entity.x, entity.y, entity.rotation)
        
        size = 30
        
        # Ship triangle in local space - always pointing up
        local_points = [
            (0, size),          # nose (top)
            (-size//2, -size//2),   # bottom left
            (size//2, -size//2)     # bottom right
        ]
        
        # Transform all points to world coordinates
        world_points = []
        for local_x, local_y in local_points:
            world_x, world_y = transform.to_world(local_x, local_y)
            world_points.extend([world_x, world_y])
        
        # Draw the triangle
        arcade.draw_triangle_filled(
            world_points[0], world_points[1],  # nose
            world_points[2], world_points[3],  # bottom left  
            world_points[4], world_points[5],  # bottom right
            BLUE
        )
            
    def _draw_thrust_flame_local(self, transform):
        """Draw thrust flame in local coordinates"""
        # In local space, ship points up (0, positive Y)
        # So flame goes down (0, negative Y) from the back of the ship
        flame_start_local = (0, -15)  # Back of ship
        flame_end_local = (0, -60)    # Flame extends down
        
        # Transform to world coordinates
        flame_start_x, flame_start_y = transform.to_world(*flame_start_local)
        flame_end_x, flame_end_y = transform.to_world(*flame_end_local)
        
        # Draw flame line
        arcade.draw_line(flame_start_x, flame_start_y, flame_end_x, flame_end_y, YELLOW, 6)
        
        # Debug circle at flame start
        arcade.draw_circle_filled(flame_start_x, flame_start_y, 3, RED) 