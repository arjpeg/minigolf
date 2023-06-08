import pygame
from src.game_object import GameObject


class Tile(GameObject):
    def __init__(self, rect: pygame.Rect) -> None:
        super().__init__(rect)

    def draw(self, display: pygame.Surface) -> None:
        pygame.draw.rect(display, (255, 255, 255), self.rect)
