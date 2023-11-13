import pygame
import os
from constants import *

def subtractCoords(coordA, coordB):
    return (coordA[0] - coordB[0], coordA[1] - coordB[1])

def singleImage(pathStrings):
    return pygame.image.load(os.path.join(*pathStrings)).convert_alpha()

def dimImage(image, dimPercent):
    mask = pygame.Surface(image.get_size()).convert_alpha()
    mask.fill((0, 0, 0, (dimPercent * 255 // 100)))

    for y in range(image.get_height()):
        for x in range(image.get_width()):
            if tuple(image.get_at((x, y)))[-1] == 0:
                mask.set_at((x, y), TRANSPARENT)
    
    image.blit(mask, ORIGIN)
    return image

def brightenImage(image, brightenAmount):
    for y in range(image.get_height()):
        for x in range(image.get_width()):
            color = tuple(image.get_at((x, y)))
            if color[-1] > 0:
                image.set_at((x, y), [min(255, val + brightenAmount) for val in color])
    return image