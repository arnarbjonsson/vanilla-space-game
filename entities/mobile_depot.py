"""
Mobile Depot Entity - A stationary container in space that can store large amounts of items
"""
from audio.audio_engine import AudioEngine
from audio.sound_bank import SoundBank
from entities.base_entity import BaseEntity
from entities.player_entity import PlayerEntity
from game_state.inventory import Inventory
from game_state.inventory_types import ORE_MINERAL_RATES, ORE_TYPES

# Mobile Depot Constants
MOBILE_DEPOT_INVENTORY_SIZE = 1000  # Much larger than player inventory
MOBILE_DEPOT_COLLISION_RADIUS = 60  # Size of the depot for collision detection
MOBILE_DEPOT_TRANSFER_RANGE = 50   # Range at which items are automatically transferred

class MobileDepot(BaseEntity):
    """Stationary container entity that can store large amounts of items and convert ore to minerals"""
    
    def __init__(self, x, y, game_state):
        """Initialize the mobile depot entity
        
        Args:
            x: X coordinate
            y: Y coordinate
            game_state: Reference to the game state
        """
        super().__init__(x, y)
        
        # Create a large inventory
        self.inventory = Inventory(max_units=MOBILE_DEPOT_INVENTORY_SIZE)
        
        # Cache the collision radius
        self._cached_radius = None
        
        # Store game state reference
        self.game_state = game_state
        
    def update(self, delta_time, input_commands=None):
        """Update depot logic - check for player and transfer items"""
        if not self.active:
            return
            
        # Find player entity
        player = next((entity for entity in self.game_state.entities 
                      if isinstance(entity, PlayerEntity) and entity.active), None)
                      
        if player and self.is_in_transfer_range(player):
            if self.transfer_items_from(player):
                print(f"Items transferred to mobile depot at ({self.x}, {self.y})")
        
    def get_collision_radius(self):
        """Get the collision radius of the depot"""
        if self._cached_radius is None:
            self._cached_radius = MOBILE_DEPOT_COLLISION_RADIUS
        return self._cached_radius
        
    def is_in_transfer_range(self, other_entity) -> bool:
        """Check if another entity is within transfer range
        
        Args:
            other_entity: The entity to check distance from
            
        Returns:
            bool: True if the entity is within transfer range
        """
        dx = self.x - other_entity.x
        dy = self.y - other_entity.y
        distance = (dx * dx + dy * dy) ** 0.5
        return distance <= MOBILE_DEPOT_TRANSFER_RANGE
        
    def transfer_items_from(self, other_entity) -> bool:
        """Transfer all items from another entity's inventory to this depot,
        converting ore to minerals in the process
        
        Args:
            other_entity: The entity to transfer items from
            
        Returns:
            bool: True if any items were transferred
        """
        if not other_entity.inventory:
            return False
            
        items_transferred = False
        for item_type, quantity in other_entity.inventory.get_all_items().items():
            # Remove items from the other entity first
            other_entity.inventory.remove_item(item_type, quantity)
            
            # Check if this is ore that should be converted to minerals
            if item_type in ORE_TYPES and item_type in ORE_MINERAL_RATES:
                # Convert ore to minerals
                conversion_rates = ORE_MINERAL_RATES[item_type]
                for mineral_type, conversion_rate in conversion_rates.items():
                    mineral_quantity = int(quantity * conversion_rate)
                    if mineral_quantity > 0:
                        self.inventory.add_item(mineral_type, mineral_quantity)
                print(f"Converted {quantity} {item_type.name} to minerals")
            else:
                # Add non-ore items directly
                self.inventory.add_item(item_type, quantity)
            
            items_transferred = True

        if items_transferred:
            AudioEngine.get_instance().play_sound(SoundBank.MINERAL_PICKUP)

        return items_transferred 