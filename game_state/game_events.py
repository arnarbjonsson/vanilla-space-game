from blinker import Signal

# Signal emitted when an asteroid is mined
# Parameters:
#   - asteroid_entity: The asteroid that was mined
#   - amount: The amount of ore that was mined
#   - hit_type: The type of hit (normal, critical, super_critical)
on_asteroid_mined = Signal('on_asteroid_mined')

# Signal emitted when items are added to an inventory
# Parameters:
#   - inventory: The inventory that items were added to
#   - item_type: The type of item that was added
#   - amount: The amount of items that were added
on_inventory_item_added = Signal('on_inventory_item_added')

# Signal emitted when items are removed from an inventory
# Parameters:
#   - inventory: The inventory that items were removed from
#   - item_type: The type of item that was removed
#   - amount: The amount of items that were removed
on_inventory_item_removed = Signal('on_inventory_item_removed') 