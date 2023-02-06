import os
import sys

import pygame
import requests

SIZE = WIDTH, HEIGHT = 600, 450
FPS = 30


def do_map(x, y):
    map_request = f"https://static-maps.yandex.ru/1.x/?ll={x},{y}&spn=30,20&l=sat"

    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    return map_file


def main():
    x, y = 133.794557, -28.694111

    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    map_file = do_map(x, y)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x -= 1
                if event.key == pygame.K_RIGHT:
                    x += 1
                if event.key == pygame.K_UP:
                    y -= 1
                if event.key == pygame.K_DOWN:
                    x += 1
                map_file = do_map(x, y)

        clock.tick(FPS)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)


if __name__ == '__main__':
    main()