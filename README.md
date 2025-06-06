# Vanilla Space Game

A classic space shooter game built with Python Arcade and managed with pipenv.

## Features

- **Player Controls**: Move left/right with arrow keys or A/D, shoot with spacebar
- **Dynamic Enemies**: Enemies with different movement patterns (straight, zigzag, sine wave)
- **Collision Detection**: Bullets destroy enemies, enemies can hit the player
- **Score System**: Earn points by destroying enemies
- **Clean Architecture**: Well-structured code with separated concerns

## Project Structure

```
vanilla-space-game/
├── main.py                 # Main entry point
├── game/
│   ├── __init__.py        # Package initialization
│   ├── constants.py       # Game configuration and constants
│   ├── space_game.py      # Main game class and game loop
│   ├── player.py          # Player spaceship class
│   ├── enemy.py           # Enemy spaceship classes
│   └── bullet.py          # Bullet/projectile classes
├── Pipfile                # Pipenv dependencies
└── README.md              # This file
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
   python -m pipenv install
   ```

3. **Activate the virtual environment**:
   ```bash
   python -m pipenv shell
   ```

## Running the Game

```bash
python main.py
```

Or with pipenv:
```bash
python -m pipenv run python main.py
```

## Game Controls

- **Movement**: Arrow Keys (←/→) or A/D keys
- **Shoot**: Spacebar
- **Quit**: Close the window or press Alt+F4

## Game Mechanics

- **Player**: Blue triangle at the bottom of the screen
- **Enemies**: Red squares that spawn from the top with various movement patterns
- **Bullets**: Yellow projectiles fired by the player
- **Scoring**: 10 points per enemy destroyed
- **Collision**: Game over when an enemy hits the player

## Architecture

The game follows clean architecture principles:

- **Small, clear methods**: Each method has a single responsibility
- **Contained classes**: Each game entity is in its own class and file
- **Separation of concerns**: Game logic, rendering, and input handling are separated
- **Modular design**: Easy to extend with new features

## Development

### Adding New Features

1. **New Enemy Types**: Extend the `Enemy` class in `game/enemy.py`
2. **Power-ups**: Create new classes similar to existing entities
3. **Game States**: Add menu/game over screens in `space_game.py`
4. **Sound Effects**: Add sound loading and playing in appropriate classes

### Code Style

- Use clear, descriptive method names
- Keep methods small and focused
- Add docstrings to all classes and methods
- Follow PEP 8 style guidelines

## Dependencies

- **arcade**: 2D game development library
- **Python 3.11**: Core language

## License

This project is open source and available under the MIT License. 