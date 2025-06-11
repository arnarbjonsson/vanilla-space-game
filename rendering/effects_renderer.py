"""
Effects Renderer - handles visual effects between entities
"""

import arcade
import random
import math
from core.constants import *

# Laser beam visual effect constants
LASER_BEAM_COLOR = (255, 140, 0)  # Bright orange RGB
LASER_BEAM_THICKNESS = 4
LASER_GLOW_COLOR = (255, 140, 0, 100)  # Orange with transparency
LASER_GLOW_THICKNESS_OFFSET = 2  # Additional thickness for glow effect
LASER_CORE_COLOR = (255, 255, 255)  # White core
LASER_CORE_THICKNESS = 2

# Particle effect constants
PARTICLE_COUNT = 15
PARTICLE_COLOR = (255, 200, 100)  # Light orange
PARTICLE_SIZE = 2
PARTICLE_SPEED = 2
PARTICLE_LIFETIME = 30  # Frames
PARTICLE_ATTRACTION_FORCE = 0.4  # How strongly particles are attracted to the beam
PARTICLE_INITIAL_OFFSET = 6  # How far particles start from the beam
PARTICLE_RANDOM_FORCE = 0.1  # Random movement factor

class MiningLaserRenderer:
    """Handles rendering of mining laser effects"""
    
    def __init__(self):
        """Initialize the mining laser renderer"""
        self.active_particles = []

    def update(self):
        """Update particle states"""
        self._update_particles()
    
    def render(self, player_entity):
        """Render mining laser effects for the player entity"""
        if not player_entity.modules:
            return
            
        # Import here to avoid circular imports
        from entities.mining_laser_module import MiningLaserModule
        
        # Find active mining laser modules and render their effects
        for i, module in enumerate(player_entity.modules):
            if (isinstance(module, MiningLaserModule) and 
                module.state == "active" and 
                module.current_target is not None):
                # Get module position from the ship
                module_x, module_y = player_entity.get_module_position(i)
                self._draw_laser_beam(module_x, module_y, module.current_target)
                self._generate_particles(module_x, module_y, module.current_target)
    
    def _update_particles(self):
        """Update and remove expired particles"""
        # Update particle positions and lifetimes
        for particle in self.active_particles[:]:
            particle['lifetime'] -= 1
            if particle['lifetime'] <= 0:
                self.active_particles.remove(particle)
                continue
            
            # Calculate distance to beam
            dx = particle['beam_dx']
            dy = particle['beam_dy']
            perp_dx = -dy
            perp_dy = dx
            
            # Calculate perpendicular distance to beam
            dist_to_beam = (particle['x'] - particle['beam_x']) * perp_dx + (particle['y'] - particle['beam_y']) * perp_dy
            
            # Calculate attraction force towards beam
            attraction_x = perp_dx * -dist_to_beam * PARTICLE_ATTRACTION_FORCE
            attraction_y = perp_dy * -dist_to_beam * PARTICLE_ATTRACTION_FORCE
            
            # Add some random movement
            random_x = random.uniform(-PARTICLE_RANDOM_FORCE, PARTICLE_RANDOM_FORCE)
            random_y = random.uniform(-PARTICLE_RANDOM_FORCE, PARTICLE_RANDOM_FORCE)
            
            # Update velocity
            particle['dx'] += attraction_x + random_x
            particle['dy'] += attraction_y + random_y
            
            # Move particle
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
    
    def _generate_particles(self, source_x, source_y, target_entity):
        """Generate particles along the laser beam"""
        # Calculate direction vector from target to source
        dx = source_x - target_entity.x
        dy = source_y - target_entity.y
        length = math.sqrt(dx * dx + dy * dy)
        
        # Normalize direction
        if length > 0:
            dx /= length
            dy /= length
        
        # Generate new particles
        for _ in range(PARTICLE_COUNT):
            # Random position along the beam
            t = random.random()
            beam_x = target_entity.x + dx * length * t
            beam_y = target_entity.y + dy * length * t
            
            # Add some random offset perpendicular to the beam
            perp_dx = -dy
            perp_dy = dx
            offset = random.uniform(-PARTICLE_INITIAL_OFFSET, PARTICLE_INITIAL_OFFSET)
            x = beam_x + perp_dx * offset
            y = beam_y + perp_dy * offset
            
            # Initial velocity towards the beam
            initial_dx = -perp_dx * PARTICLE_ATTRACTION_FORCE
            initial_dy = -perp_dy * PARTICLE_ATTRACTION_FORCE
            
            self.active_particles.append({
                'x': x,
                'y': y,
                'dx': initial_dx,
                'dy': initial_dy,
                'lifetime': PARTICLE_LIFETIME,
                'beam_x': beam_x,
                'beam_y': beam_y,
                'beam_dx': dx,
                'beam_dy': dy
            })
    
    def _draw_laser_beam(self, source_x, source_y, target_entity):
        """Draw a laser beam between two points"""
        # Draw the outer glow effect
        arcade.draw_line(
            source_x, source_y,
            target_entity.x, target_entity.y,
            LASER_GLOW_COLOR,
            LASER_BEAM_THICKNESS + LASER_GLOW_THICKNESS_OFFSET
        )
        
        # Draw the main beam
        arcade.draw_line(
            source_x, source_y,
            target_entity.x, target_entity.y,
            LASER_BEAM_COLOR,
            LASER_BEAM_THICKNESS
        )
        
        # Draw the white core
        arcade.draw_line(
            source_x, source_y,
            target_entity.x, target_entity.y,
            LASER_CORE_COLOR,
            LASER_CORE_THICKNESS
        )
        
        # Draw particles
        for particle in self.active_particles:
            alpha = int((particle['lifetime'] / PARTICLE_LIFETIME) * 255)
            color = (*PARTICLE_COLOR, alpha)
            arcade.draw_circle_filled(
                particle['x'],
                particle['y'],
                PARTICLE_SIZE,
                color
            )


class EffectsRenderer:
    """Handles rendering of visual effects between entities"""
    
    def __init__(self):
        """Initialize the effects renderer"""
        self.mining_laser_renderer = MiningLaserRenderer()
    
    def render_effects(self, game_state):
        """Render all active effects in the game based on game state"""
        if not game_state.player_entity:
            return
        
        # Update and render mining laser effects
        self.mining_laser_renderer.update()
        self.mining_laser_renderer.render(game_state.player_entity) 