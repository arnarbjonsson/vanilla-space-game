"""
State Manager - manages game state and processes input commands
"""

from game_state.game_state import GameState
from entities.player_entity import PlayerEntity
from input.commands import InputCommand
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class StateManager:
    """Manages the current game state and processes updates"""
    
    def __init__(self):
        """Initialize the state manager"""
        self.current_state = GameState()
        
    def initialize(self):
        """Initialize the game state"""
        self._setup_initial_state()
        
    def _setup_initial_state(self):
        """Set up the initial game state"""
        # Create and add player entity at center bottom of larger screen
        player = PlayerEntity(SCREEN_WIDTH // 2, 100)  # Increased from 50 to 100 for better positioning
        self.current_state.player_entity = player
        self.current_state.add_entity(player)
        
        # Initialize game state
        self.current_state.score = 0
        self.current_state.is_game_running = True
        
    def update(self, delta_time, input_commands):
        """Update game state based on time and input commands"""
        if not self.current_state.is_game_running:
            return
            
        self._process_input_commands(input_commands, delta_time)
        self._update_entities(delta_time)
        self._update_game_logic(delta_time)
        
    def _process_input_commands(self, commands, delta_time):
        """Process input commands and route them to appropriate entities"""
        for command in commands:
            if command == InputCommand.SHOOT:
                self._handle_shoot_command()
            elif command == InputCommand.PAUSE:
                self.current_state.is_game_running = not self.current_state.is_game_running
                
        # Pass movement commands to player entity
        if self.current_state.player_entity:
            movement_commands = [cmd for cmd in commands 
                               if cmd in [InputCommand.ROTATE_LEFT, 
                                        InputCommand.ROTATE_RIGHT, 
                                        InputCommand.THRUST]]
            self.current_state.player_entity.update(delta_time, movement_commands)
        
    def _update_entities(self, delta_time):
        """Update all entities"""
        for entity in self.current_state.entities:
            entity.update(delta_time)
            
        # Clean up inactive entities
        self.current_state.cleanup_inactive_entities()
        
    def _handle_shoot_command(self):
        """Handle shooting action"""
        # For now, just increment score as a placeholder
        self.current_state.score += 1
        
    def _update_game_logic(self, delta_time):
        """Update game logic that doesn't depend on input"""
        # Update game timer
        self.current_state.game_time += delta_time
        
        # Add any time-based game logic here
        # For example: enemy spawning, bullet movement, etc.
        
    def get_current_state(self):
        """Get the current game state"""
        return self.current_state 