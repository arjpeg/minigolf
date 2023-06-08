import pygame


def clamp(number: float, min_: float, max_: float) -> float:
    """Clamp a number between a minimum and maximum value."""
    return max(min_, min(number, max_))


def collision_check(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
    """Check if two rectangles are colliding."""
    return rect1.colliderect(rect2)
