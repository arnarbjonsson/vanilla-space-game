"""
Inventory System - handles item storage and transfer between entities
"""

from typing import Dict, Optional, Tuple
from blinker import Signal
from .inventory_types import InventoryType

class Inventory:
    """Represents an inventory location that can store items"""
    
    def __init__(self, max_units: int):
        """
        Initialize an inventory
        
        Args:
            max_units: Maximum number of units this inventory can hold
        """
        self.max_units = max_units
        self.items: Dict[InventoryType, int] = {}  # type -> quantity
        self.on_items_added = Signal('on_items_added')
        self.on_items_removed = Signal('on_items_removed')
    
    def get_total_units(self) -> int:
        """Get the total number of units in the inventory"""
        return sum(self.items.values())
    
    def get_available_space(self) -> int:
        """Get the number of units that can still be added"""
        return self.max_units - self.get_total_units()
    
    def can_add(self, item_type: InventoryType, quantity: int) -> bool:
        """Check if the specified quantity can be added to the inventory"""
        return self.get_available_space() >= quantity
    
    def add_item(self, item_type: InventoryType, quantity: int) -> bool:
        """
        Add items to the inventory
        
        Args:
            item_type: Type of item to add
            quantity: Number of units to add
            
        Returns:
            bool: True if items were added successfully
        """
        if not self.can_add(item_type, quantity):
            return False
            
        self.items[item_type] = self.items.get(item_type, 0) + quantity
        
        # Emit signal
        self.on_items_added.send(self, item_type=item_type, quantity=quantity)
        
        return True
    
    def remove_item(self, item_type: InventoryType, amount: float) -> bool:
        """Remove items from inventory"""
        if item_type not in self.items:
            return False
        
        if self.items[item_type] < amount:
            return False
        
        self.items[item_type] -= amount
        if self.items[item_type] <= 0:
            del self.items[item_type]
        self.on_items_removed.send(self, item_type=item_type, quantity=amount)
        return True
    
    def get_item_quantity(self, item_type: InventoryType) -> int:
        """Get the quantity of a specific item type"""
        return self.items.get(item_type, 0)
    
    def get_all_items(self) -> Dict[InventoryType, int]:
        """Get a copy of all items in the inventory"""
        return self.items.copy()


class InventoryManager:
    """Manages inventories and transfers between them"""
    
    @staticmethod
    def transfer_items(
        source: Inventory,
        target: Inventory,
        item_type: InventoryType,
        quantity: int
    ) -> bool:
        """
        Transfer items between inventories
        
        Args:
            source: Source inventory
            target: Target inventory
            item_type: Type of item to transfer
            quantity: Number of units to transfer
            
        Returns:
            bool: True if transfer was successful
        """
        # Check if source has enough items
        if source.get_item_quantity(item_type) < quantity:
            return False
            
        # Check if target has enough space
        if not target.can_add(item_type, quantity):
            return False
            
        # Perform the transfer
        if source.remove_item(item_type, quantity):
            if target.add_item(item_type, quantity):
                return True
            else:
                # Rollback if target add fails
                source.add_item(item_type, quantity)
        return False
    
    @staticmethod
    def transfer_all_items(source: Inventory, target: Inventory) -> Dict[InventoryType, int]:
        """
        Transfer all items from source to target
        
        Args:
            source: Source inventory
            target: Target inventory
            
        Returns:
            Dict mapping item types to quantities that were successfully transferred
        """
        transferred = {}
        for item_type, quantity in source.get_all_items().items():
            if InventoryManager.transfer_items(source, target, item_type, quantity):
                transferred[item_type] = quantity
        return transferred
    
    @staticmethod
    def transfer_all_possible_items(source: Inventory, target: Inventory) -> Dict[InventoryType, int]:
        """
        Transfer as many items as possible from source to target
        
        Args:
            source: Source inventory
            target: Target inventory
            
        Returns:
            Dict mapping item types to quantities that were successfully transferred
        """
        transferred = {}
        for item_type, quantity in source.get_all_items().items():
            # Calculate how many units can be transferred
            available_space = target.get_available_space()
            transfer_quantity = min(quantity, available_space)
            
            if transfer_quantity > 0:
                if InventoryManager.transfer_items(source, target, item_type, transfer_quantity):
                    transferred[item_type] = transfer_quantity
        return transferred 