# Vanilla Space Game

A space exploration and mining game built with Python Arcade featuring realistic physics and clean architecture.

## Features

- **Realistic Spaceship Physics**: Thrust-based movement with momentum and drag
- **Asteroid Mining System**: Stationary asteroids with different ore types and quantities
- **Dynamic Visuals**: Spaceship textures and rotating asteroids with varied appearances
- **Clean Architecture**: Entity-Component-System design with separated rendering
- **Frame-Rate Independent**: Smooth gameplay regardless of system performance

## Current Gameplay

- **Spaceship Control**: Fly around with realistic thrust physics
- **Asteroid Field**: Navigate through 12 randomly distributed asteroids
- **Ore Resources**: Each asteroid contains different ore types (iron, copper, gold, platinum)
- **Visual Variety**: 6 different asteroid textures with random sizes and subtle rotation
- **Space Physics**: Momentum-based movement with natural deceleration

## Project Structure

```
vanilla-space-game/
├── main.py                     # Main entry point
├── core/
│   ├── constants.py           # Game configuration and constants
│   └── game_loop.py           # Main game loop coordination
├── entities/
│   ├── base_entity.py         # Abstract base class for all entities
│   ├── player_entity.py       # Player spaceship with physics
│   └── asteroid_entity.py     # Asteroid entities with ore properties
├── rendering/
│   ├── base_renderer.py       # Abstract renderer with coordinate transforms
│   ├── renderer.py            # Main renderer coordinator
│   ├── player_renderer.py     # Spaceship rendering with local coordinates
│   ├── asteroid_renderer.py   # Asteroid rendering with texture variation
│   └── background_renderer.py # Background image rendering
├── input/
│   ├── commands.py            # Input command enumeration
│   └── input_system.py        # Input handling and command generation
├── game_state/
│   ├── game_state.py          # Game state data container
│   └── state_manager.py       # Game state management and updates
├── ui/
│   └── ui_renderer.py         # User interface rendering
├── assets/
│   ├── spaceship.png          # Player spaceship texture
│   ├── asteroid1-6.png        # Six different asteroid textures
│   └── background.png         # Space background image
└── Pipfile                    # Pipenv dependencies
```

## Installation & Setup

### Prerequisites
- Python 3.11 (managed via pyenv)
- pipenv

### Installation

1. **Clone/Navigate to the project**:
   ```bash
   cd vanilla-space-game
   ```

2. **Install dependencies**:
   ```bash
   pipenv install
   ```

## Running the Game

```bash
pipenv run python main.py
```

## Game Controls

- **Rotation**: A/D keys (rotate left/right)
- **Thrust**: W key (accelerate forward)
- **Pause**: Esc key
- **Quit**: Close the window

## Game Mechanics

### Spaceship Physics
- **Thrust-based Movement**: Ship accelerates in the direction it's facing
- **Momentum**: Ship continues moving when not thrusting
- **Drag**: Natural deceleration over time (frame-rate independent)
- **Screen Wrapping**: Ship wraps around screen edges

### Asteroid System
- **Stationary Asteroids**: 12 asteroids distributed across the play area
- **Ore Resources**: Each asteroid contains 3-10 units of ore
- **Ore Types**: Iron, copper, gold, and platinum
- **Visual Variety**: 6 different textures with random scaling (15-45% size)
- **Subtle Rotation**: Each asteroid rotates slowly (3-5 degrees/second)

### Technical Features
- **Local Coordinate System**: Clean rendering with position/rotation transforms
- **Entity-Component Architecture**: Modular design for easy expansion
- **Frame-Rate Independence**: Consistent physics regardless of FPS
- **Asset Management**: Efficient texture loading with fallback rendering

## Architecture Highlights

The game demonstrates professional game development patterns:

### Entity-Component-System (ECS)
- **Entities**: Game objects with data (player, asteroids)
- **Systems**: Logic processors (input, physics, rendering)
- **Components**: Reusable data containers and behaviors

### Rendering Pipeline
- **Local Coordinates**: Entities work in local space for cleaner logic
- **Coordinate Transforms**: Automatic world-space conversion for rendering
- **Renderer Separation**: Each entity type has its dedicated renderer
- **Fallback Systems**: Graceful degradation if textures fail to load

### Input System
- **Command Pattern**: Input converted to abstract commands
- **Frame-Rate Independent**: Smooth controls regardless of FPS
- **Extensible**: Easy to add new input types and bindings

## Development

### Adding New Features

1. **New Entity Types**: Extend `BaseEntity` and create corresponding renderer
2. **Mining Mechanics**: Use existing `asteroid.mine_ore()` method
3. **Weapons System**: Add bullet entities and collision detection
4. **UI Elements**: Extend `UIRenderer` for new interface components

### Code Style

- **Clean Architecture**: Small, focused classes with single responsibilities
- **Separation of Concerns**: Clear boundaries between input, logic, and rendering
- **Local Coordinates**: Use coordinate transforms for clean entity logic
- **Frame-Rate Independence**: Always use `delta_time` for time-based calculations

## Dependencies

- **arcade**: Modern 2D game development library
- **Python 3.11**: Core language with type hints support

## Future Enhancements

- Asteroid mining mechanics
- Resource collection and management
- Weapon systems for asteroid breaking
- Upgrade system for spaceship
- Multiple asteroid fields/levels
- Sound effects and music

## License

This project is open source and available under the MIT License. 