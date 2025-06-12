"""
Player Entity - handles the player spaceship logic
"""

import math

import arcade

from entities.base_entity import BaseEntity
from input.commands import InputCommand
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game_state.inventory import Inventory

# Player Ship Constants - Easy to tune
PLAYER_ROTATION_SPEED = 100     # degrees per second
PLAYER_THRUST_POWER = 100       # pixels per second squared
PLAYER_MAX_VELOCITY = 80       # pixels per second
PLAYER_DRAG = 0.2              # drag coefficient (higher = more drag)
PLAYER_MAX_HEALTH = 100        # maximum health points
PLAYER_MAX_MODULES = 4         # maximum number of modules that can be equipped
PLAYER_INVENTORY_SIZE = 200    # maximum number of units the player can carry

# Module locator positions (relative to ship center)
MODULE_LOCATORS = [
    (-10, -40),   # Left side
    (-10, 40),    # Right side
    (30, -15),   # Bottom
    (30, 15),    # Top
]

INVENTORY_FULL_SOUND = arcade.load_sound("assets/audio/warning.wav")

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
        
        # Gameplay properties
        self.health = PLAYER_MAX_HEALTH
        self.max_health = PLAYER_MAX_HEALTH
        
        # Module system
        self.modules = []  # List of equipped modules
        self.max_modules = PLAYER_MAX_MODULES  # Maximum number of modules that can be equipped
        
        # Inventory system
        self.inventory = Inventory(max_units=PLAYER_INVENTORY_SIZE)
        self.inventory.on_items_added.connect(self.on_inventory_items_added)
        
        # Game state reference (for modules to access other entities)
        self.game_state = None

    def on_inventory_items_added(self, player_inventory, item_type, quantity):
        self.check_play_inventory_full_sound()

    def check_play_inventory_full_sound(self):
        if self.inventory.get_total_units() / self.inventory.max_units > 0.9:
            INVENTORY_FULL_SOUND.play()

    def update(self, delta_time, input_commands=None):
        """Update player logic based on input and physics"""
        if not self.active:
            return
            
        self._process_input(input_commands or [], delta_time)
        self._update_physics(delta_time)
        self._handle_screen_bounds()
        self._update_modules(delta_time)
        
    def _process_input(self, commands, delta_time):
        """Process input commands for player control"""
        # Reset thrust state
        self.is_thrusting = False
        
        for command in commands:
            if command == InputCommand.ROTATE_LEFT:
                self.rotation += PLAYER_ROTATION_SPEED * delta_time  # A key: turn left 
            elif command == InputCommand.ROTATE_RIGHT:
                self.rotation -= PLAYER_ROTATION_SPEED * delta_time  # D key: turn right
            elif command == InputCommand.THRUST:
                self._apply_thrust(delta_time)
                self.is_thrusting = True
                
        # Normalize rotation to 0-360 degrees
        self.rotation = self.rotation % 360
        
    def _apply_thrust(self, delta_time):
        """Apply thrust force in the direction the ship is facing"""
        # Convert rotation to radians (0 degrees = pointing up)
        angle_rad = math.radians(self.rotation)
        
        # Calculate thrust components (0° = up, 90° = right, etc.)
        thrust_x = math.cos(angle_rad) * PLAYER_THRUST_POWER * delta_time
        thrust_y = math.sin(angle_rad) * PLAYER_THRUST_POWER * delta_time
        
        # Add to velocity
        self.velocity_x += thrust_x
        self.velocity_y += thrust_y
        
        # Cap maximum velocity
        velocity_magnitude = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
        
        if velocity_magnitude > PLAYER_MAX_VELOCITY:
            scale = PLAYER_MAX_VELOCITY / velocity_magnitude
            self.velocity_x *= scale
            self.velocity_y *= scale
            
    def _update_physics(self, delta_time):
        """Update physics simulation"""
        # Apply velocity to position
        self.x += self.velocity_x * delta_time
        self.y += self.velocity_y * delta_time
        
        # Apply drag (frame-rate independent)
        # Higher drag values now mean more drag (more intuitive)
        drag_factor = max(0.0, 1.0 - PLAYER_DRAG * delta_time)
        self.velocity_x *= drag_factor
        self.velocity_y *= drag_factor
        
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

    def _update_modules(self, delta_time):
        """Update all equipped modules"""
        for module in self.modules:
            if module.active:
                module.update(delta_time)

    # Module management methods
    def equip_module(self, module):
        """
        Equip a module to the ship
        
        Args:
            module: BaseModule instance to equip
            
        Returns:
            bool: True if module was successfully equipped
        """
        if len(self.modules) >= PLAYER_MAX_MODULES:
            return False  # Ship is full
            
        if module in self.modules:
            return False  # Module already equipped
            
        self.modules.append(module)
        module.equip_to_ship(self)
        
        return True
    
    def unequip_module(self, module):
        """
        Unequip a module from the ship
        
        Args:
            module: BaseModule instance to unequip
            
        Returns:
            bool: True if module was successfully unequipped
        """
        if module not in self.modules:
            return False
            
        self.modules.remove(module)
        module.unequip_from_ship(self)
        return True
    
    def activate_module(self, module_index):
        """
        Activate a module by its index in the modules list
        
        Args:
            module_index: Index of the module to activate (0-based)
            
        Returns:
            bool: True if module was successfully activated
        """
        if module_index < 0 or module_index >= len(self.modules):
            return False
            
        module = self.modules[module_index]
        return module.activate(self)
    
    def get_module_by_index(self, index):
        """Get a module by its index, or None if invalid index"""
        if 0 <= index < len(self.modules):
            return self.modules[index]
        return None
    
    def get_equipped_modules(self):
        """Get list of all equipped modules"""
        return self.modules.copy()
    
    def has_module_slot_available(self):
        """Check if there's an available slot for a new module"""
        return len(self.modules) < PLAYER_MAX_MODULES
    
    # Target selection methods for modules
    def find_closest_asteroid(self, max_range=None):
        """
        Find the closest asteroid within range
        
        Args:
            max_range: Maximum distance to search (None for unlimited)
            
        Returns:
            AsteroidEntity or None: Closest asteroid or None if none in range
        """
        if not self.game_state:
            return None
        
        asteroids = self.game_state.get_asteroids()
        closest_asteroid = None
        closest_distance = float('inf')
        
        for asteroid in asteroids:
            if not asteroid.active or asteroid.is_depleted():
                continue
                
            # Calculate distance between ship and asteroid
            distance = self._calculate_distance_to(asteroid)
            
            # Check if asteroid is within range (if specified)
            if max_range is not None:
                # Account for asteroid collision radius
                effective_distance = distance - asteroid.get_collision_radius()
                if effective_distance > max_range:
                    continue
            
            if distance < closest_distance:
                closest_distance = distance
                closest_asteroid = asteroid
        
        return closest_asteroid
    
    def _calculate_distance_to(self, entity):
        """Calculate distance between this player and another entity"""
        dx = self.x - entity.x
        dy = self.y - entity.y
        return math.sqrt(dx * dx + dy * dy)

    def set_game_state(self, game_state):
        """Set reference to the game state for module access"""
        self.game_state = game_state 

    def get_module_position(self, module_index):
        """
        Get the world position of a module's locator
        
        Args:
            module_index: Index of the module (0-based)
            
        Returns:
            tuple: (x, y) world coordinates of the module locator
        """
        if module_index < 0 or module_index >= len(MODULE_LOCATORS):
            return (self.x, self.y)  # Default to ship center if invalid index
            
        # Get the locator offset
        locator_x, locator_y = MODULE_LOCATORS[module_index]
        
        # Convert rotation to radians
        angle_rad = math.radians(self.rotation)
        
        # Rotate the locator offset
        rotated_x = locator_x * math.cos(angle_rad) - locator_y * math.sin(angle_rad)
        rotated_y = locator_x * math.sin(angle_rad) + locator_y * math.cos(angle_rad)
        
        # Add to ship position
        return (self.x + rotated_x, self.y + rotated_y) 

    def _on_ore_mined(self, module, ore_type, amount, hit_type):
        """Handle ore being mined by adding it to player's inventory"""
        print(f"Player received mined ore signal: {amount} units of {ore_type}")
        if self.inventory:
            success = self.inventory.add_item(ore_type, amount)
            if success:
                print(f"Successfully added {amount} units of {ore_type} to inventory")
                print(f"Current inventory contents: {self.inventory.items}")
            else:
                self.check_play_inventory_full_sound()
                print(f"Failed to add {amount} units of {ore_type} to inventory - inventory full?")
        else:
            print("Player inventory not available.") 