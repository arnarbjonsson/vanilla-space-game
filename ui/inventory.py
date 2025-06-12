import arcade
import math
from game_state.inventory_types import INVENTORY_ICONS, InventoryType, ORE_NAMES

class InventoryUIRenderer:
    """Renders the player's inventory UI"""
    
    # UI Constants
    PANEL_WIDTH = 300
    PANEL_HEIGHT = 600
    PANEL_COLOR = (0, 0, 0, 25)  # Black with 10% opacity
    PADDING = 30
    TITLE_FONT_SIZE = 20
    ITEM_FONT_SIZE = 16
    ITEM_SPACING = 48
    ICON_SIZE = 48
    FONT_NAME = "EveSansNeue-Regular"
    
    # Capacity bar constants
    CAPACITY_BAR_HEIGHT = 8
    CAPACITY_BAR_PADDING = 4
    CAPACITY_BAR_BG_COLOR = (255, 255, 255, 51)  # White with 20% opacity
    CAPACITY_BAR_FILL_COLOR = (255, 255, 255, 255)  # Solid white
    WARNING_THRESHOLD = 0.9  # 90% full
    BLINK_SPEED = 2.0  # Blinks per second
    
    def __init__(self, game_state):
        """Initialize the inventory UI renderer"""
        self.game_state = game_state
        self.item_textures = {}  # Cache for loaded textures
        self._load_textures()
        self.blink_time = 0.0  # Track time for blinking effect

    def _load_textures(self):
        """Load all inventory item textures"""
        for item_type in InventoryType:
            try:
                texture_path = INVENTORY_ICONS[item_type]
                self.item_textures[item_type] = arcade.load_texture(texture_path)
            except (KeyError, FileNotFoundError) as e:
                print(f"Warning: Could not load texture for {item_type}: {e}")
                self.item_textures[item_type] = None
    
    def _draw_capacity_bar(self, x, y, width, current, maximum):
        """Draw the inventory capacity bar
        
        Args:
            x: Left x coordinate
            y: Top y coordinate
            width: Width of the bar
            current: Current inventory usage
            maximum: Maximum inventory capacity
        """
        # Draw background
        arcade.draw_lbwh_rectangle_filled(
            x,
            y - self.CAPACITY_BAR_HEIGHT,
            width,
            self.CAPACITY_BAR_HEIGHT,
            self.CAPACITY_BAR_BG_COLOR
        )
        
        # Calculate fill width based on current/maximum
        fill_width = (current / maximum) * width
        
        # Draw fill
        if fill_width > 0:
            # Calculate blink opacity if near full
            opacity = 255
            if current / maximum >= self.WARNING_THRESHOLD:
                # Update blink time
                self.blink_time += arcade.get_window().delta_time
                # Calculate opacity using sine wave (0.5 to 1.0 range)
                opacity = int(255 * (0.5 + 0.5 * math.sin(self.blink_time * self.BLINK_SPEED * math.pi)))
            
            # Create color with current opacity
            fill_color = (255, 255, 255, opacity)
            
            arcade.draw_lbwh_rectangle_filled(
                x,
                y - self.CAPACITY_BAR_HEIGHT,
                fill_width,
                self.CAPACITY_BAR_HEIGHT,
                fill_color
            )
    
    def render(self):
        """Render the inventory UI"""
        if not self.game_state or not self.game_state.player_entity:
            print("Cannot render inventory: game_state or player_entity is None")
            return
            
        # Get player's inventory
        inventory = self.game_state.player_entity.inventory
        if not inventory:
            print("Cannot render inventory: player inventory is None")
            return
            
        # Calculate panel position (top-right corner)
        screen_width = arcade.get_window().width
        panel_x = screen_width - self.PANEL_WIDTH - self.PADDING
        panel_y = arcade.get_window().height - self.PADDING
        
        # Draw panel background
        arcade.draw_lbwh_rectangle_filled(
            panel_x,
            panel_y - self.PANEL_HEIGHT,
            self.PANEL_WIDTH,
            self.PANEL_HEIGHT,
            self.PANEL_COLOR
        )
        
        # Draw inventory title
        arcade.draw_text(
            "Mineral Hold",
            panel_x + self.PADDING,
            panel_y - self.PADDING - self.TITLE_FONT_SIZE,
            arcade.color.ASH_GREY,
            self.TITLE_FONT_SIZE,
            font_name=self.FONT_NAME
        )
        
        # Draw inventory capacity bar
        bar_y = panel_y - self.PADDING - self.TITLE_FONT_SIZE - 32
        self._draw_capacity_bar(
            panel_x + self.PADDING,
            bar_y,
            self.PANEL_WIDTH - (self.PADDING * 2),
            inventory.get_total_units(),
            inventory.max_units
        )
        
        # Draw inventory contents
        if not inventory.items:
            # Draw "Empty" text if inventory is empty
            arcade.draw_text(
                "Empty",
                panel_x + self.PADDING,
                bar_y - self.CAPACITY_BAR_HEIGHT - self.ITEM_SPACING,
                arcade.color.WHITE,
                self.ITEM_FONT_SIZE,
                font_name=self.FONT_NAME
            )
        else:
            # Draw each item in the inventory
            y = bar_y - self.CAPACITY_BAR_HEIGHT - self.ITEM_SPACING
            for item_type, quantity in inventory.items.items():
                # Draw item icon
                if item_type in self.item_textures and self.item_textures[item_type]:
                    arcade.draw_texture_rect(
                        self.item_textures[item_type],
                        arcade.XYWH(
                            panel_x + self.PADDING + self.ICON_SIZE/2,
                            y,
                            self.ICON_SIZE,
                            self.ICON_SIZE,
                        )
                    )
                
                # Draw item quantity and name
                name = ORE_NAMES.get(item_type, item_type.name.title())
                text = f"{quantity} x {name}"
                arcade.draw_text(
                    text,
                    panel_x + self.PADDING + self.ICON_SIZE + 4,
                    y - 8,
                    arcade.color.Color(255, 255, 255, 200),  # Semi-transparent white
                    self.ITEM_FONT_SIZE,
                    font_name=self.FONT_NAME
                )
                
                y -= self.ITEM_SPACING
    
    def _draw_inventory_item(self, item_type: InventoryType, quantity: int, x: float, y: float):
        """Draw a single inventory item row
        
        Args:
            item_type: Type of inventory item
            quantity: Amount of the item
            x: Left x coordinate
            y: Top y coordinate
        """
        # Draw item icon
        if item_type in self.item_textures and self.item_textures[item_type]:
            arcade.draw_texture_rect(
                self.item_textures[item_type],
                arcade.XYWH(
                    x + self.ICON_SIZE/2,
                    y - self.ICON_SIZE/2,
                    self.ICON_SIZE,
                    self.ICON_SIZE
                ),
                angle=0
            )
        
        # Draw quantity x name
        name = ORE_NAMES.get(item_type, item_type.name.title())
        text = f"{quantity} x {name}"
        arcade.draw_text(
            text,
            x + self.ICON_SIZE + 10,
            y - 10,
            arcade.color.WHITE,
            self.ITEM_FONT_SIZE,
            font_name=self.FONT_NAME
        ) 