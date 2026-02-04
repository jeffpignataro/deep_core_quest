#!/usr/bin/env python3
"""
Deep Core Quest - An Incremental Mining Game
Main entry point
"""

import pygame
import sys
from src.game import Game

def main():
    """Initialize and run the game"""
    pygame.init()
    
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Error running game: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
