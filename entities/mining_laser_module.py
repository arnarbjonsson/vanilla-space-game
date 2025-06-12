"""
Mining Laser Module - mines ore from nearby asteroids
"""

import math
import random
from entities.base_module import BaseModule
import time
import arcade
from blinker import Signal
from game_state.inventory_types import InventoryType, HitType

# Mining Laser Constants - Easy to tune
MINING_LASER_CYCLE_TIME = 4.0      # Total cycle time in seconds
MINING_LASER_ACTIVE_DURATION = 3.5  # How long laser beam stays visible
MINING_RANGE = 200                   # Maximum mining distance in pixels
ORE_PER_CYCLE = 20                   # Amount of ore mined per activation (10x)

# Critical Hit Constants
CRITICAL_HIT_CHANCE = 0.25          # 25% chance for critical hit
SUPER_CRITICAL_HIT_CHANCE = 0.05    # 5% chance for super critical hit
CRITICAL_MULTIPLIER = 1.25          # 25% more ore for critical hits
SUPER_CRITICAL_MULTIPLIER = 1.5     # 50% more ore for super critical hits

# Audio effect constants
LASER_SOUND = arcade.Sound("assets/audio/laser-beam.wav")
ORE_MINED_SOUND = arcade.Sound("assets/audio/success.wav")
LASER_SOUND_VOLUME = 0.5  # Volume level (0.0 to 1.0)
FADE_OUT_DURATION = 0.5  # Duration of fade out in seconds

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
        self.last_hit_type = HitType.NORMAL  # Track the last hit type for visual feedback
        
        # Visual effects
        self.current_target = None  # Currently targeted asteroid for visual effects
        self.active_duration = MINING_LASER_ACTIVE_DURATION
        self.active_timer = 0.0     # Timer for active state
        
        # Audio
        self.laser_sound_playback = None
        self.fade_out_timer = 0.0
        self.is_fading_out = False
        
        # Signal for when ore is mined
        self.on_ore_mined = Signal()
    
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
            self.last_mined_amount = 0
            self.last_mined_ore_type = None
            self.last_hit_type = HitType.NORMAL
            return False
        
        # Store target for visual effects and register laser beam
        self.current_target = target_asteroid
        return True
    
    def on_module_effect_end(self):
        """
        Called when the module effect ends - mine the targeted asteroid
        
        Returns:
            bool: True if mining was successful
        """
        if self.current_target is None:
            print("Mining failed: No target asteroid.")
            return False
            
        # Get the remaining ore amount
        remaining_ore = self.current_target.inventory.get_item_quantity(self.current_target.ore_type)
        if remaining_ore <= 0:
            print("Mining failed: No ore mined (asteroid depleted).")
            self.last_mined_amount = 0
            self.last_mined_ore_type = None
            self.last_hit_type = HitType.NORMAL
            return False
        
        # Determine hit type and multiplier
        hit_type, multiplier = self._determine_hit_type()
        self.last_hit_type = hit_type
            
        # Calculate how much we can mine (either full cycle or remaining amount)
        base_mining_amount = min(self.ore_per_cycle, remaining_ore)
        mining_amount = int(base_mining_amount * multiplier)
            
        # Mine ore from the target asteroid
        success = self.current_target.mine_ore(mining_amount, hit_type)
        
        if success:
            # Update mining stats
            self.last_mined_amount = mining_amount
            self.last_mined_ore_type = self.current_target.ore_type
            self.total_ore_mined += mining_amount

            self._play_ore_mined_sound()
            
            # Emit signal with mined ore details
            print(f"Mining successful: {hit_type.name_display.upper()} hit! Mined {mining_amount} units of {self.current_target.ore_type}.")
            self.on_ore_mined.send(
                self,
                ore_type=self.current_target.ore_type,
                amount=mining_amount,
                hit_type=hit_type
            )
            return True
        else:
            # No ore was mined (asteroid was already depleted)
            self.last_mined_amount = 0
            self.last_mined_ore_type = None
            self.last_hit_type = HitType.NORMAL
            print("Mining failed: No ore mined (asteroid depleted).")
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
        self._start_fade_out()
    
    def _play_laser_sound(self):
        """Play the laser beam sound effect in a loop"""
        if not self.laser_sound_playback:
            self.laser_sound_playback = arcade.play_sound(LASER_SOUND, volume=LASER_SOUND_VOLUME, loop=True)
            self.is_fading_out = False
            self.fade_out_timer = 0.0

    def _play_ore_mined_sound(self):
        """Play sound effect when ore is successfully mined"""
        ORE_MINED_SOUND.play()

    def _start_fade_out(self):
        """Start fading out the laser sound"""
        if self.laser_sound_playback and not self.is_fading_out:
            self.is_fading_out = True
            self.fade_out_timer = 0.0

    def _stop_laser_sound(self):
        """Stop the laser beam sound effect"""
        if self.laser_sound_playback:
            arcade.stop_sound(self.laser_sound_playback)
            self.laser_sound_playback = None
            self.is_fading_out = False
            self.fade_out_timer = 0.0

    def _update_active_state(self, delta_time):
        """Update module while in active state - keep laser visible briefly"""
        self.active_timer += delta_time
        
        # After active duration, execute end effect and start cooldown
        if self.active_timer >= self.active_duration:
            self.active_timer = 0.0
            self.on_module_effect_end()
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
        
        # Handle sound fade out
        if self.is_fading_out and self.laser_sound_playback:
            self.fade_out_timer += delta_time
            if self.fade_out_timer >= FADE_OUT_DURATION:
                self._stop_laser_sound()
            else:
                # Calculate new volume based on fade progress
                fade_progress = self.fade_out_timer / FADE_OUT_DURATION
                new_volume = LASER_SOUND_VOLUME * (1.0 - fade_progress)
                self.laser_sound_playback.volume = new_volume 