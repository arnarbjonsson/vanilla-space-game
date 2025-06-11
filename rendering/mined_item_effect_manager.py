import arcade
from game_state.inventory_types import INVENTORY_ICONS
from game_state.game_events import on_asteroid_mined

ITEM_POPUP_LIFETIME = 2.0  # 5 seconds
ITEM_POPUP_SPEED = 25  # Pixels per second
ITEM_POPUP_SIZE = 48  # Doubled from 32
ITEM_POPUP_OFFSET = 50  # Distance above asteroid

class OreMinedIndicatorEffect:
    """Represents a single ore mined indicator effect"""
    
    def __init__(self, item_type, x, y, amount, texture):
        self.item_type = item_type
        self.x = x
        self.y = y
        self.amount = amount
        self.texture = texture
        self.time_created = arcade.get_window().time
        
    def get_remaining_lifetime(self):
        """Get the remaining lifetime of the effect in seconds"""
        elapsed = arcade.get_window().time - self.time_created
        return max(0, ITEM_POPUP_LIFETIME - elapsed)
        
    def update(self):
        """Update the effect's state
        
        Returns:
            bool: True if effect is still active, False if it should be removed
        """
        remaining = self.get_remaining_lifetime()
        if remaining > 0:
            # Move up at a constant rate
            self.y += ITEM_POPUP_SPEED / 60  # Move at ITEM_POPUP_SPEED pixels per second
        return remaining > 0
        
    def render(self):
        """Render the effect"""
        remaining = self.get_remaining_lifetime()

        # Draw the icon with alpha
        arcade.draw_texture_rect(
            self.texture,
            arcade.XYWH(self.x, self.y, ITEM_POPUP_SIZE, ITEM_POPUP_SIZE),
            angle=0,
        )
        
        # Draw the amount text
        arcade.draw_text(
            f"+{self.amount}",
            self.x,
            self.y - ITEM_POPUP_SIZE/2 - 10,  # Position text below the icon
            arcade.color.WHITE,
            font_size=16,
            anchor_x="center",
            anchor_y="center"
        )

class MinedItemEffectManager:
    def __init__(self):
        self.active_effects = []
        self.item_textures = {}
        # Connect to the asteroid mined signal
        on_asteroid_mined.connect(self.on_asteroid_mined)

    def add_effect(self, item_type, x, y, amount):
        print(f"Effect manager received signal for {item_type} at ({x}, {y})")
        # Load texture if not already cached
        if item_type not in self.item_textures:
            try:
                texture_path = INVENTORY_ICONS[item_type]
                print(f"Loading texture from {texture_path}")
                self.item_textures[item_type] = arcade.load_texture(texture_path)
                print(f"Successfully loaded texture for {item_type}")
            except (KeyError, FileNotFoundError) as e:
                print(f"Warning: Could not load texture for {item_type}: {e}")
                return  # Skip adding effect if texture is missing
        
        # Create and add new effect
        effect = OreMinedIndicatorEffect(
            item_type=item_type,
            x=x,
            y=y + ITEM_POPUP_OFFSET,  # Start above the asteroid
            amount=amount,
            texture=self.item_textures[item_type]
        )
        self.active_effects.append(effect)
        print(f"Added effect, total active effects: {len(self.active_effects)}")

    def on_asteroid_mined(self, asteroid_entity, amount):
        """Handle the asteroid mined event"""
        print(f"Effect manager received asteroid mined signal for asteroid at ({asteroid_entity.x}, {asteroid_entity.y})")
        # Position effect above the asteroid, accounting for its radius
        y_offset = asteroid_entity.get_collision_radius() + ITEM_POPUP_OFFSET
        self.add_effect(asteroid_entity.ore_type, asteroid_entity.x, asteroid_entity.y + y_offset, amount)

    def render(self):
        """Render all active effects and update their state"""
        expired = []
        for effect in self.active_effects:
            if not effect.update():
                expired.append(effect)
        for effect in expired:
            self.active_effects.remove(effect)
            print(f"Effect manager: Removed expired effect, remaining: {len(self.active_effects)}")
        
        if self.active_effects:
            print(f"Effect manager: Rendering {len(self.active_effects)} effects")
        for effect in self.active_effects:
            effect.render() 