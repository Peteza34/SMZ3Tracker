import os
import pygame
import button_factory
import status_bar
import panelManager
from button_data import *
from helpers import *
from constants import *

pygame.init()

os.environ["SDL_MOUSE_FOCUS_CLICKTHROUGH"] = "1"

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption(TITLE)
pygame.display.set_icon(singleImage(ICON_PATH))

_panelManager = panelManager.PanelManager(WIN.get_size())
_panelManager.addPanel(button_factory.makeButtonPanel(ALTTP_PANEL_DATA, LARGE_BUTTON_SIZE, BUTTON_SPACING))
_panelManager.addPanel(button_factory.makeButtonPanel(SM_PANEL_DATA_1, LARGE_BUTTON_SIZE, BUTTON_SPACING))
_panelManager.addPanel(button_factory.makeButtonPanel(SM_PANEL_DATA_2, LARGE_BUTTON_SIZE, BUTTON_SPACING))
_panelManager.addPanel(button_factory.makeButtonPanel(ALTTP_LOCATION_PANEL_A, LARGE_BUTTON_SIZE, BUTTON_SPACING))
_panelManager.addPanel(button_factory.makeChestPanel(LARGE_CHEST_PANEL_A, LARGE_BUTTON_SIZE, BUTTON_SPACING), isKeyPanel = False)
_panelManager.addPanel(button_factory.makeALTTPKeysanityPanel(ALTTP_KEYSANITY_PANEL_A, LARGE_BUTTON_SIZE, BUTTON_SPACING), isNonKeyPanel = False)
_panelManager.addPanel(button_factory.makeButtonPanel(ALTTP_LOCATION_PANEL_B, LARGE_BUTTON_SIZE, BUTTON_SPACING))
_panelManager.addPanel(button_factory.makeChestPanel(LARGE_CHEST_PANEL_B, LARGE_BUTTON_SIZE, BUTTON_SPACING), isKeyPanel = False)
_panelManager.addPanel(button_factory.makeALTTPKeysanityPanel(ALTTP_KEYSANITY_PANEL_B, LARGE_BUTTON_SIZE, BUTTON_SPACING), isNonKeyPanel = False)
_panelManager.addPanel(button_factory.makeButtonPanel(SM_LOCATION_PANEL, LARGE_BUTTON_SIZE, BUTTON_SPACING))
_panelManager.addPanel(button_factory.makeSMKeysanityPanel(SM_KEYSANITY_PANEL, LARGE_BUTTON_SIZE, BUTTON_SPACING), isNonKeyPanel = False)
_panelManager.addPanel(button_factory.makeButtonPanel(GOAL_PANEL, LARGE_BUTTON_SIZE, BUTTON_SPACING))
_panelManager.addStatusBar(status_bar.makeStatusBar(KEY_BUTTON, _panelManager.toggleKeysanity, MESSAGE_BUTTON))

def main():
    clock = pygame.time.Clock()
    mouse = pygame.mouse
    isRunning = True

    while(isRunning):
        clock.tick(FPS)
        mouseState = [mouse.get_pos(), (False, False, False)]
        
        if not mouse.get_focused():
            mouseState[0] = (-1, -1)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseState[1] = mouse.get_pressed()

        _panelManager.update(mouseState)

        _panelManager.draw()

        WIN.fill(TRANSPARENT)
        WIN.blit(_panelManager, ORIGIN)

        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()