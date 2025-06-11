"""
Effects Renderer - handles visual effects between entities
"""

import arcade
from core.constants import *

# Laser beam visual effect constants
LASER_BEAM_COLOR = (255, 140, 0)  # Bright orange RGB
LASER_BEAM_THICKNESS = 4
LASER_GLOW_COLOR = (255, 140, 0, 100)  # Orange with transparency
LASER_GLOW_THICKNESS_OFFSET = 2  # Additional thickness for glow effect

class EffectsRenderer:
    """Handles rendering of visual effects between entities"""
    
    def __init__(self):
        """Initialize the effects renderer"""
        pass
    
    def render_effects(self, game_state):
        """Render all active effects in the game based on game state"""
        if not game_state.player_entity:
            return
        
        # Render mining laser effects by observing module states
        self._render_mining_laser_effects(game_state.player_entity)
    
    def _render_mining_laser_effects(self, player_entity):
        """Render mining laser beam effects from player to target asteroids"""
        # Check if player has modules
        if not player_entity.modules:
            return
        
        # Import here to avoid circular imports
        from entities.mining_laser_module import MiningLaserModule
        
        # Find active mining laser modules and render their effects
        for module in player_entity.modules:
            # Check if it's a mining laser module that is active with a target
            if (isinstance(module, MiningLaserModule) and 
                module.state == "active" and 
                module.current_target is not None):
                self._draw_laser_beam(player_entity, module.current_target)
    
    def _draw_laser_beam(self, source_entity, target_entity):
        """Draw a laser beam between two entities"""
        # Draw the main beam
        arcade.draw_line(
            source_entity.x, source_entity.y,
            target_entity.x, target_entity.y,
            LASER_BEAM_COLOR,
            LASER_BEAM_THICKNESS
        )
        
        # Add a subtle glow effect with a thicker, more transparent line
        arcade.draw_line(
            source_entity.x, source_entity.y,
            target_entity.x, target_entity.y,
            LASER_GLOW_COLOR,
            LASER_BEAM_THICKNESS + LASER_GLOW_THICKNESS_OFFSET
        ) 