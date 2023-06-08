import pygame

from src.ball import Ball
from src.game_object import GameObject
from src.settings import HEIGHT, WIDTH

# from src.tile import Tile


display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("Minigolf")

ball = Ball(pygame.Rect(WIDTH // 2, HEIGHT // 2, 20, 20))

tiles: list[GameObject] = [
    # floor
    # GameObject(pygame.Rect(40, HEIGHT - 20, WIDTH - 80, 20)),
]


def main() -> None:
    run = True

    while run:
        display.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                ball.on_mouse_down()

            if event.type == pygame.MOUSEBUTTONUP:
                ball.on_mouse_up()

        for tile in tiles:
            tile.draw(display)

        ball.update(tiles)
        ball.draw(display)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
