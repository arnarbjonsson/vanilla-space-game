"""
Base Module - defines the interface for spaceship modules/abilities
"""

from abc import ABC, abstractmethod
import time


class ModuleState:
    """Enumeration for module states"""
    READY = "ready"           # Module is ready to be activated
    ACTIVE = "active"         # Module is currently active/executing
    COOLING_DOWN = "cooling_down"  # Module is cooling down after use


class BaseModule(ABC):
    """Abstract base class for all spaceship modules"""
    
    # Class-level constants for cycle times
    CYCLE_ACTIVE_TIME = 3.5  # Time in seconds for active state
    CYCLE_COOLDOWN_TIME = 4.0  # Time in seconds for cooldown state
    
    def __init__(self, name, icon_path=None):
        """
        Initialize module
        
        Args:
            name: Display name of the module
            icon_path: Path to module icon for UI
        """
        self.name = name
        self.icon_path = icon_path
        
        # State management
        self.state = ModuleState.READY
        self.cooldown_remaining = 0.0
        self.last_activation_time = 0.0
        self.fitted_to_ship_entity = None
        
        # Module properties
        self.active = True
        self.equipped = False  # Whether module is equipped to a ship
        self.module_index = -1  # Index in ship's module list
        
    def update(self, delta_time):
        """Update module state and cooldown timer"""
        if not self.active:
            return
        
        # Update cooldown timer
        if self.state == ModuleState.COOLING_DOWN:
            self.cooldown_remaining -= delta_time
            
            if self.cooldown_remaining <= 0.0:
                self.cooldown_remaining = 0.0
                self.state = ModuleState.READY
                self._on_cooldown_complete()
        
        # Update active state
        elif self.state == ModuleState.ACTIVE:
            self._update_active_state(delta_time)
    
    def can_activate(self):
        """Check if module can be activated"""
        return self.active and self.equipped and self.state == ModuleState.READY
    
    def activate(self, ship_entity):
        """
        Activate the module if possible
        
        Args:
            ship_entity: The ship this module is equipped to
            
        Returns:
            bool: True if activation was successful
        """
        if not self.can_activate():
            return False
        
        self.state = ModuleState.ACTIVE
        self.last_activation_time = time.time()
        
        # Start the module's effect
        success = self.on_module_effect_start(ship_entity)
        
        if success:
            # Don't start cooldown yet - let _update_active_state handle it
            return True
        else:
            # Reset state if execution failed
            self.state = ModuleState.READY
            return False
    
    def _start_cooldown(self):
        """Start the cooldown period"""
        self.state = ModuleState.COOLING_DOWN
        self.cooldown_remaining = self.CYCLE_COOLDOWN_TIME
    
    def get_cycle_progress(self):
        """
        Get cycle progress as a percentage
        
        Returns:
            float: Progress from 0.0 (just started) to 1.0 (ready)
        """
        if self.state == ModuleState.READY:
            return 1.0
        elif self.state == ModuleState.COOLING_DOWN:
            return 1.0 - (self.cooldown_remaining / self.CYCLE_COOLDOWN_TIME)
        elif self.state == ModuleState.ACTIVE:
            return self.active_timer / self.CYCLE_ACTIVE_TIME
        else:
            return 0.0
    
    def get_module_index(self):
        """
        Get the index of this module in its ship's module list
        
        Returns:
            int: Module index, or -1 if not equipped
        """
        return self.module_index if self.equipped else -1
    
    def equip_to_ship(self, ship_entity):
        """Equip this module to a ship"""
        self.equipped = True
        # Find our index in the ship's module list
        self.module_index = ship_entity.modules.index(self)
        self.fitted_to_ship_entity = ship_entity
        self._on_equipped(ship_entity)
    
    def unequip_from_ship(self, ship_entity):
        """Unequip this module from a ship"""
        self.equipped = False
        self.module_index = -1
        self._on_unequipped(ship_entity)
    
    def destroy(self):
        """Deactivate the module"""
        self.active = False
        self.equipped = False
    
    # Abstract methods to be implemented by subclasses
    @abstractmethod
    def on_module_effect_start(self, ship_entity):
        """
        Called when the module effect starts
        
        Args:
            ship_entity: The ship this module is equipped to
            
        Returns:
            bool: True if effect start was successful
        """
        pass
    
    @abstractmethod
    def on_module_effect_end(self, ship_entity):
        """
        Called when the module effect ends
        
        Args:
            ship_entity: The ship this module is equipped to
            
        Returns:
            bool: True if effect end was successful
        """
        pass
    
    # Optional overrides for subclasses
    def _update_active_state(self, delta_time):
        """
        Update module while in active state
        Override for modules that have ongoing effects
        """
        pass
    
    def _on_equipped(self, ship_entity):
        """Called when module is equipped to a ship"""
        pass
    
    def _on_unequipped(self, ship_entity):
        """Called when module is unequipped from a ship"""
        pass
    
    def _on_cooldown_complete(self):
        """Called when cooldown period ends"""
        pass
    
    def __str__(self):
        """String representation of the module"""
        return f"{self.name} ({self.state}, {self.cooldown_remaining:.1f}s remaining)" 