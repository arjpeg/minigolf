import math
from typing import Literal
import pygame

from src.game_object import GameObject
from src.utils import clamp
from src.settings import FRICTION_FACTOR, GRAVITY, HEIGHT, WIDTH


class Ball(GameObject):
    def __init__(self, rect: pygame.Rect) -> None:
        self.rect = rect
        self.velocity = pygame.Vector2(0, 0)
        self.grounded = False

        self._start_click_pos = pygame.Vector2(0, 0)
        self._in_drag_state = False

        self.can_jump = False

    def draw(self, display: pygame.Surface) -> None:
        super().draw(display)

        pygame.draw.circle(
            display, (255, 255, 255), self.rect.center, self.rect.width // 2
        )
        # pygame.draw.rect(display, (255, 255, 255), self.rect)

    def update(self, tiles: list[GameObject]) -> None:
        # Update the velocity
        self.velocity.x *= FRICTION_FACTOR
        self.velocity.y += GRAVITY if not self.grounded else 0

        # Don't let the velocity get too high
        self.velocity.x = clamp(self.velocity.x, -40, 40)
        self.velocity.y = clamp(self.velocity.y, -50, 40)

        if abs(self.velocity.x) < 0.1:
            self.velocity.x = 0

        if abs(self.velocity.y) < 0.1:
            self.velocity.y = 0

        self.rect.x += self.velocity.x  # type: ignore
        x_col = self.fix_position(tiles, "x")[0]

        self.rect.y += int(self.velocity.y)
        y_col = self.fix_position(tiles, "y")[1]

        if not y_col:
            self.grounded = False
        else:
            self.grounded = True
            self.velocity.y = -abs(self.velocity.y)
            self.can_jump = True

    def fix_position(
        self, tiles: list[GameObject], axis: Literal["x"] | Literal["y"]
    ) -> tuple[bool, bool]:
        tiles = [
            *tiles,
            GameObject(pygame.Rect(0, 0, WIDTH, 1)),
            GameObject(pygame.Rect(-30, 0, 30, HEIGHT)),
            GameObject(pygame.Rect(0, HEIGHT, WIDTH, 30)),
            GameObject(pygame.Rect(WIDTH, 0, 30, HEIGHT + 30)),
        ]

        collisions = [tile for tile in tiles if tile.rect.colliderect(self.rect)]

        collision_occured = [False, False]

        if axis == "x":
            for tile in collisions:
                collision = self.velocity.x != 0

                if self.velocity.x < 0:
                    self.rect.left = tile.rect.right

                elif self.velocity.x > 0:
                    self.rect.right = tile.rect.left

                if collision:
                    self.velocity.x *= -0.4
                    collision_occured[0] = True

        elif axis == "y":
            for tile in collisions:
                collision = self.velocity.y != 0

                if self.velocity.y < 0:
                    self.rect.top = tile.rect.bottom
                elif self.velocity.y > 0:
                    self.rect.bottom = tile.rect.top

                if collision:
                    self.velocity.y *= -0.4
                    collision_occured[1] = True

        return tuple(collision_occured)

    def on_mouse_down(self) -> None:
        self._start_click_pos = pygame.Vector2(pygame.mouse.get_pos())
        self._in_drag_state = True

    def on_mouse_up(self) -> None:
        if not self.can_jump:
            return

        self._in_drag_state = False

        start_click_pos = self._start_click_pos
        end_click_pos = pygame.Vector2(pygame.mouse.get_pos())

        _current_window = pygame.display.get_surface()

        pygame.draw.line(
            _current_window,
            (255, 255, 255),
            start_click_pos,
            end_click_pos,
            2,
        )

        magnitude = (start_click_pos - end_click_pos).magnitude()
        angle = (start_click_pos - end_click_pos).angle_to(pygame.Vector2(1, 0))

        self.velocity.x += math.cos(math.radians(angle)) * magnitude / 10
        self.velocity.y += math.sin(math.radians(angle)) * -magnitude / 7

        self._start_click_pos = pygame.Vector2(0, 0)
        self.can_jump = False
