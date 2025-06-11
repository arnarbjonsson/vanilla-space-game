"""
Mining Laser Module - mines ore from nearby asteroids
"""

import math
from entities.base_module import BaseModule
import time

# Mining Laser Constants - Easy to tune
MINING_LASER_CYCLE_TIME = 2.5      # Total cycle time in seconds
MINING_LASER_ACTIVE_DURATION = 2.0  # How long laser beam stays visible
MINING_RANGE = 200                   # Maximum mining distance in pixels
ORE_PER_CYCLE = 2                   # Amount of ore mined per activation


class MiningLaserModule(BaseModule):
    """Mining laser module that extracts ore from nearby asteroids"""
    
    def __init__(self):
        """Initialize the mining laser module"""
        super().__init__(
            name="Mining Laser",
            cycle_time=MINING_LASER_CYCLE_TIME,
            icon_path="assets/ming_laser_icon.png"  # Icon for UI 
        )
        
        # Mining properties
        self.mining_range = MINING_RANGE
        self.ore_per_cycle = ORE_PER_CYCLE
        
        # Statistics
        self.total_ore_mined = 0
        self.last_mined_ore_type = None
        self.last_mined_amount = 0
        
        # Visual effects
        self.current_target = None  # Currently targeted asteroid for visual effects
        self.active_duration = MINING_LASER_ACTIVE_DURATION
        self.active_timer = 0.0     # Timer for active state
    
    def _execute_module_effect(self, ship_entity):
        """
        Execute mining laser effect - mine ore from nearby asteroids
        
        Args:
            ship_entity: The ship this module is equipped to
            
        Returns:
            bool: True if mining was successful
        """
        # Reset active timer when starting new activation
        self.active_timer = 0.0
        
        # Use the ship's targeting system to find the closest asteroid
        target_asteroid = ship_entity.find_closest_asteroid(max_range=self.mining_range)
        
        if target_asteroid is None:
            # No asteroids in range
            self.current_target = None
            self.last_mined_amount = 0
            self.last_mined_ore_type = None
            return False
        
        # Store target for visual effects and register laser beam
        self.current_target = target_asteroid
        
        # Mine ore from the target asteroid
        mined_amount = target_asteroid.mine_ore(self.ore_per_cycle)
        
        if mined_amount > 0:
            # Successful mining
            self.last_mined_amount = mined_amount
            self.last_mined_ore_type = target_asteroid.ore_type
            self.total_ore_mined += mined_amount
            
            # You could add the ore to the ship's inventory here
            # For now, we'll just track statistics
            
            return True
        else:
            # No ore was mined (asteroid was already depleted)
            self.last_mined_amount = 0
            self.last_mined_ore_type = None
            return False
    
    def get_mining_stats(self):
        """Get mining statistics for this module"""
        return {
            'total_ore_mined': self.total_ore_mined,
            'last_mined_ore_type': self.last_mined_ore_type,
            'last_mined_amount': self.last_mined_amount
        }
    
    def get_status_text(self):
        """Get current status text for UI display"""
        if self.state == "ready":
            return "Mining Laser Ready"
        elif self.state == "cooling_down":
            return f"Recharging... ({self.cooldown_remaining:.1f}s)"
        elif self.state == "active":
            return "Firing Laser!"
        else:
            return "Mining Laser"
    
    def _on_cooldown_complete(self):
        """Called when cooldown period ends"""
        # Could play a sound effect or show notification
        pass
    
    def _start_cooldown(self):
        """Override to clear visual target when laser stops firing"""
        super()._start_cooldown()
        self.current_target = None
    
    def _update_active_state(self, delta_time):
        """Update module while in active state - keep laser visible briefly"""
        self.active_timer += delta_time
        
        # After active duration, start cooldown
        if self.active_timer >= self.active_duration:
            self.active_timer = 0.0
            self._start_cooldown()
    
    def activate(self, ship_entity):
        """
        Override activate to handle visual effect duration
        
        Args:
            ship_entity: The ship this module is equipped to
            
        Returns:
            bool: True if activation was successful
        """
        if not self.can_activate():
            return False
        
        self.state = "active"
        self.last_activation_time = time.time()
        
        # Execute the module's effect
        success = self._execute_module_effect(ship_entity)
        
        if success:
            # Don't immediately start cooldown - let _update_active_state handle it
            # This allows the visual effect to be visible
            return True
        else:
            # Reset state if execution failed
            self.state = "ready"
            return False 