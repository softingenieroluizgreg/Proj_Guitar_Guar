import pygame
import os


class Assets:

    @staticmethod
    def image(filename):
        path = os.path.join("assets", "images", filename)
        return pygame.image.load(path).convert_alpha()

    @staticmethod
    def sound(filename):
        path = os.path.join("assets", "sounds", filename)
        return pygame.mixer.Sound(path)

    @staticmethod
    def music(filename):
        path = os.path.join("assets", "music", filename)
        return path