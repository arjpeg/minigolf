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

        print(
            "init",
            f"{self.grounded=} (added {GRAVITY if not self.grounded else 0})",
            f"{self.velocity=}",
        )

        # Don't let the velocity get too high
        self.velocity.x = clamp(self.velocity.x, -40, 40)
        self.velocity.y = clamp(self.velocity.y, -50, 40)

        print("after boundary check", f"{self.grounded=}", f"{self.velocity=}")

        if abs(self.velocity.x) < 0.1:
            self.velocity.x = 0

        if abs(self.velocity.y) < 0.1:
            self.velocity.y = 0

        self.rect.x += self.velocity.x  # type: ignore
        # self.fix_position(tiles, "x")

        self.rect.y += int(self.velocity.y)

        _, y_ground_col = self.move_in_bounds()

        # tile_collision = self.fix_position(tiles, "y")
        tile_collision = False

        print(y_ground_col, tile_collision)

        if not y_ground_col and not tile_collision:
            self.grounded = False
        elif tile_collision or y_ground_col:
            self.grounded = True
            self.velocity.y = -abs(self.velocity.y)
            self.can_jump = True

        print(self.velocity, "\n")

    def move_in_bounds(self) -> tuple[int, int]:
        res = [False, False]

        if self.rect.x <= 0 or self.rect.right >= WIDTH:
            self.velocity.x *= -0.4
            self.rect.x = clamp(self.rect.x, 0, WIDTH - self.rect.width)  # type: ignore
            res[0] = True

        if self.rect.bottom >= HEIGHT - 1:
            self.rect.y = HEIGHT - self.rect.height
            self.velocity.y *= -0.4
            print(f"reduce velocity by * 0.4 (now: {self.velocity.y=})")

            res[1] = True

        print(
            "in boundary check",
            f"{self.velocity=}, {self.rect.bottom} >= {HEIGHT}",
        )

        return tuple(res)

    def fix_position(
        self, tiles: list[GameObject], axis: Literal["x"] | Literal["y"]
    ) -> bool:
        collisions = [tile for tile in tiles if tile.rect.colliderect(self.rect)]

        is_grounded = False

        if axis == "x":
            for tile in collisions:
                if self.velocity.x < 0:
                    self.rect.left = tile.rect.right
                elif self.velocity.x > 0:
                    self.rect.right = tile.rect.left

        elif axis == "y":
            for tile in collisions:
                if self.velocity.y < 0:
                    self.rect.top = tile.rect.bottom
                elif self.velocity.y > 0:
                    self.rect.bottom = tile.rect.top
                    is_grounded = True

        return is_grounded

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

        print(
            "after mouse up\n",
            f"{self.velocity=}",
            f"{magnitude=}",
            f"{angle=}",
        )

        self._start_click_pos = pygame.Vector2(0, 0)
        self.can_jump = False
