"""
Game State - holds all current game data
"""


class GameState:
    """Contains all current game state data"""
    
    def __init__(self):
        """Initialize game state with default values"""
        # Entity management
        self.entities = []
        self.player_entity = None
        
        # Game state
        self.score = 0
        self.game_time = 0.0
        self.is_game_running = False
        
    def add_entity(self, entity):
        """Add an entity to the game state"""
        self.entities.append(entity)
        
    def remove_entity(self, entity):
        """Remove an entity from the game state"""
        if entity in self.entities:
            self.entities.remove(entity)
            
    def get_entities_by_type(self, entity_class):
        """Get all entities of a specific type using isinstance"""
        return [entity for entity in self.entities if isinstance(entity, entity_class)]
        
    def cleanup_inactive_entities(self):
        """Remove inactive entities from the game state"""
        self.entities = [entity for entity in self.entities if entity.is_active()]
        
        # Check if player was destroyed
        if self.player_entity and not self.player_entity.is_active():
            self.player_entity = None
        
    def reset(self):
        """Reset the game state to initial values"""
        self.entities.clear()
        self.player_entity = None
        self.score = 0
        self.game_time = 0.0
        self.is_game_running = False 