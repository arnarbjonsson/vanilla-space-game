"""
Module UI - handles module button rendering and interaction
"""

import arcade
import math
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class ModuleButton:
    """Represents a single module button"""
    
    def __init__(self, module, x, y, radius=30):
        """
        Initialize a module button
        
        Args:
            module: The module this button represents
            x, y: Center position of the button
            radius: Button radius in pixels
        """
        self.module = module
        self.x = x
        self.y = y
        self.radius = radius
        self.icon_texture = None
        self._load_icon()
    
    def _load_icon(self):
        """Load the module's icon texture"""
        if self.module.icon_path:
            try:
                self.icon_texture = arcade.load_texture(self.module.icon_path)
            except FileNotFoundError:
                print(f"Warning: Could not load module icon: {self.module.icon_path}")
                self.icon_texture = None
    
    def contains_point(self, x, y):
        """Check if a point is inside this button"""
        distance = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        return distance <= self.radius
    
    def render(self):
        """Render the module button"""
        # Determine button color based on module state
        if self.module.state == "ready":
            button_color = (64, 64, 64, 200)  # Dark gray with transparency
            border_color = (64, 64, 64, 255)  # Solid dark gray border
        elif self.module.state == "cooling_down":
            button_color = (255, 165, 0, 200)  # Orange with transparency
            border_color = (255, 165, 0, 255)  # Solid orange border
        else:  # active
            button_color = (0, 255, 0, 200)  # Green with transparency
            border_color = (0, 255, 0, 255)  # Solid green border
        
        # Draw button background circle
        arcade.draw_circle_filled(self.x, self.y, self.radius, button_color)
        
        # Draw button border
        arcade.draw_circle_outline(self.x, self.y, self.radius, border_color, 3)
        
        # Draw cycle progress arc if not ready
        if self.module.state != "ready":
            self._render_cycle_progress()
        
        # Draw module icon
        if self.icon_texture:
            # Scale icon to fit inside button (leave some padding)
            icon_size = self.radius * 1.2  # Slightly smaller than button
            arcade.draw_texture_rect(
                self.icon_texture,
                arcade.XYWH(self.x, self.y, icon_size, icon_size),
                angle=0
            )
        else:
            # Fallback: draw module name initial
            initial = self.module.name[0].upper() if self.module.name else "?"
            arcade.draw_text(
                initial,
                self.x, self.y,
                arcade.color.WHITE,
                font_size=16,
                anchor_x="center",
                anchor_y="center"
            )
    
    def _render_cycle_progress(self):
        """Render cycle progress as a circular arc"""
        progress = self.module.get_cycle_progress()
        
        # Draw progress arc (from top, clockwise)
        start_angle = 90  # Start at top
        end_angle = start_angle - (360 * progress)  # Clockwise progress

        if progress > 0:
            # Draw the remaining cycle arc in dark red (more visible against orange)
            arcade.draw_arc_outline(
                self.x, self.y, 
                self.radius * 2, self.radius * 2,  # width, height
                arcade.color.DARK_RED,
                end_angle, start_angle,  # remaining portion
                5  # line width
            )


class ModuleUI:
    """Handles module UI rendering and interaction"""
    
    def __init__(self):
        """Initialize the module UI system"""
        self.buttons = []
        self.button_spacing = 80  # Distance between button centers
        self.bottom_margin = 60   # Distance from bottom of screen
    
    def update(self, player_entity):
        """Update module buttons based on player's equipped modules"""
        if not player_entity:
            self.buttons.clear()
            return
        
        modules = player_entity.get_equipped_modules()
        self.buttons.clear()
        
        # Calculate starting position for centered buttons
        total_width = len(modules) * self.button_spacing - self.button_spacing
        start_x = (SCREEN_WIDTH - total_width) // 2
        
        # Create buttons for each module
        for i, module in enumerate(modules):
            x = start_x + i * self.button_spacing
            y = self.bottom_margin
            button = ModuleButton(module, x, y)
            self.buttons.append(button)
    
    def render(self):
        """Render all module buttons"""
        for button in self.buttons:
            button.render()
    
    def handle_mouse_click(self, x, y, player_entity):
        """
        Handle mouse click events
        
        Args:
            x, y: Mouse click position
            player_entity: Player entity to activate modules on
            
        Returns:
            bool: True if a button was clicked
        """
        for i, button in enumerate(self.buttons):
            if button.contains_point(x, y):
                # Activate the corresponding module
                if player_entity:
                    success = player_entity.activate_module(i)
                    return success
        return False 