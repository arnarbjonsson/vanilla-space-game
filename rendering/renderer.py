"""
Renderer - handles all visual rendering using entity-specific renderers
"""

import arcade
from core.constants import *
from entities.player_entity import PlayerEntity
from entities.asteroid_entity import AsteroidEntity
from entities.mobile_depot import MobileDepot
from game_state.game_state import GameState
from rendering.player_renderer import PlayerRenderer
from rendering.asteroid_renderer import AsteroidRenderer
from rendering.background_renderer import BackgroundRenderer
from rendering.effects_renderer import EffectsRenderer
from rendering.mobile_depot_renderer import MobileDepotRenderer
from ui.ui_renderer import UIRenderer
from rendering.mined_item_effect_manager import MinedItemEffectManager


class Renderer:
    """Handles all visual rendering of the game using entity renderers"""
    
    def __init__(self, game_state: GameState):
        """Initialize the renderer with entity-specific renderers"""
        self.background_renderer = BackgroundRenderer()
        self.player_renderer = PlayerRenderer()
        self.asteroid_renderers = {}  # Map of asteroid entities to their renderers
        self.mobile_depot_renderers = {}  # Map of mobile depot entities to their renderers
        self.effects_renderer = EffectsRenderer()
        self.ui_renderer = UIRenderer(game_state=game_state)
        self.mined_item_effect_manager = MinedItemEffectManager()
        
    def initialize(self):
        """Initialize renderer resources"""
        # Initialize all sub-renderers
        self.background_renderer.initialize()
        
    def render(self, game_state):
        """Render the current game state"""
        # Render background first
        self.background_renderer.render()
        
        # Then render all entities
        self._render_entities(game_state)
        
        # Render effects between entities
        self.effects_renderer.render_effects(game_state)
        
        # Finally render UI on top
        self.ui_renderer.render(game_state)
        
        self.mined_item_effect_manager.render()
            
    def handle_mouse_click(self, x, y, game_state):
        """
        Handle mouse click events
        
        Args:
            x, y: Mouse click position
            game_state: Current game state
            
        Returns:
            bool: True if the click was handled by UI
        """
        return self.ui_renderer.handle_mouse_click(x, y, game_state)

    def _render_entities(self, game_state):
        """Render all entities using their specific renderers"""
        for entity in game_state.entities:
            if isinstance(entity, AsteroidEntity):
                # Get or create renderer for this asteroid
                if entity not in self.asteroid_renderers:
                    renderer = AsteroidRenderer(entity)
                    self.asteroid_renderers[entity] = renderer
                self.asteroid_renderers[entity].render(entity)
            elif isinstance(entity, MobileDepot):
                # Get or create renderer for this mobile depot
                if entity not in self.mobile_depot_renderers:
                    renderer = MobileDepotRenderer(entity)
                    self.mobile_depot_renderers[entity] = renderer
                self.mobile_depot_renderers[entity].render()

        self.player_renderer.render(game_state.player_entity)
