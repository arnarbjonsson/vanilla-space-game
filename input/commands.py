"""
Input Commands - defines all possible input actions
"""

from enum import Enum


class InputCommand(Enum):
    """Enumeration of all possible input commands"""
    
    # Movement commands
    ROTATE_LEFT = "rotate_left"
    ROTATE_RIGHT = "rotate_right"
    THRUST = "thrust"
    
    # Action commands
    SHOOT = "shoot"
    PAUSE = "pause"
    
    # Menu commands (for future use)
    CONFIRM = "confirm"
    CANCEL = "cancel" 