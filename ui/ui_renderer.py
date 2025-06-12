"""
UI Renderer - handles all user interface rendering
"""

import arcade
from core.constants import *
from ui.module_ui import ModuleUI
from game_state.game_state import GameState
from ui.inventory import InventoryUIRenderer


class UIRenderer:
    """Handles rendering of all UI elements"""
    
    def __init__(self, game_state: GameState):
        """Initialize the UI renderer"""
        self.module_ui = ModuleUI()
        self.inventory_renderer = InventoryUIRenderer(game_state=game_state)
        
    def render(self, game_state: GameState):
        """Render all UI elements
        
        Args:
            game_state: Current game state
        """
        self._render_hud(game_state)
        self._render_controls_hint()
        
        # Update and render module UI
        self.module_ui.update(game_state.player_entity)
        self.module_ui.render()
        
        # Render inventory UI
        self.inventory_renderer.render()
    
    def handle_mouse_click(self, x: float, y: float, game_state: GameState) -> bool:
        """Handle mouse click events
        
        Args:
            x: Mouse x coordinate
            y: Mouse y coordinate
            game_state: Current game state
            
        Returns:
            bool: True if the click was handled by UI
        """
        # Check if module UI handled the click
        if game_state.player_entity:
            return self.module_ui.handle_mouse_click(x, y, game_state.player_entity)
        
        return False
            
    def _render_hud(self, game_state):
        """Render heads-up display elements"""
        # Draw game time
        arcade.draw_text(
            f"Time: {game_state.game_time:.1f}s",
            10, SCREEN_HEIGHT - 60,
            WHITE,
            font_size=16
        )

    def _render_controls_hint(self):
        """Render controls information"""
        arcade.draw_text(
            "Controls: A/D to rotate, W to thrust, 1-4 for modules",
            10, 20,
            WHITE,
            font_size=12
        ) 