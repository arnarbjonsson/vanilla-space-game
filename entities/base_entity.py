"""
Base Entity - defines the interface for all game entities
"""

from abc import ABC, abstractmethod


class BaseEntity(ABC):
    """Abstract base class for all game entities"""
    
    def __init__(self, x=0, y=0):
        """Initialize entity with position"""
        self.x = x
        self.y = y
        self.active = True
        
    @abstractmethod
    def update(self, delta_time, input_commands=None):
        """Update entity logic - must be implemented by subclasses"""
        pass
        
    def destroy(self):
        """Mark entity as inactive"""
        self.active = False
        
    def is_active(self):
        """Check if entity is active"""
        return self.active 