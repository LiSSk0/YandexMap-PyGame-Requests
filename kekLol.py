import os
import sys

import pygame
import requests

SIZE = WIDTH, HEIGHT = 800, 450
FPS = 50


def get_coords(name):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={name}&format=json"

    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        try:
            toponym = \
            json_response["response"]["GeoObjectCollection"]["featureMember"][0][
                "GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]
            return toponym_coodrinates
        except IndexError:
            print("Ошибка выполнения запроса:")
            return None

    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return None


def CheckWhereClicked(position):
    if 130 < position[0] < 200 and 20 < position[1] < 40:
        return True
    return False


def place_inputting(screen, name):
    font = pygame.font.Font(None, 27)
    pygame.draw.rect(screen, '#AE604D', (130, 20, 70, 20))
    pygame.draw.rect(screen, '#000000', (130, 20, 70, 20), 1)
    pygame.draw.rect(screen, '#AE604D', (0, 0, 200, 20))
    pygame.draw.rect(screen, '#000000', (0, 0, 200, 20), 1)
    text = font.render("find", True, '#000000')
    text2 = font.render(name, True, '#000000')
    screen.blit(text2, (10, 0))
    screen.blit(text, (150, 22))


def do_map(x, y, spn_x, spn_y):
    map_request = f"https://static-maps.yandex.ru/1.x/?ll={x},{y}&spn={spn_x},{spn_y}&l=sat&pt={x},{y},vkbkm"

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
    spn_x, spn_y = 1.7, 1.7
    if spn_x < 0 or spn_y < 0 or spn_x > 50 or spn_y > 50:
        spn_x, spn_y = 1.7, 1.7
    text = "Австралия"
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    map_file = do_map(x, y, spn_x, spn_y)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if CheckWhereClicked(mouse_position):
                    k = get_coords(text)
                    if k is not None:
                        k = k.split()
                        x, y = float(k[0]), float(k[1])
                        map_file = do_map(x, y, spn_x, spn_y)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
                if event.key == pygame.K_PAGEUP:
                    if 0 < spn_x < 0.1:
                        spn_x += 0.01
                    elif 0.1 <= spn_x < 1:
                        spn_x += 0.2
                    elif spn_x < 20:
                        spn_x += 5
                    elif spn_x * 3 < 100:
                        spn_x *= 3
                    if 0 < spn_y < 0.1:
                        spn_y += 0.01
                    elif 0.1 <= spn_y < 1:
                        spn_y += 0.2
                    elif spn_y < 20:
                        spn_y += 5
                    elif spn_y * 3 < 100:
                        spn_y *= 3
                    print(spn_x, spn_y)
                if event.key == pygame.K_PAGEDOWN:
                    spn_x *= 0.5
                    spn_y *= 0.5
                if event.key == pygame.K_LEFT:
                    x -= 1
                if event.key == pygame.K_RIGHT:
                    x += 1
                if event.key == pygame.K_UP:
                    y += 1
                if event.key == pygame.K_DOWN:
                    y -= 1
                map_file = do_map(x, y, spn_x, spn_y)
        clock.tick(FPS)
        screen.blit(pygame.image.load(map_file), (200, 0))
        place_inputting(screen, text)
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)


if __name__ == '__main__':
    main()
