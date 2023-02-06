import os
import sys

import pygame
import requests

SIZE = WIDTH, HEIGHT = 600, 450
x, y = 133.794557, -28.694111

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

pygame.init()
screen = pygame.display.set_mode(SIZE)
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

os.remove(map_file)