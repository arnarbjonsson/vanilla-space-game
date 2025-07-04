"""
Asteroid Entity - handles stationary asteroids with ore resources
"""

import random

import arcade

from audio.audio_engine import AudioEngine
from audio.sound_bank import SoundBank
from entities.base_entity import BaseEntity
from game_state.inventory import Inventory
from game_state.inventory_types import InventoryType
from game_state.game_events import on_asteroid_mined

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
        
        # Mining state
        self.active_mining_module = None  # Reference to active mining module

        # Create inventory with initial ore
        self.inventory = Inventory(max_units=initial_ore)
        self.inventory.add_item(self.ore_type, initial_ore)
        
        # Cache the collision radius
        self._cached_radius = None
        
    def update(self, delta_time, input_commands=None):
        """Update asteroid logic (rotation and depletion check)"""
        if not self.active:
            return
        
        # Update rotation
        self.rotation += self.rotation_speed * delta_time
        self.rotation = self.rotation % 360  # Keep rotation between 0-360
        
        # Check if asteroid is depleted
        if self.is_depleted():
            AudioEngine.get_instance().play_sound(SoundBank.MINING_BLAST)
            self.destroy()
            
    def start_mining(self, mining_module):
        """Start mining this asteroid with the given module"""
        self.active_mining_module = mining_module
        
    def stop_mining(self):
        """Stop mining this asteroid"""
        self.active_mining_module = None
        
    def get_collision_radius(self):
        """Get the collision radius based on asteroid type and scale"""
        if self._cached_radius is None:
            # Load the texture to get the actual size
            texture_path = f"assets/asteroid{self.asteroid_type}.png"
            try:
                texture = arcade.load_texture(texture_path)
                # Use the texture's width and height to determine the radius
                radius = max(texture.width, texture.height) / 2
                self._cached_radius = radius * self.scale
            except FileNotFoundError:
                # Fallback to base radius if texture is not found
                base_radius = ASTEROID_BASE_RADII.get(self.asteroid_type, 30)
                self._cached_radius = base_radius * self.scale
        return self._cached_radius
        
    def is_depleted(self):
        """Check if the asteroid has no ore remaining"""
        return self.inventory.get_item_quantity(self.ore_type) <= 0
