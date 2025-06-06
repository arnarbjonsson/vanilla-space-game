"""
Vanilla Space Game - Main Entry Point
Simple space game with clean system architecture
"""

import arcade
from core.game_loop import GameLoop
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE


def main():
    """Main function to start the game"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_loop = GameLoop(window)
    
    # Set the game loop as the window's view
    window.show_view(game_loop)
    
    arcade.run()


if __name__ == "__main__":
    main() 