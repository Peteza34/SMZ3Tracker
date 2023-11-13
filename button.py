import pygame
from helpers import *
from constants import *

class ButtonPanel(pygame.Surface):
    def __init__(self, position, size, buttons):
        super().__init__(size, pygame.SRCALPHA)
        self.position = position
        self.rect = self.get_rect(topleft = position)
        self.buttons = buttons

    def reset(self):
        for button in self.buttons:
            button.reset()

    def update(self, mouseState):
        status = ""
        mousePosition = subtractCoords(mouseState[0], self.position)

        for button in self.buttons:
            status += button.update([mousePosition, mouseState[1]])
            
        return status
    
    def draw(self):
        self.fill(TRANSPARENT)

        for button in self.buttons:
            button.draw()
            self.blit(button, button.position)

class AbstractButton(pygame.Surface):
    def __init__(self, name, position, size):
        super().__init__(size, pygame.SRCALPHA)
        self.name = name
        self.position = position
        self.rect = self.get_rect(topleft = position)
        self.key = ""

    def reset(self):
        pass

    def click(self, mouseState):
        pass

    def update(self, mouseState):
        pass

    def draw(self):
        pass

class SimpleButton(AbstractButton):
    def __init__(self, name, position, size, images):
        super().__init__(name, position, size)
        self.images = images
        self.isActive = False
        self.key = "inactive"

    def reset(self):
        self.isActive = False

    def click(self, mouseState):
        if mouseState[1][1]:
            self.reset()
        elif mouseState[1][0] or mouseState[1][2]:
            self.isActive = not self.isActive

    def update(self, mouseState):
        status = ""
        
        if self.isActive:
            self.key = "active"
        else:
            self.key = "inactive"
        
        if self.rect.collidepoint(mouseState[0]):
            self.key += "Highlight"
            status += self.__str__()
            if any(mouseState[1]):
                self.click(mouseState)
        
        return status
    
    def draw(self):
        self.fill(TRANSPARENT)
        self.blit(self.images[self.key], ORIGIN)

    def __str__(self):
        return self.name + ": Collected" if self.isActive else self.name + ": Not Collected"
    
class CycleButton(AbstractButton):
    def __init__(self, name, position, size, images, imageCount):
        super().__init__(name, position, size)
        self.images = images
        self.imageCount = imageCount
        self.imageIndex = 0
        self.key = "0"

    def reset(self):
        self.imageIndex = 0

    def click(self, mouseState):
        if mouseState[1][1]:
            self.reset()
        elif mouseState[1][0]:
            self.imageIndex = (self.imageIndex + 1) % self.imageCount
        elif mouseState[1][2]:
            self.imageIndex -= 1
            if self.imageIndex < 0:
                self.imageIndex = self.imageCount - 1
    
    def update(self, mouseState):
        status = ""
        self.key = str(self.imageIndex)

        if self.rect.collidepoint(mouseState[0]):
            self.key += "Highlight"
            status += self.__str__()

            if any(mouseState[1]):
                self.click(mouseState)
        
        return status
    
    def draw(self):
        self.fill(TRANSPARENT)
        self.blit(self.images[self.key], ORIGIN)

    def __str__(self):
        return self.name[self.imageIndex]

class DoubleButton(AbstractButton):
    def __init__(self, name, position, size, images):
        super().__init__(name, position, size)
        self.isActiveLeft = False
        self.isActiveRight = False
        self.images = images
        self.keyLeft = "leftInactive"
        self.keyRight = "rightInactive"

    def reset(self):
        self.isActiveLeft = self.isActiveRight = False

    def click(self, mouseState):
        if mouseState[1][1]:
            self.reset()
        elif mouseState[1][0]:
            self.isActiveLeft = not self.isActiveLeft
        elif mouseState[1][2]:
            self.isActiveRight = not self.isActiveRight
    
    def update(self, mouseState):
        status = ""

        self.keyLeft = "left"
        self.keyRight = "right"

        if self.isActiveLeft:
            self.keyLeft += "Active"
        else:
            self.keyLeft += "Inactive"

        if self.isActiveRight:
            self.keyRight += "Active"
        else:
            self.keyRight += "Inactive"

        if self.rect.collidepoint(mouseState[0]):
            self.keyLeft += "Highlight"
            self.keyRight += "Highlight"
            status += self.__str__()
            
            if any(mouseState[1]):
                self.click(mouseState)
            
        return status
    
    def draw(self):
        self.fill(TRANSPARENT)
        self.blit(self.images[self.keyLeft], ORIGIN)
        self.blit(self.images[self.keyRight], (self.rect.width // 2, self.rect.height //2))

        color = LIGHT_GRAY if self.isActiveLeft or self.isActiveRight else DARK_GRAY
        
        pygame.draw.line(self, color, (0, self.rect.height), (self.rect.width, 0))

    def __str__(self):
        left = self.name[0]
        right = self.name[1]
        
        if self.isActiveLeft:
            left += ": Collected"
        else:
            left += ": Not Collected"
        if self.isActiveRight:
            right += ": Collected"
        else:
            right += ": Not Collected"
        
        return left + ", " + right

class CounterButton(AbstractButton):
    def __init__(self, name, position, size, images, interval, maxCount):
        super().__init__(name, position, size)
        self.images = images
        self.font = pygame.font.SysFont(TRACKER_FONT_NAME, TRACKER_FONT_SIZE, True)
        self.countImage = None
        self.countImageRect = None
        self.interval = interval
        self.maxCount = maxCount
        self.count = 0
        self.key = "inactive"

    def createCountImage(self):
        foreImage = self.font.render(str(self.count), True, TRACKER_FONT_COLOR)
        backImage = self.font.render(str(self.count), True, TRACKER_FONT_BORDER_COLOR)

        countImage = pygame.Surface((foreImage.get_width() + 2 * TRACKER_FONT_BORDER, foreImage.get_height() + 2 * TRACKER_FONT_BORDER), pygame.SRCALPHA)
        countImage.blit(backImage, ORIGIN)
        countImage.blit(backImage, (TRACKER_FONT_BORDER * 2, 0))
        countImage.blit(backImage, (0, TRACKER_FONT_BORDER * 2))
        countImage.blit(backImage, (TRACKER_FONT_BORDER * 2, TRACKER_FONT_BORDER * 2))
        countImage.blit(foreImage, (TRACKER_FONT_BORDER, TRACKER_FONT_BORDER))

        countImageRect = countImage.get_rect(center = (self.get_width() - SMALL_BUTTON_SIZE // 2, self.get_height() - SMALL_BUTTON_SIZE // 2))
        if self.count >= 100:
            countImageRect.x = countImageRect.x - TRIPLE_DIGIT_OFFSET
        return (countImage, countImageRect)

    def reset(self):
        self.count = 0

    def click(self, mouseState):
        if mouseState[1][1]:
            self.reset()
        elif mouseState[1][0]:
            self.count = (self.count + self.interval) % (self.maxCount + self.interval)
        elif mouseState[1][2]:
            self.count -= self.interval
            if self.count < 0:
                self.count = self.maxCount

    def update(self, mouseState):
        status = ""
        
        if self.count > 0:
            self.key = "active"
        else:
            self.key = "inactive"

        if self.rect.collidepoint(mouseState[0]):
            self.key += "Highlight"
            status += self.__str__()

            if any(mouseState[1]):
                self.click(mouseState)
                self.countImage, self.countImageRect = self.createCountImage()
        
        return status

    def draw(self):
        self.fill(TRANSPARENT)
        self.blit(self.images[self.key], ORIGIN)
        if self.count > 0:
            self.blit(self.countImage, self.countImageRect)
    
    def __str__(self):
        return self.name + " Count: " + str(self.count)
    
class KeyButton(CounterButton):
    def __init__(self, name, position, size, images, interval, maxCount):
        super().__init__(name, position, size, images, interval, maxCount)
        self.countImage, self.countImageRect = self.createCountImage()
    
    def draw(self):
        self.fill(TRANSPARENT)
        self.blit(self.images[self.key], ORIGIN)
        self.blit(self.countImage, self.countImageRect)

class BowButton(AbstractButton):
    def __init__(self, name, position, size, images):
        super().__init__(name, position, size)
        self.images = images
        self.key = "inactive"
        self.silverKey = "silvers"
        self.isActive = False
        self.isSilvers = False

    def reset(self):
        self.isActive = self.isSilvers = False

    def click(self, mouseState):
        if mouseState[1][1]:
            self.reset()
        elif mouseState[1][0]:
            self.isActive = not self.isActive
        elif mouseState[1][2]:
            self.isSilvers = not self.isSilvers
    
    def update(self, mouseState):
        status = ""

        self.silverKey = "silvers"

        if self.isActive:
            self.key = "active"
        else:
            self.key = "inactive"
        
        if self.rect.collidepoint(mouseState[0]):
            self.key += "Highlight"
            self.silverKey += "Highlight"
            status += self.__str__()

            if any(mouseState[1]):
                self.click(mouseState)
        
        return status
    
    def draw(self):
        self.fill(TRANSPARENT)
        self.blit(self.images[self.key], ORIGIN)
        if self.isSilvers:
            self.blit(self.images[self.silverKey], ORIGIN)
    
    def __str__(self):
        bow = "Bow: Collected" if self.isActive else "Bow: Not Collected"
        silvers = "Silvers: Collected" if self.isSilvers else "Silvers: Not Collected"
        return bow + ", " + silvers

class LocationButton(AbstractButton):
    def __init__(self, name, position, size, initials, foreButtons, backButton = None):
        super().__init__(name, position, size)
        self.initials = initials
        self.images = self.makeInitialsImages(initials)
        self.foreButtons = foreButtons
        self.backButton = backButton
        self.key = "initials"

    def makeInitialsImages(self, initials):
        images = {}
        fontA = pygame.font.SysFont(TRACKER_FONT_NAME, INITIALS_FONT_SIZE)
        fontB = pygame.font.SysFont(TRACKER_FONT_NAME, INITIALS_FONT_SIZE, True)

        imageA = pygame.Surface((SMALL_BUTTON_SIZE, SMALL_BUTTON_SIZE), pygame.SRCALPHA)
        imageB = imageA.copy()
        
        initialA = fontA.render(initials, True, WHITE)
        initialB = fontB.render(initials, True, WHITE)
        backA = fontA.render(initials, True, BLACK)
        backB = fontB.render(initials, True, BLACK)
        
        positionA = initialA.get_rect(center = (SMALL_BUTTON_SIZE // 2, SMALL_BUTTON_SIZE // 2)).topleft
        positionB = initialB.get_rect(center = (SMALL_BUTTON_SIZE // 2, SMALL_BUTTON_SIZE // 2)).topleft
        
        imageA.blit(backA, (positionA[0] - TRACKER_FONT_BORDER, positionA[1] - TRACKER_FONT_BORDER))
        imageA.blit(backA, (positionA[0] - TRACKER_FONT_BORDER, positionA[1] + TRACKER_FONT_BORDER))
        imageA.blit(backA, (positionA[0] + TRACKER_FONT_BORDER, positionA[1] - TRACKER_FONT_BORDER))
        imageA.blit(backA, (positionA[0] + TRACKER_FONT_BORDER, positionA[1] + TRACKER_FONT_BORDER))
        imageA.blit(initialA, positionA)
        
        imageB.blit(backB, (positionB[0] - TRACKER_FONT_BORDER, positionB[1] - TRACKER_FONT_BORDER))
        imageB.blit(backB, (positionB[0] - TRACKER_FONT_BORDER, positionB[1] + TRACKER_FONT_BORDER))
        imageB.blit(backB, (positionB[0] + TRACKER_FONT_BORDER, positionB[1] - TRACKER_FONT_BORDER))
        imageB.blit(backB, (positionB[0] + TRACKER_FONT_BORDER, positionB[1] + TRACKER_FONT_BORDER))
        imageB.blit(initialB, positionB)
        
        images["initials"] = imageA
        images["initialsHighlight"] = imageB
        
        return images

    def reset(self):
        if self.backButton:
            self.backButton.reset()
        for button in self.foreButtons:
            button.reset()

    def update(self, mouseState):
        status = ""
        self.key = "initials"
        mousePosition = subtractCoords(mouseState[0], self.position)
        
        if self.rect.collidepoint(mouseState[0]):
            self.key += "Highlight"
            status += self.__str__()

        for button in self.foreButtons:
            status += button.update([mousePosition, mouseState[1]])
            if button.rect.collidepoint(mousePosition):
                mousePosition = (-1, -1)
                mouseState[1] = (False, False, False)

        if self.backButton:
            status += self.backButton.update((mousePosition, mouseState[1]))

        return status
    
    def draw(self):
        self.fill(TRANSPARENT)
        if self.backButton:
            self.backButton.draw()
            self.blit(self.backButton, self.backButton.position)
        for button in self.foreButtons:
            button.draw()
            self.blit(button, button.position)
        self.blit(self.images[self.key], ORIGIN)
    
    def __str__(self):
        return self.name + " - "

class ChestButton(CounterButton):
    def __init__(self, name, position, size, images, interval, maxCount):
        super().__init__(name, position, size, images, interval, maxCount)
        self.count = maxCount
        self.font = pygame.font.SysFont(TRACKER_FONT_NAME, LARGE_CHEST_FONT_SIZE if size[0] == LARGE_BUTTON_SIZE else SMALL_CHEST_FONT_SIZE, True)
        self.countImage, self.countImageRect = self.createCountImage()

    def createCountImage(self):
        image = self.font.render(str(self.count), True, CHEST_FONT_COLOR)
        return (image, image.get_rect(center = (self.get_width() // 2, self.get_height() // 2 + LARGE_CHEST_Y_OFFSET if self.get_height() == LARGE_BUTTON_SIZE else self.get_height() // 2 + SMALL_CHEST_Y_OFFSET)))
    
    def reset(self):
        self.count = self.maxCount

    def click(self, mouseState):
        if mouseState[1][1]:
            self.reset()
        elif mouseState[1][2]:
            self.count += self.interval
            if self.count > self.maxCount:
                self.count = 0
        elif mouseState[1][0]:
            self.count -= self.interval
            if self.count < 0:
                self.count = self.maxCount
    
    def __str__(self):
        return "Item Count: " + str(self.count)

class GoalButton(CounterButton):
    def __init__(self, name, position, size, images, interval, maxCount):
        super().__init__(name, position, size, images, interval, maxCount)
        self.count = maxCount
        self.countImage, self.countImageRect = self.createCountImage()

    def createCountImage(self):
        foreImage = self.font.render("?" if self.count == self.maxCount else str(self.count), True, TRACKER_FONT_COLOR)
        backImage = self.font.render("?" if self.count == self.maxCount else str(self.count), True, TRACKER_FONT_BORDER_COLOR)

        countImage = pygame.Surface((foreImage.get_width() + 2 * TRACKER_FONT_BORDER, foreImage.get_height() + 2 * TRACKER_FONT_BORDER), pygame.SRCALPHA)
        countImage.blit(backImage, ORIGIN)
        countImage.blit(backImage, (TRACKER_FONT_BORDER * 2, 0))
        countImage.blit(backImage, (0, TRACKER_FONT_BORDER * 2))
        countImage.blit(backImage, (TRACKER_FONT_BORDER * 2, TRACKER_FONT_BORDER * 2))
        countImage.blit(foreImage, (TRACKER_FONT_BORDER, TRACKER_FONT_BORDER))

        countImageRect = countImage.get_rect(center = (self.get_width() * .75, self.get_height() * .75))

        return (countImage, countImageRect)
    
    def reset(self):
        self.count = self.maxCount

    def draw(self):
        self.fill(TRANSPARENT)
        self.blit(self.images[self.key], ORIGIN)
        self.blit(self.countImage, self.countImageRect)

    def __str__(self):
        return self.name + ": Unknown" if self.count == self.maxCount else self.name + ": " + str(self.count)

class StatusBarButton(SimpleButton):
    def __init__(self, name, position, size, images, functionality):
        super().__init__(name, position, size, images)
        self.functionality = functionality

    def click(self, mouseState):
        if mouseState[1][0]:
            self.isActive = not self.isActive
            self.functionality()

    def __str__(self):
        return self.name
    
class BossButton(SimpleButton):
    def __init__(self, name, position, size, images):
        super().__init__(name, position, size, images)
    
    def __str__(self):
        return "Boss Defeated" if self.isActive else "Boss Not Defeated"