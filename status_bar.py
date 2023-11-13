import pygame
import os
import button
from helpers import *
from constants import *
from button_data import *

def makeStatusBar(keyButtonData, keyButtonFunctionality, messageButtonData):
    keyImages = {}
    imageA = singleImage(keyButtonData[3][0])
    imageB = singleImage(keyButtonData[3][1])

    keyImages["inactive"] = imageA
    keyImages["inactiveHighlight"] = brightenImage(imageA.copy(), HIGHLIGHT_BRIGHTEN_INACTIVE)
    keyImages["active"] = imageB
    keyImages["activeHighlight"] = brightenImage(imageB.copy(), HIGHLIGHT_BRIGHTEN_INACTIVE)

    messageImages = {}
    imageC = singleImage(messageButtonData[3][0])
    imageD = singleImage(messageButtonData[3][1])

    messageImages["inactive"] = imageC
    messageImages["inactiveHighlight"] = brightenImage(imageC.copy(), HIGHLIGHT_BRIGHTEN_INACTIVE)
    messageImages["active"] = imageD
    messageImages["activeHighlight"] = brightenImage(imageD.copy(), HIGHLIGHT_BRIGHTEN_INACTIVE)

    keyButton = button.StatusBarButton(keyButtonData[0], keyButtonData[1], keyButtonData[2], keyImages, keyButtonFunctionality)
    statusBar = StatusBar(STATUS_BAR_POSITION, STATUS_BAR_SIZE, keyButton)
    messageButton = button.StatusBarButton(messageButtonData[0], messageButtonData[1], messageButtonData[2], messageImages, statusBar.toggleShowMessages)
    messageButton.isActive = True
    statusBar.addMessageButton(messageButton)

    return statusBar

class StatusBar(pygame.Surface):
    def __init__(self, position, size, keyButton):
        super().__init__(size, pygame.SRCALPHA)
        self.position = position
        self.keyButton = keyButton
        self.messageButton = None
        self.message = ""
        self.messageImage = None
        self.messageRect = None
        self.showMessage = False
        self.isShowMessages = True
        self.font = pygame.font.Font(os.path.join(*STATUS_BAR_FONT_PATH), STATUS_BAR_FONT_SIZE)

    def toggleShowMessages(self):
        self.isShowMessages = not self.isShowMessages

    def addMessageButton(self, messageButton):
        self.messageButton = messageButton

    def makeMessageImage(self):
        image = self.font.render(self.message, True, WHITISH)
        return (image, image.get_rect(center = (self.get_width() // 2, self.get_height() // 2)))
    
    def update(self, mouseState, message):
        self.showMessage = False
        
        mousePos = subtractCoords(mouseState[0], self.position)
        message += self.keyButton.update((mousePos, mouseState[1]))
        message += self.messageButton.update((mousePos, mouseState[1]))
        
        if message and self.isShowMessages:
            self.showMessage = True
            if message != self.message:
                self.message = message
                self.messageImage, self.messageRect = self.makeMessageImage()
        
    def draw(self):
        self.keyButton.draw()
        self.messageButton.draw()
        
        self.fill(STATUS_BAR_BACKGROUND)
        self.blit(self.keyButton, self.keyButton.position)
        self.blit(self.messageButton, self.messageButton.position)

        if self.showMessage:
            self.blit(self.messageImage, self.messageRect)