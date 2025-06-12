"""
Vanilla Space Game - Main Entry Point
Simple space game with clean system architecture
"""

# Project uses the `arcade` 2D game engine:
# - Base class: arcade.Window(width, height, title)
#     - override: on_draw(), on_update(delta_time), on_key_press(), etc.
# - Sprites: arcade.Sprite(image, scale)
#     - .center_x, .center_y, .change_x, .change_y, .update()
# - Sprite Lists: arcade.SpriteList(), .draw(), .update()
# - Drawing primitives: arcade.draw_rectangle_filled(x, y, w, h, color)
# - Input constants: arcade.key.UP, arcade.key.DOWN, etc.
# - Common methods: arcade.load_texture(), arcade.play_sound(), arcade.run()
# Docs: https://api.arcade.academy/en/stable/

import arcade
from core.game_loop import GameLoop
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE


def main():
    """Main function to start the game"""
    arcade.load_font("assets/fonts/EveSansNeue-Regular.otf")

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_loop = GameLoop(window)
    
    # Set the game loop as the window's view
    window.show_view(game_loop)
    
    arcade.run()


if __name__ == "__main__":
    main() 