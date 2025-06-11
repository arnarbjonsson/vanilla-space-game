"""
UI Renderer - handles all user interface rendering
"""

import arcade
from core.constants import *
from ui.module_ui import ModuleUI


class UIRenderer:
    """Handles rendering of all UI elements"""
    
    def __init__(self):
        """Initialize the UI renderer"""
        self.module_ui = ModuleUI()
        
    def render(self, game_state):
        """Render all UI elements"""
        self._render_hud(game_state)
        self._render_controls_hint()
        
        # Update and render module UI
        self.module_ui.update(game_state.player_entity)
        self.module_ui.render()
        
        # Render pause overlay if game is paused
        if not game_state.is_game_running:
            self._render_pause_overlay()
    
    def handle_mouse_click(self, x, y, game_state):
        """
        Handle mouse click events for UI elements
        
        Args:
            x, y: Mouse click position
            game_state: Current game state
            
        Returns:
            bool: True if UI handled the click
        """
        # Check if module UI handled the click
        if game_state.player_entity:
            return self.module_ui.handle_mouse_click(x, y, game_state.player_entity)
        return False
            
    def _render_hud(self, game_state):
        """Render heads-up display elements"""
        # Draw score
        arcade.draw_text(
            f"Score: {game_state.score}",
            10, SCREEN_HEIGHT - 30,
            WHITE,
            font_size=20
        )
        
        # Draw game time
        arcade.draw_text(
            f"Time: {game_state.game_time:.1f}s",
            10, SCREEN_HEIGHT - 60,
            WHITE,
            font_size=16
        )
        
        # Draw player health if player exists
        if game_state.player_entity:
            health_percentage = game_state.player_entity.get_health_percentage()
            self._render_health_bar(10, SCREEN_HEIGHT - 90, health_percentage)
            
    def _render_health_bar(self, x, y, health_percentage):
        """Render a health bar using correct arcade functions"""
        bar_width = 100
        bar_height = 10
        
        # Background (red) - using left, bottom, width, height
        arcade.draw_lbwh_rectangle_filled(
            x, y, bar_width, bar_height, RED
        )
        
        # Health (green)
        health_width = bar_width * health_percentage
        if health_width > 0:
            arcade.draw_lbwh_rectangle_filled(
                x, y, health_width, bar_height, GREEN
            )
            
        # Health text
        arcade.draw_text(
            f"Health: {int(health_percentage * 100)}%",
            x + bar_width + 10, y,
            WHITE,
            font_size=12
        )
        
    def _render_controls_hint(self):
        """Render controls information"""
        arcade.draw_text(
            "Controls: A/D to rotate, W to thrust, 1-4 for modules, Esc to pause",
            10, 20,
            WHITE,
            font_size=12
        )
        
    def _render_pause_overlay(self):
        """Render pause overlay"""
        # Semi-transparent overlay using correct function
        arcade.draw_lbwh_rectangle_filled(
            0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,
            (0, 0, 0, 128)  # Semi-transparent black
        )
        
        # Pause text
        arcade.draw_text(
            "PAUSED",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
            WHITE,
            font_size=48,
            anchor_x="center",
            anchor_y="center"
        )
        
        arcade.draw_text(
            "Press ESC to resume",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
            WHITE,
            font_size=16,
            anchor_x="center",
            anchor_y="center"
        ) 