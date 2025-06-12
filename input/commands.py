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
    
    # Module commands
    ACTIVATE_MODULE_1 = "activate_module_1"
    ACTIVATE_MODULE_2 = "activate_module_2"
    ACTIVATE_MODULE_3 = "activate_module_3"
    ACTIVATE_MODULE_4 = "activate_module_4"
    
    # Menu commands (for future use)
    CONFIRM = "confirm"
    CANCEL = "cancel" 