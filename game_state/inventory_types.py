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
    PLEXITE = auto()           # Basic mineral, used in many structures
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
    InventoryType.PLEXITE: "assets/icons/types/plexite.png",
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
        InventoryType.TRITANIUM: 0.4,  # 40% Tritanium
        InventoryType.PLEXITE: 0.1,    # 10% Plexite
    },
    InventoryType.SCORDITE: {
        InventoryType.TRITANIUM: 0.3,  # 30% Tritanium
        InventoryType.PLEXITE: 0.2,    # 20% Plexite
    },
    InventoryType.PYROXERES: {
        InventoryType.TRITANIUM: 0.2,  # 20% Tritanium
        InventoryType.PLEXITE: 0.3,    # 30% Plexite
        InventoryType.MEXALLON: 0.1,   # 10% Mexallon
    },
    InventoryType.PLAGIOCLASE: {
        InventoryType.TRITANIUM: 0.1,  # 10% Tritanium
        InventoryType.PLEXITE: 0.2,    # 20% Plexite
        InventoryType.MEXALLON: 0.2,   # 20% Mexallon
    },
    InventoryType.OMBER: {
        InventoryType.TRITANIUM: 0.1,  # 10% Tritanium
        InventoryType.PLEXITE: 0.2,    # 20% Plexite
        InventoryType.ISOGEN: 0.1,     # 10% Isogen
    }
}
