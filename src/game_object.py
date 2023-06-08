import pygame

from src.settings import DEBUG


class GameObject:
    def __init__(self, rect: pygame.Rect) -> None:
        self.rect = rect
        self.velocity = pygame.Vector2(0, 0)

    def draw(self, display: pygame.Surface) -> None:
        if DEBUG:
            # Draw the hitbox
            pygame.draw.rect(display, (255, 0, 0), self.rect, 2)
