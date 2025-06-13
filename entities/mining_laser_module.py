"""
Mining Laser Module - mines ore from nearby asteroids
"""

import random
import time

from blinker import Signal

from audio.audio_engine import AudioEngine
from audio.sound_bank import SoundBank
from entities.base_module import BaseModule
from game_state.inventory_types import HitType, InventoryType
from game_state.game_events import on_asteroid_mined


# Mining Laser Constants - Easy to tune
MINING_RANGE = 200                   # Maximum mining distance in pixels
ORE_PER_CYCLE = 20                   # Amount of ore mined per activation

# Audio effect constants
LASER_SOUND_VOLUME = 0.5  # Volume level (0.0 to 1.0)

class MiningLaserModule(BaseModule):
    """Mining laser module that extracts ore from nearby asteroids"""
    
    # Override cycle times
    CYCLE_ACTIVE_TIME = 3.0  # How long laser beam stays visible
    CYCLE_COOLDOWN_TIME = 1.0  # Total cycle time in seconds
    
    def __init__(self):
        """Initialize the mining laser module"""
        super().__init__(
            name="Mining Laser",
            icon_path="assets/ming_laser_icon.png"  # Icon for UI 
        )
        
        # Mining properties
        self.mining_range = MINING_RANGE
        self.ore_per_cycle = ORE_PER_CYCLE
        
        # Visual effects
        self.current_target = None  # Currently targeted asteroid for visual effects
        self.active_timer = 0.0     # Timer for active state
    
    def _determine_hit_type(self) -> tuple[HitType, float]:
        """Determine the type of hit and its multiplier based on random rolls
        
        Returns:
            tuple[HitType, float]: The hit type and its corresponding multiplier
        """
        roll = random.random()
        
        # Check for super critical first (5% chance)
        if roll < HitType.SUPER_CRITICAL.chance:
            return HitType.SUPER_CRITICAL, HitType.SUPER_CRITICAL.multiplier
            
        # Then check for critical (25% chance)
        if roll < HitType.SUPER_CRITICAL.chance + HitType.CRITICAL.chance:
            return HitType.CRITICAL, HitType.CRITICAL.multiplier
            
        # Otherwise normal hit (70% chance)
        return HitType.NORMAL, HitType.NORMAL.multiplier
    
    def on_module_effect_start(self, ship_entity):
        """
        Called when the module effect starts - find and target asteroid
        
        Args:
            ship_entity: The ship this module is equipped to
            
        Returns:
            bool: True if targeting was successful
        """
        # Reset active timer when starting new activation
        self.active_timer = 0.0
        
        # Use the ship's targeting system to find the closest asteroid
        target_asteroid = ship_entity.find_closest_asteroid(max_range=self.mining_range)
        
        if target_asteroid is None:
            # No asteroids in range
            self.current_target = None
            return False
        
        # Store target for visual effects and register laser beam
        self.current_target = target_asteroid
        target_asteroid.start_mining(self)
        return True
    
    def _calculate_mining_amount(self, remaining_ore: int) -> tuple[int, HitType]:
        """Calculate how much ore to mine based on hit type and remaining ore.
        
        Args:
            remaining_ore: Amount of ore remaining in the asteroid
            
        Returns:
            tuple[int, HitType]: Amount to mine and the hit type
        """
        hit_type, multiplier = self._determine_hit_type()
        base_amount = min(self.ore_per_cycle, remaining_ore)
        return int(base_amount * multiplier), hit_type


    def _transfer_ore(self, ship_entity, ore_type: InventoryType, amount: int, hit_type: HitType) -> bool:
        """Transfer ore from asteroid to ship inventory.
        
        Args:
            ship_entity: The ship to transfer ore to
            ore_type: Type of ore to transfer
            amount: Amount to transfer
            hit_type: Type of mining hit
            
        Returns:
            bool: True if transfer was successful
        """
        # First try to mine from asteroid
        if not self.current_target.inventory.remove_item(self.current_target.ore_type, amount):
            print("Mining failed: Could not mine ore from asteroid: {} / {} ".format(amount, self.current_target.inventory.get_item_quantity(self.current_target.ore_type)))
            return False

        # Add to ship inventory
        if not ship_entity.inventory.add_item(ore_type, amount):
            print("Transfer failed: Could not transfer ore from asteroid.")
            return False
            
        return True

    def on_module_effect_end(self, ship_entity):
        """Called when the module effect ends - mine the targeted asteroid"""
        if not self._validate_mining_state(ship_entity):
            return False
            
        # Calculate mining amount
        remaining_ore = self.current_target.inventory.get_item_quantity(self.current_target.ore_type)
        mining_amount, hit_type = self._calculate_mining_amount(remaining_ore)

        # Calculate how much will fit in ship inventory
        available_space = ship_entity.inventory.get_available_space()
        actual_amount = min(mining_amount, available_space)

        if actual_amount <= 0:
            print("Mining failed: Inventory full.")
            AudioEngine.get_instance().play_sound(SoundBank.WARNING)
            return False

        # Transfer the ore
        if not self._transfer_ore(ship_entity, self.current_target.ore_type, actual_amount, hit_type):
            print("Mining failed: Could not transfer ore to ship inventory.", actual_amount)
            return False
        else:
            on_asteroid_mined.send(self.current_target, amount=actual_amount, hit_type=hit_type)

        # Update stats and play effects
        self._play_ore_mined_sound(self.current_target.ore_type, actual_amount, hit_type)

        return True

    def _validate_mining_state(self, ship_entity) -> bool:
        """Validate that mining can proceed."""
        if self.current_target is None:
            print("Mining failed: No target asteroid")
            return False
            
        if not ship_entity or not ship_entity.inventory:
            print("Mining failed: No player inventory available")
            return False
            
        remaining_ore = self.current_target.inventory.get_item_quantity(self.current_target.ore_type)
        if remaining_ore <= 0:
            print("Mining failed: Asteroid is depleted")
            return False
            
        return True

    def _on_cooldown_complete(self):
        """Called when cooldown period ends"""
        # Could play a sound effect or show notification
        pass
    
    def _start_cooldown(self):
        """Override to clear visual target when laser stops firing"""
        super()._start_cooldown()
        if self.current_target:
            self.current_target.stop_mining()
        self.current_target = None

    def _play_laser_sound(self):
        AudioEngine.get_instance().play_sound(SoundBank.LASER_BEAM, duration=self.CYCLE_ACTIVE_TIME, loop=False)

    def _play_ore_mined_sound(self, ore_type, amount, hit_type):
        """Play sound effect when ore is successfully mined
        
        Args:
            ore_type: Type of ore that was mined
            amount: Amount of ore mined
            hit_type: Type of mining hit (normal, critical, super critical)
        """
        # Base volume for normal hits
        base_volume = 0.5
        
        # Adjust volume and pitch based on hit type
        if hit_type == HitType.SUPER_CRITICAL:
            volume = base_volume * 1.5  # 50% louder
            pitch_shift = 1.5  # Higher pitch for super critical
        elif hit_type == HitType.CRITICAL:
            volume = base_volume * 1.25  # 25% louder
            pitch_shift = 1.25  # Higher pitch for critical
        else:
            volume = base_volume
            pitch_shift = 1.0  # Normal pitch
            
        AudioEngine.get_instance().play_sound(
            SoundBank.SUCCESS,
            volume=volume,
            pitch_shift=pitch_shift
        )

    def _update_active_state(self, delta_time):
        """Update module while in active state - keep laser visible briefly"""
        self.active_timer += delta_time
        
        # After active duration, execute end effect and start cooldown
        if self.active_timer >= self.CYCLE_ACTIVE_TIME:
            self.active_timer = 0.0
            self.on_module_effect_end(self.fitted_to_ship_entity)
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
        
        # Start the module effect
        success = self.on_module_effect_start(ship_entity)
        
        if success:
            # Start playing the laser sound
            self._play_laser_sound()
            # Don't immediately start cooldown - let _update_active_state handle it
            # This allows the visual effect to be visible
            return True
        else:
            # Reset state if execution failed
            self.state = "ready"
            return False

    def update(self, delta_time):
        """Update module state including sound effects"""
        super().update(delta_time)
