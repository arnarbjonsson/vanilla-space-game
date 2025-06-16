"""
Inventory Types - defines all possible inventory item types in the game
"""

from enum import Enum, auto
from typing import Dict, List, Tuple

class InventoryType(Enum):
    """Enumeration of all possible inventory item types"""
    
    # Ores
    VELDSPAR = auto()          # Most common ore, found in high security space
    SCORDITE = auto()          # Common ore, found in high security space
    PYROXERES = auto()         # Common ore, found in high security space
    PLAGIOCLASE = auto()       # Common ore, found in high security space
    OMBER = auto()             # Uncommon ore, found in low security space
    
    # Minerals (processed from ores)
    # Basic Minerals
    TRITANIUM = auto()         # Basic mineral, used in almost everything
    PYERITE = auto()           # Basic mineral, used in many structures
    MEXALLON = auto()          # Basic mineral, used in many structures
    ISOGEN = auto()            # Basic mineral, used in many structures
    
    # Advanced Minerals
    NOCXIUM = auto()           # Advanced mineral, used in advanced structures
    ZYDRINE = auto()           # Advanced mineral, used in advanced structures
    MEGACYTE = auto()          # Advanced mineral, used in advanced structures
    
    # Special Minerals
    PLEX = auto()              # Special mineral, used for subscription time
    MORPHITE = auto()          # Special mineral, used in advanced structures


# Module-level constants and utility functions
ORE_TYPES = {
    InventoryType.VELDSPAR,
    InventoryType.SCORDITE,
    InventoryType.PYROXERES,
    InventoryType.PLAGIOCLASE,
    InventoryType.OMBER
}

# Display names for ore types
ORE_NAMES: Dict[InventoryType, str] = {
    InventoryType.VELDSPAR: "Veldspar",
    InventoryType.SCORDITE: "Scordite",
    InventoryType.PYROXERES: "Pyroxeres",
    InventoryType.PLAGIOCLASE: "Plagioclase",
    InventoryType.OMBER: "Omber"
}

# Icon paths for all inventory types
INVENTORY_ICONS: Dict[InventoryType, str] = {
    # Ores
    InventoryType.VELDSPAR: "assets/icons/types/veldspar.png",
    InventoryType.SCORDITE: "assets/icons/types/scordite.png",
    InventoryType.PYROXERES: "assets/icons/types/pyroxeres.png",
    InventoryType.PLAGIOCLASE: "assets/icons/types/plagioclase.png",
    InventoryType.OMBER: "assets/icons/types/omber.png",
    
    # Basic Minerals
    InventoryType.TRITANIUM: "assets/icons/types/tritanium.png",
    InventoryType.PYERITE: "assets/icons/types/Pyerite.png",
    InventoryType.MEXALLON: "assets/icons/types/mexallon.png",
    InventoryType.ISOGEN: "assets/icons/types/isogen.png",
    
    # Advanced Minerals
    InventoryType.NOCXIUM: "assets/icons/types/nocxium.png",
    InventoryType.ZYDRINE: "assets/icons/types/zydrine.png",
    InventoryType.MEGACYTE: "assets/icons/types/megacyte.png",
    
    # Special Minerals
    InventoryType.PLEX: "assets/icons/types/plex.png",
    InventoryType.MORPHITE: "assets/icons/types/morphite.png"
}

# Define ore to mineral conversion rates
ORE_MINERAL_RATES: Dict[InventoryType, Dict[InventoryType, float]] = {
    InventoryType.VELDSPAR: {
        InventoryType.TRITANIUM: 1.0,  # 40% Tritanium
    },
    InventoryType.SCORDITE: {
        InventoryType.TRITANIUM: 0.60,  # 30% Tritanium
        InventoryType.PYERITE: 0.4,    # 20% Pyerite
    },
    InventoryType.PYROXERES: {
        InventoryType.TRITANIUM: 0.4,  # 20% Tritanium
        InventoryType.PYERITE: 0.5,    # 30% Pyerite
        InventoryType.MEXALLON: 0.1,   # 10% Mexallon
    },
    InventoryType.PLAGIOCLASE: {
        InventoryType.TRITANIUM: 0.2,  # 10% Tritanium
        InventoryType.PYERITE: 0.4,    # 20% Pyerite
        InventoryType.MEXALLON: 0.4,   # 20% Mexallon
    },
    InventoryType.OMBER: {
        InventoryType.TRITANIUM: 0.25,  # 10% Tritanium
        InventoryType.PYERITE: 0.50,    # 20% Pyerite
        InventoryType.ISOGEN: 0.25,     # 10% Isogen
    }
}

class HitType(Enum):
    """Enum representing different types of mining hits"""
    NORMAL = auto()
    CRITICAL = auto()
    SUPER_CRITICAL = auto()

    @property
    def multiplier(self) -> float:
        """Get the ore multiplier for this hit type"""
        if self == HitType.NORMAL:
            return 1.0
        elif self == HitType.CRITICAL:
            return 1.25
        elif self == HitType.SUPER_CRITICAL:
            return 1.5

    @property
    def chance(self) -> float:
        """Get the base chance for this hit type"""
        if self == HitType.NORMAL:
            return 0.50  # 70%
        elif self == HitType.CRITICAL:
            return 0.35  # 25%
        elif self == HitType.SUPER_CRITICAL:
            return 0.15  # 5%

    @property
    def name_display(self) -> str:
        """Get the display name for this hit type"""
        if self == HitType.NORMAL:
            return "normal"
        elif self == HitType.CRITICAL:
            return "critical"
        elif self == HitType.SUPER_CRITICAL:
            return "super_critical"
