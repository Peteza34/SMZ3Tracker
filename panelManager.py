import pygame
from constants import *

class PanelManager(pygame.Surface):
    def __init__(self, size):
        super().__init__(size, pygame.SRCALPHA)
        self.nonKeyPanels = []
        self.keyPanels = []
        self.isKeysanity = False
        self.statusBar = None

    def addPanel(self, panel, isNonKeyPanel = True, isKeyPanel = True):
        if isNonKeyPanel:
            self.nonKeyPanels.append(panel)
        if isKeyPanel:
            self.keyPanels.append(panel)

    def addStatusBar(self, statusBar):
        self.statusBar = statusBar

    def toggleKeysanity(self):
        self.isKeysanity = not self.isKeysanity
        return self.isKeysanity
    
    def reset(self):
        for panel in set(self.keyPanels + self.nonKeyPanels):
            panel.reset()

    def update(self, mouseState):
        message = ""
        if self.isKeysanity:
            for panel in self.keyPanels:
                message += panel.update(mouseState)
        else:
            for panel in self.nonKeyPanels:
                message += panel.update(mouseState)

        self.statusBar.update(mouseState, message)

    def draw(self):
        self.fill(TRANSPARENT)
        if self.isKeysanity:
            for panel in self.keyPanels:
                panel.draw()
                self.blit(panel, panel.position)
        else:
            for panel in self.nonKeyPanels:
                panel.draw()
                self.blit(panel, panel.position)
        
        self.statusBar.draw()
        self.blit(self.statusBar, self.statusBar.position)