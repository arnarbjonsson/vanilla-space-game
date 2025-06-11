"""
Input System - handles user input and converts it to game commands
"""

import arcade
from input.commands import InputCommand


class InputSystem:
    """Handles all user input and converts it to game commands"""
    
    def __init__(self):
        """Initialize the input system"""
        self.active_keys = set()
        self.commands_this_frame = []
        
    def process_input(self):
        """Process current input state and return commands"""
        commands = self._generate_commands_from_keys()
        
        # Get any one-time commands from this frame
        frame_commands = self.commands_this_frame.copy()
        self.commands_this_frame.clear()
        
        return commands + frame_commands
        
    def _generate_commands_from_keys(self):
        """Generate continuous commands from currently pressed keys"""
        commands = []
        
        # Rotation commands
        if arcade.key.LEFT in self.active_keys or arcade.key.A in self.active_keys:
            commands.append(InputCommand.ROTATE_LEFT)
            
        if arcade.key.RIGHT in self.active_keys or arcade.key.D in self.active_keys:
            commands.append(InputCommand.ROTATE_RIGHT)
            
        # Thrust command
        if arcade.key.UP in self.active_keys or arcade.key.W in self.active_keys:
            commands.append(InputCommand.THRUST)
            
        return commands
        
    def on_key_press(self, key, modifiers):
        """Handle key press events"""
        self.active_keys.add(key)
        
        # Handle one-time action commands
        if key == arcade.key.SPACE:
            self.commands_this_frame.append(InputCommand.SHOOT)
        elif key == arcade.key.ESCAPE:
            self.commands_this_frame.append(InputCommand.PAUSE)
        
        # Handle module activation commands
        elif key == arcade.key.KEY_1:
            self.commands_this_frame.append(InputCommand.ACTIVATE_MODULE_1)
        elif key == arcade.key.KEY_2:
            self.commands_this_frame.append(InputCommand.ACTIVATE_MODULE_2)
        elif key == arcade.key.KEY_3:
            self.commands_this_frame.append(InputCommand.ACTIVATE_MODULE_3)
        elif key == arcade.key.KEY_4:
            self.commands_this_frame.append(InputCommand.ACTIVATE_MODULE_4)
            
    def on_key_release(self, key, modifiers):
        """Handle key release events"""
        self.active_keys.discard(key)
        
    def is_key_pressed(self, key):
        """Check if a specific key is currently pressed"""
        return key in self.active_keys 