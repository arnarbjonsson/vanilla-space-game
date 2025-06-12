from .animated import AnimatedWalkingSprite as AnimatedWalkingSprite, TextureAnimation as TextureAnimation, TextureAnimationSprite as TextureAnimationSprite, TextureKeyframe as TextureKeyframe
from .base import BasicSprite as BasicSprite, SpriteType as SpriteType, SpriteType_co as SpriteType_co
from .colored import SpriteCircle as SpriteCircle, SpriteSolidColor as SpriteSolidColor
from .enums import FACE_DOWN as FACE_DOWN, FACE_LEFT as FACE_LEFT, FACE_RIGHT as FACE_RIGHT, FACE_UP as FACE_UP
from .mixins import PyMunk as PyMunk, PymunkMixin as PymunkMixin
from .sprite import Sprite as Sprite
from pathlib import Path

__all__ = ['SpriteType', 'SpriteType_co', 'BasicSprite', 'Sprite', 'PyMunk', 'TextureAnimationSprite', 'TextureAnimation', 'TextureKeyframe', 'AnimatedWalkingSprite', 'load_animated_gif', 'SpriteSolidColor', 'SpriteCircle', 'FACE_LEFT', 'FACE_RIGHT', 'FACE_UP', 'FACE_DOWN', 'PymunkMixin']

def load_animated_gif(resource_name: str | Path) -> TextureAnimationSprite: ...
