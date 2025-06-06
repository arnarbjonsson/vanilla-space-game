"""
Player Entity - handles the player spaceship logic
"""

import math
from entities.base_entity import BaseEntity
from input.commands import InputCommand
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class PlayerEntity(BaseEntity):
    """Player spaceship entity with rotation and thrust physics"""
    
    def __init__(self, x, y):
        """Initialize the player entity"""
        super().__init__(x, y)
        
        # Physics properties
        self.rotation = 0  # degrees, 0 = pointing up
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_thrusting = False
        
        # Physics constants
        self.rotation_speed = 180  # degrees per second
        self.thrust_power = 300    # pixels per second squared
        self.max_velocity = 400    # pixels per second
        self.drag = 0.98          # velocity multiplier per frame (friction)
        
        # Gameplay properties
        self.health = 100
        self.max_health = 100
        
    def update(self, delta_time, input_commands=None):
        """Update player logic based on input and physics"""
        if not self.active:
            return
            
        self._process_input(input_commands or [], delta_time)
        self._update_physics(delta_time)
        self._handle_screen_bounds()
        
    def _process_input(self, commands, delta_time):
        """Process input commands for player control"""
        # Reset thrust state
        self.is_thrusting = False
        
        for command in commands:
            if command == InputCommand.ROTATE_LEFT:
                self.rotation += self.rotation_speed * delta_time  # A key: turn left 
            elif command == InputCommand.ROTATE_RIGHT:
                self.rotation -= self.rotation_speed * delta_time  # D key: turn right
            elif command == InputCommand.THRUST:
                self._apply_thrust(delta_time)
                self.is_thrusting = True
                
        # Normalize rotation to 0-360 degrees
        self.rotation = self.rotation % 360
        
    def _apply_thrust(self, delta_time):
        """Apply thrust force in the direction the ship is facing"""
        # Convert rotation to radians (0 degrees = pointing up)
        # Reverse the thrust direction to go forward instead of backward
        angle_rad = math.radians(self.rotation)
        
        # Calculate thrust components - reversed to go forward
        thrust_x = -math.sin(angle_rad) * self.thrust_power * delta_time
        thrust_y = math.cos(angle_rad) * self.thrust_power * delta_time  # Positive cos for up direction
        
        # Add to velocity
        self.velocity_x += thrust_x
        self.velocity_y += thrust_y
        
        # Cap maximum velocity
        velocity_magnitude = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
        
        if velocity_magnitude > self.max_velocity:
            scale = self.max_velocity / velocity_magnitude
            self.velocity_x *= scale
            self.velocity_y *= scale
            
    def _update_physics(self, delta_time):
        """Update physics simulation"""
        # Apply velocity to position
        self.x += self.velocity_x * delta_time
        self.y += self.velocity_y * delta_time
        
        # Apply drag
        self.velocity_x *= self.drag
        self.velocity_y *= self.drag
        
    def _handle_screen_bounds(self):
        """Handle player hitting screen boundaries with wrap-around"""
        # Wrap around horizontally
        if self.x < 0:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x = 0
            
        # Wrap around vertically
        if self.y < 0:
            self.y = SCREEN_HEIGHT
        elif self.y > SCREEN_HEIGHT:
            self.y = 0
            
    def take_damage(self, damage):
        """Handle player taking damage"""
        self.health -= damage
        if self.health <= 0:
            self.destroy()
            
    def heal(self, amount):
        """Heal the player"""
        self.health = min(self.health + amount, self.max_health)
        
    def get_health_percentage(self):
        """Get health as a percentage"""
        return self.health / self.max_health
        
    def destroy(self):
        """Mark entity as inactive"""
        self.active = False
        
    def is_active(self):
        """Check if entity is active"""
        return self.active
        
    # Properties for compatibility with old coordinate system
    @property
    def x(self):
        """Get x position for compatibility"""
        return self.center_x
        
    @x.setter
    def x(self, value):
        """Set x position for compatibility"""
        self.center_x = value
        
    @property
    def y(self):
        """Get y position for compatibility"""
        return self.center_y
        
    @y.setter
    def y(self, value):
        """Set y position for compatibility"""
        self.center_y = value
        
    @property
    def rotation(self):
        """Get rotation for compatibility"""
        return self.angle
        
    @rotation.setter
    def rotation(self, value):
        """Set rotation for compatibility"""
        self.angle = value 