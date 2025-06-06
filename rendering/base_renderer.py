"""
Base Renderer - defines the interface for entity-specific renderers
"""

import math
from abc import ABC, abstractmethod


class BaseRenderer(ABC):
    """Abstract base class for entity renderers"""
    
    def render(self, entity):
        """Render the entity with automatic position and rotation handling"""
        # Create a transformation helper for local coordinates
        transform = CoordinateTransform(entity.x, entity.y, entity.rotation)
        
        # Now render in local space using the transform helper
        self.render_local(entity, transform)
    
    @abstractmethod
    def render_local(self, entity, transform):
        """Render the entity in local coordinates - must be implemented by subclasses"""
        pass


class CoordinateTransform:
    """Helper class to transform local coordinates to world coordinates"""
    
    def __init__(self, world_x, world_y, rotation_degrees):
        self.world_x = world_x
        self.world_y = world_y
        self.rotation_rad = math.radians(rotation_degrees)
        self.cos_r = math.cos(self.rotation_rad)
        self.sin_r = math.sin(self.rotation_rad)
    
    def to_world(self, local_x, local_y):
        """Transform local coordinates to world coordinates"""
        # Rotate local coordinates
        rotated_x = local_x * self.cos_r - local_y * self.sin_r
        rotated_y = local_x * self.sin_r + local_y * self.cos_r
        
        # Translate to world position
        world_x = rotated_x + self.world_x
        world_y = rotated_y + self.world_y
        
        return world_x, world_y 