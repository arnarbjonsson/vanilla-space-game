"""
Asteroid Entity - handles stationary asteroids with ore resources
"""

import random

import arcade

from entities.base_entity import BaseEntity
from game_state.inventory import Inventory
from game_state.inventory_types import InventoryType
from game_state.game_events import on_asteroid_mined

DEPLETED_SOUND = arcade.Sound("assets/audio/mining-blast.wav")

# Asteroid Constants - Easy to tune
ASTEROID_TYPES_COUNT = 6           # Number of different asteroid textures (1-6)
ASTEROID_MIN_SCALE = 0.3         # Minimum size scale factor
ASTEROID_MAX_SCALE = 0.6         # Maximum size scale factor
ASTEROID_MIN_ROTATION_SPEED = 3   # Minimum rotation speed (degrees/second)
ASTEROID_MAX_ROTATION_SPEED = 5   # Maximum rotation speed (degrees/second)
ASTEROID_MIN_ORE = 30             # Minimum ore amount per asteroid (10x)
ASTEROID_MAX_ORE = 100            # Maximum ore amount per asteroid (10x)

# Asteroid collision radii by type (base values before scaling)
ASTEROID_BASE_RADII = {
    1: 40,  # asteroid1.png
    2: 35,  # asteroid2.png  
    3: 30,  # asteroid3.png
    4: 45,  # asteroid4.png
    5: 25,  # asteroid5.png
    6: 20   # asteroid6.png
}

# Available ore types for asteroids
ASTEROID_ORE_TYPES = [
    InventoryType.VELDSPAR,
    InventoryType.SCORDITE,
    InventoryType.PYROXERES,
    InventoryType.PLAGIOCLASE,
    InventoryType.OMBER
]


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
        
        # Initialize ore
        self.ore_type = random.choice(ASTEROID_ORE_TYPES)
        
        # Calculate ore amount based on asteroid size
        # Scale factor is between 0.3 and 0.6, so we'll use it to scale the ore amount
        # This means smaller asteroids will have proportionally less ore
        size_factor = (self.scale - ASTEROID_MIN_SCALE) / (ASTEROID_MAX_SCALE - ASTEROID_MIN_SCALE)
        min_ore = int(ASTEROID_MIN_ORE * (0.5 + size_factor * 0.5))  # 50-100% of min ore
        max_ore = int(ASTEROID_MAX_ORE * (0.5 + size_factor * 0.5))  # 50-100% of max ore
        initial_ore = random.randint(min_ore, max_ore)
        
        # Create inventory with initial ore
        self.inventory = Inventory(max_units=initial_ore)
        self.inventory.add_item(self.ore_type, initial_ore)
        
    def update(self, delta_time, input_commands=None):
        """Update asteroid logic (rotation and depletion check)"""
        if not self.active:
            return
        
        # Update rotation
        self.rotation += self.rotation_speed * delta_time
        self.rotation = self.rotation % 360  # Keep rotation between 0-360
        
        # Check if asteroid is depleted
        if self.is_depleted():
            self.destroy()
            
    def mine_ore(self, amount, hit_type=None):
        """Mine ore from the asteroid"""
        if not self.inventory:
            return False

        success = self.inventory.remove_item(self.ore_type, amount)
        if success:
            # Emit the asteroid mined signal
            on_asteroid_mined.send(self, amount=amount, hit_type=hit_type)

        if self.is_depleted():
            DEPLETED_SOUND.play()
            
        return success
        
    def get_collision_radius(self):
        """Get the collision radius based on asteroid type and scale"""
        # Base radius varies by asteroid type, scaled by the scale factor
        base_radius = ASTEROID_BASE_RADII.get(self.asteroid_type, 30)
        return base_radius * self.scale
        
    def is_depleted(self):
        """Check if the asteroid has no ore remaining"""
        return self.inventory.get_item_quantity(self.ore_type) <= 0

    def on_items_removed(self, item_type, amount):
        print(f"Asteroid at ({self.x}, {self.y}) emitted on_items_removed signal for {item_type}")
        # Additional logic can be added here if needed 