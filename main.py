#!/usr/bin/python3

import pygame
import random
import time
from Game.Game import Arena

def main():
    game = Arena()
    # Start game
    game.loop()
    pygame.quit()

if __name__ == "__main__":
    main()