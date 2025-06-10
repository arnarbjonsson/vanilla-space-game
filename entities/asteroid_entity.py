"""
Asteroid Entity - handles stationary asteroids with ore resources
"""

import random
from entities.base_entity import BaseEntity


class AsteroidEntity(BaseEntity):
    """Stationary asteroid entity with ore resources"""
    
    def __init__(self, x, y):
        """Initialize the asteroid entity"""
        super().__init__(x, y)
        
        # Visual properties
        self.asteroid_type = random.randint(1, 6)  # Which asteroid asset to use (1-6)
        self.scale = random.uniform(0.15, 0.45)  # Random size variation (30% of original size)
        
        # Rotation properties (subtle rotation)
        self.rotation = random.uniform(0, 360)  # Start with random rotation
        # Random direction and speed between 3-5 degrees per second
        speed = random.uniform(3, 5)
        direction = random.choice([-1, 1])  # Either clockwise (-) or counter-clockwise (+)
        self.rotation_speed = speed * direction
        
        # Ore properties
        self.ore_type = random.choice(['iron', 'copper', 'gold', 'platinum'])
        self.ore_remaining = random.randint(3, 10)  # How much ore this asteroid contains
        
    def update(self, delta_time, input_commands=None):
        """Update asteroid logic (rotation and depletion check)"""
        if not self.active:
            return
        
        # Update rotation
        self.rotation += self.rotation_speed * delta_time
        self.rotation = self.rotation % 360  # Keep rotation between 0-360
        
        # Check if asteroid is depleted
        if self.ore_remaining <= 0:
            self.destroy()
            
    def mine_ore(self, amount=1):
        """Mine ore from this asteroid, returns the amount actually mined"""
        if not self.active or self.ore_remaining <= 0:
            return 0
            
        actual_mined = min(amount, self.ore_remaining)
        self.ore_remaining -= actual_mined
        
        # Destroy asteroid if depleted
        if self.ore_remaining <= 0:
            self.destroy()
            
        return actual_mined
        
    def get_collision_radius(self):
        """Get the collision radius based on asteroid type and scale"""
        # Base radius varies by asteroid type, scaled by the scale factor
        base_radii = {
            1: 40,  # asteroid1.png
            2: 35,  # asteroid2.png  
            3: 30,  # asteroid3.png
            4: 45,  # asteroid4.png
            5: 25,  # asteroid5.png
            6: 20   # asteroid6.png
        }
        
        base_radius = base_radii.get(self.asteroid_type, 30)
        return base_radius * self.scale
        
    def is_depleted(self):
        """Check if the asteroid has no ore remaining"""
        return self.ore_remaining <= 0 