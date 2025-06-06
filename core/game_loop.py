"""
Main Game Loop - coordinates between input, game state, and rendering systems
"""

import arcade
from input.input_system import InputSystem
from game_state.state_manager import StateManager
from rendering.renderer import Renderer
from core.constants import BLACK


class GameLoop(arcade.View):
    """Main game loop that coordinates all systems"""
    
    def __init__(self, window):
        """Initialize the game loop with all systems"""
        super().__init__()
        self.window = window
        
        # Initialize the three core systems
        self.input_system = InputSystem()
        self.state_manager = StateManager()
        self.renderer = Renderer()
        
        # Set up the systems
        self._setup_systems()
        
    def _setup_systems(self):
        """Set up and configure all systems"""
        self.state_manager.initialize()
        self.renderer.initialize()
        
    def on_show_view(self):
        """Called when this view becomes active"""
        arcade.set_background_color(BLACK)
        
    def on_update(self, delta_time):
        """Main update loop - process input, update game state"""
        # Process input and get commands
        input_commands = self.input_system.process_input()
        
        # Update game state based on input and time
        self.state_manager.update(delta_time, input_commands)
        
    def on_draw(self):
        """Main render loop - draw everything"""
        self.clear()
        
        # Get current game state and render it
        current_state = self.state_manager.get_current_state()
        self.renderer.render(current_state)
        
    def on_key_press(self, key, modifiers):
        """Handle key press events"""
        self.input_system.on_key_press(key, modifiers)
        
    def on_key_release(self, key, modifiers):
        """Handle key release events"""
        self.input_system.on_key_release(key, modifiers) 