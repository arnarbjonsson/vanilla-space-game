"""
Mobile Depot Renderer - Handles rendering of mobile depot entities
"""

import arcade
from rendering.base_renderer import BaseRenderer
import math
import random

ICON_SIZE = 64


class MobileDepotRenderer(BaseRenderer):
    """Handles rendering of mobile depot entities"""
    
    def __init__(self, mobile_depot):
        """Initialize the mobile depot renderer
        
        Args:
            mobile_depot: The mobile depot entity to render
        """
        self.mobile_depot = mobile_depot
        
        # Visual properties
        self.size = mobile_depot.get_collision_radius() * 2
        self.color = arcade.color.BLUE
        self.texture = None
        self._load_textures()
        
        # Connect to inventory events
        self.mobile_depot.inventory.on_items_added.connect(self._on_items_added)
        
        # List to store orbiting icons
        self.orbiting_icons = []
        
    def _load_textures(self):
        """Load the mobile depot texture"""
        try:
            self.texture = arcade.load_texture("assets/mobile_depot.png")
        except FileNotFoundError:
            print("Warning: Could not load assets/mobile_depot.png")
            self.texture = None

    def render(self):
        """Render the mobile depot"""
        if not self.mobile_depot.active:
            return
            
        self.render_local()
        
    def render_local(self):
        """Render the mobile depot in local space"""
        if self.texture:
            # Draw the texture at twice the size of the current square
            arcade.draw_texture_rect(
                self.texture,
                arcade.XYWH(self.mobile_depot.x, self.mobile_depot.y, self.size * 2, self.size * 2),
                angle=0
            )
        else:
            # Fallback: draw the blue square if texture fails to load
            left = self.mobile_depot.x - self.size / 2
            bottom = self.mobile_depot.y - self.size / 2
            arcade.draw_lbwh_rectangle_filled(
                left,
                bottom,
                self.size,
                self.size,
                self.color
            )
            arcade.draw_lbwh_rectangle_outline(
                left,
                bottom,
                self.size,
                self.size,
                arcade.color.WHITE,
                2
            )
        
        # Draw orbiting icons on top of the mobile depot
        self._draw_orbiting_icons()

    def _draw_orbiting_icons(self):
        """Draw the orbiting icons"""
        for icon in self.orbiting_icons:
            # Update the icon position
            icon['angle'] += icon['speed'] * arcade.get_window().delta_time
            # Calculate the orbit radius based on the remaining duration
            orbit_radius = self.size * (icon['duration'] / 3)  # 3 is the initial duration
            icon['x'] = self.mobile_depot.x + orbit_radius * math.cos(math.radians(icon['angle']))
            icon['y'] = self.mobile_depot.y + orbit_radius * math.sin(math.radians(icon['angle']))
            
            # Draw the icon
            arcade.draw_texture_rect(
                icon['texture'],
                arcade.XYWH(icon['x'], icon['y'], ICON_SIZE, ICON_SIZE),  # Fixed size for icons
                angle=0
            )
            
            # Remove the icon if it has been on the screen for the entire duration
            icon['duration'] -= arcade.get_window().delta_time
            if icon['duration'] <= 0:
                self.orbiting_icons.remove(icon)

    def _on_items_added(self, inventory, item_type, quantity):
        """Handle items added to the mobile depot inventory"""
        # Spew out item icons
        self._spew_item_icons(item_type, quantity)
        
    def _spew_item_icons(self, item_type, quantity):
        """Spew out item icons when items are transferred"""
        # Load the item icon texture
        try:
            icon_texture = arcade.load_texture(f"assets/icons/types/{item_type.name.lower()}.png")
        except FileNotFoundError:
            print(f"Warning: Could not load icon for {item_type}")
            return
        
        # Create an icon that orbits the mobile depot for 3 seconds
        self._create_orbiting_icon(icon_texture, 3)
        
    def _create_orbiting_icon(self, icon_texture, duration):
        """Create an icon that orbits the mobile depot for a specified duration"""
        # Calculate the orbit radius
        orbit_radius = self.size * 1.5
        
        # Calculate the orbit speed
        orbit_speed = 360 / duration  # degrees per second
        
        # Randomize the start angle
        orbit_angle = random.uniform(0, 360)
        
        # Calculate the icon position
        icon_x = self.mobile_depot.x + orbit_radius * math.cos(math.radians(orbit_angle))
        icon_y = self.mobile_depot.y + orbit_radius * math.sin(math.radians(orbit_angle))
        
        # Add the icon to the orbiting icons list
        self.orbiting_icons.append({
            'texture': icon_texture,
            'x': icon_x,
            'y': icon_y,
            'angle': orbit_angle,
            'speed': orbit_speed,
            'duration': duration
        })
        
        # Draw the icon
        arcade.draw_texture_rect(
            icon_texture,
            arcade.XYWH(icon_x, icon_y, self.size, self.size),
            angle=0
        ) 