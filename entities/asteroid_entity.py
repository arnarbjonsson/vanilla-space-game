"""
Asteroid Entity - handles stationary asteroids with ore resources
"""

import random
from entities.base_entity import BaseEntity

# Asteroid Constants - Easy to tune
ASTEROID_TYPES_COUNT = 6           # Number of different asteroid textures (1-6)
ASTEROID_MIN_SCALE = 0.3         # Minimum size scale factor
ASTEROID_MAX_SCALE = 0.6         # Maximum size scale factor
ASTEROID_MIN_ROTATION_SPEED = 3   # Minimum rotation speed (degrees/second)
ASTEROID_MAX_ROTATION_SPEED = 5   # Maximum rotation speed (degrees/second)
ASTEROID_MIN_ORE = 3              # Minimum ore amount per asteroid
ASTEROID_MAX_ORE = 10             # Maximum ore amount per asteroid

# Asteroid collision radii by type (base values before scaling)
ASTEROID_BASE_RADII = {
    1: 40,  # asteroid1.png
    2: 35,  # asteroid2.png  
    3: 30,  # asteroid3.png
    4: 45,  # asteroid4.png
    5: 25,  # asteroid5.png
    6: 20   # asteroid6.png
}

ORE_TYPES = ['iron', 'copper', 'gold', 'platinum']


class AsteroidEntity(BaseEntity):
    """Stationary asteroid entity with ore resources"""
    
    def __init__(self, x, y):
        """Initialize the asteroid entity"""
        super().__init__(x, y)
        
        # Visual properties
        self.asteroid_type = random.randint(1, ASTEROID_TYPES_COUNT)  # Which asteroid asset to use
        self.scale = random.uniform(ASTEROID_MIN_SCALE, ASTEROID_MAX_SCALE)  # Random size variation
        
        # Rotation properties (subtle rotation)
        self.rotation = random.uniform(0, 360)  # Start with random rotation
        # Random direction and speed
        speed = random.uniform(ASTEROID_MIN_ROTATION_SPEED, ASTEROID_MAX_ROTATION_SPEED)
        direction = random.choice([-1, 1])  # Either clockwise (-) or counter-clockwise (+)
        self.rotation_speed = speed * direction
        
        # Ore properties
        self.ore_type = random.choice(ORE_TYPES)
        self.ore_remaining = random.randint(ASTEROID_MIN_ORE, ASTEROID_MAX_ORE)  # How much ore this asteroid contains
        
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
        base_radius = ASTEROID_BASE_RADII.get(self.asteroid_type, 30)
        return base_radius * self.scale
        
    def is_depleted(self):
        """Check if the asteroid has no ore remaining"""
        return self.ore_remaining <= 0 