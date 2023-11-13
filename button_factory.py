import pygame
import button
import math
from constants import *
from helpers import *

def makeSimpleButton(position, size, name, paths, isBoss = False):
    images = {}
    
    imageA = singleImage(paths)

    images["active"] = imageA
    images["activeHighlight"] = brightenImage(imageA.copy(), HIGHLIGHT_BRIGHTEN)
    
    imageDim = dimImage(imageA.copy(), DIM_PERCENT)
    images["inactive"] = imageDim
    images["inactiveHighlight"] = brightenImage(imageDim.copy(), HIGHLIGHT_BRIGHTEN_INACTIVE)

    if isBoss:
        return button.BossButton(name, position, size, images)
    else:
        return button.SimpleButton(name, position, size, images)

def makeBowButton(position, size, name, paths):
    images = {}

    imageA = singleImage(paths[0])
    imageSilvers = singleImage(paths[1])

    images["active"] = imageA
    images["activeHighlight"] = brightenImage(imageA.copy(), HIGHLIGHT_BRIGHTEN)
    images["silvers"] = imageSilvers
    images["silversHighlight"] = brightenImage(imageSilvers.copy(), HIGHLIGHT_BRIGHTEN)

    imageDim = dimImage(imageA.copy(), DIM_PERCENT)
    images["inactive"] = imageDim
    images["inactiveHighlight"] = brightenImage(imageDim.copy(), HIGHLIGHT_BRIGHTEN_INACTIVE)

    return button.BowButton(name, position, size, images)

def makeDoubleButton(position, size, name, paths):
    images = {}

    imageLeft = singleImage(paths[0])
    imageRight = singleImage(paths[1])

    images["leftActive"] = imageLeft
    images["leftActiveHighlight"] = brightenImage(imageLeft.copy(), HIGHLIGHT_BRIGHTEN)
    images["rightActive"] = imageRight
    images["rightActiveHighlight"] = brightenImage(imageRight.copy(), HIGHLIGHT_BRIGHTEN)

    imageDimLeft = dimImage(imageLeft.copy(), DIM_PERCENT)
    imageDimRight = dimImage(imageRight.copy(), DIM_PERCENT)

    images["leftInactive"] = imageDimLeft
    images["leftInactiveHighlight"] = brightenImage(imageDimLeft.copy(), HIGHLIGHT_BRIGHTEN_INACTIVE)
    images["rightInactive"] = imageDimRight
    images["rightInactiveHighlight"] = brightenImage(imageDimRight.copy(), HIGHLIGHT_BRIGHTEN_INACTIVE)
    
    return button.DoubleButton(name, position, size, images)

def makeCycleButton(position, size, name, paths, hasDimImage = True):
    images = {}
    imagesTemp = []

    for path in paths:
        imagesTemp.append(singleImage(path))
    
    if hasDimImage:
        imageDim = dimImage(imagesTemp[0].copy(), DIM_PERCENT)
        imagesTemp.insert(0, imageDim)

    for i in range(len(imagesTemp)):
        images[str(i)] = imagesTemp[i]
        images[str(i) + "Highlight"] = brightenImage(imagesTemp[i].copy(), HIGHLIGHT_BRIGHTEN_INACTIVE if i == 0 and hasDimImage else HIGHLIGHT_BRIGHTEN)

    return button.CycleButton(name, position, size, images, len(imagesTemp))
    
def makeCounterButton(position, size, name, paths, interval, maxCount, hasDimImage = True):
    images = {}

    imageA = singleImage(paths)
    
    images["active"] = imageA
    images["activeHighlight"] = brightenImage(imageA.copy(), HIGHLIGHT_BRIGHTEN)

    if hasDimImage:
        imageDim = dimImage(imageA.copy(), DIM_PERCENT)

        images["inactive"] = imageDim
        images["inactiveHighlight"] = brightenImage(imageDim.copy(), HIGHLIGHT_BRIGHTEN_INACTIVE)

    else:
        images["inactive"] = images["active"]
        images["inactiveHighlight"] = images["activeHighlight"]

    return button.CounterButton(name, position, size, images, interval, maxCount)

def makeGoalButton(position, size, name, paths, interval, maxCount):
    images = {}

    imageA = singleImage(paths)

    images["active"] = imageA
    images["activeHighlight"] = brightenImage(imageA.copy(), HIGHLIGHT_BRIGHTEN)
    images["inactive"] = images["active"]
    images["inactiveHighlight"] = images["activeHighlight"]

    return button.GoalButton(name, position, size, images, interval, maxCount)

def makeGoalCycleButton(position, size, name, text):
    images = {}
    font = pygame.font.SysFont(TRACKER_FONT_NAME, INITIALS_FONT_SIZE, False)
    highlightFont = pygame.font.SysFont(TRACKER_FONT_NAME, INITIALS_FONT_SIZE, True)

    for i in range(len(text)):
        imageA = pygame.Surface(size, pygame.SRCALPHA)
        imageB = imageA.copy()

        imageAT = font.render(text[i], True, WHITE)
        imageBT = highlightFont.render(text[i], True, WHITE)

        imageA.blit(imageAT, imageAT.get_rect(center = (size[0] // 2, size[1] // 2)))
        imageB.blit(imageBT, imageBT.get_rect(center = (size[0] // 2, size[1] // 2)))

        images[str(i)] = imageA
        images[str(i) + "Highlight"] = imageB

    return button.CycleButton(name, position, size, images, len(text))

def makeLocationButton(position, size, name, initials, backButtonData, foreButtonData):
    backButton = None
    foreButtons = []

    if backButtonData and backButtonData[0] == "SimpleButton":
        backButton = makeSimpleButton(backButtonData[1], backButtonData[2], backButtonData[3], backButtonData[4], True)

    for foreButton in foreButtonData:
        if foreButton[0] == "CycleButton":
            foreButtons.append(makeCycleButton(foreButton[1], foreButton[2], foreButton[3], foreButton[4], foreButton[5]))
        elif foreButton[0] == "SimpleButton":
            foreButtons.append(makeSimpleButton(foreButton[1], foreButton[2], foreButton[3], foreButton[4]))
    
    return button.LocationButton(name, position, size, initials, foreButtons, backButton)

def makeButtonPanel(buttonPanelData, gridSize, buttonSpacing):
    buttons = []
    panelSize = (buttonPanelData[0][0] * (gridSize + buttonSpacing) - buttonSpacing, buttonPanelData[0][1] * (gridSize + buttonSpacing) - buttonSpacing)
    panelPosition = (buttonPanelData[1])
    
    for buttonData in buttonPanelData[2]:
        buttonPosition = (buttonData[1][0] * gridSize + math.floor(buttonData[1][0]) * buttonSpacing, buttonData[1][1] * gridSize + math.floor(buttonData[1][1]) * buttonSpacing)
        if buttonData[0] == "SimpleButton":
            buttons.append(makeSimpleButton(buttonPosition, buttonData[2], buttonData[3], buttonData[4]))
        elif buttonData[0] == "DoubleButton":
            buttons.append(makeDoubleButton(buttonPosition, buttonData[2], buttonData[3], buttonData[4]))
        elif buttonData[0] == "CounterButton":
            buttons.append(makeCounterButton(buttonPosition, buttonData[2], buttonData[3], buttonData[4], buttonData[6], buttonData[7], buttonData[5]))
        elif buttonData[0] == "CycleButton":
            buttons.append(makeCycleButton(buttonPosition, buttonData[2], buttonData[3], buttonData[4], buttonData[5]))
        elif buttonData[0] == "BowButton":
            buttons.append(makeBowButton(buttonPosition, buttonData[2], buttonData[3], buttonData[4]))
        elif buttonData[0] == "LocationButton":
            buttons.append(makeLocationButton(buttonPosition, buttonData[2], buttonData[3], buttonData[4], buttonData[5], buttonData[6]))
        elif buttonData[0] == "GoalButton":
            buttons.append(makeGoalButton(buttonPosition, buttonData[2], buttonData[3], buttonData[4], buttonData[5], buttonData[6]))
        elif buttonData[0] == "GoalCycleButton":
            buttons.append(makeGoalCycleButton(buttonPosition, buttonData[2], buttonData[3], buttonData[4]))

    return button.ButtonPanel(panelPosition, panelSize, buttons)  

def makeChestPanel(chestPanelData, gridSize, buttonSpacing):
    buttons = []
    panelSize = (chestPanelData[0][0] * (gridSize + buttonSpacing) - buttonSpacing, chestPanelData[0][1] * (gridSize + buttonSpacing) - buttonSpacing)
    panelPosition = chestPanelData[1]

    imageA = singleImage(chestPanelData[2][0])
    imageB = singleImage(chestPanelData[2][1])

    chestImages = {}
    chestImages["inactive"] = imageA
    chestImages["inactiveHighlight"] = brightenImage(imageA.copy(), HIGHLIGHT_BRIGHTEN)
    chestImages["active"] = imageB
    chestImages["activeHighlight"] = brightenImage(imageB.copy(), HIGHLIGHT_BRIGHTEN)
    i = 0

    for x in range(chestPanelData[0][0]):
        for y in range(chestPanelData[0][1]):
            buttonPosition = (x * (gridSize + buttonSpacing), y * (gridSize + buttonSpacing))
            itemCount = chestPanelData[3][i]
            buttons.append(button.ChestButton("Item Count", buttonPosition, (gridSize, gridSize), chestImages, 1, itemCount))
            i += 1

    return button.ButtonPanel(panelPosition, panelSize, buttons)

def makeALTTPKeysanityPanel(keysanityPanelData, gridSize, buttonSpacing):
    buttons = []
    panelSize = (keysanityPanelData[0][0] * (gridSize + buttonSpacing) - buttonSpacing, keysanityPanelData[0][1] * (gridSize + buttonSpacing) - buttonSpacing)
    panelPosition = keysanityPanelData[1]

    chestImageA = singleImage(keysanityPanelData[2][0])
    chestImageB = singleImage(keysanityPanelData[2][1])
    bigKeyImage = singleImage(keysanityPanelData[3])
    bigKeyImageInactive = dimImage(bigKeyImage.copy(), DIM_PERCENT)
    smallKeyImage = singleImage(keysanityPanelData[4])
    
    chestImages = {}
    chestImages["inactive"] = chestImageA
    chestImages["inactiveHighlight"] = brightenImage(chestImageA.copy(), HIGHLIGHT_BRIGHTEN)
    chestImages["active"] = chestImageB
    chestImages["activeHighlight"] = brightenImage(chestImageB.copy(), HIGHLIGHT_BRIGHTEN)

    bigKeyImages = {}
    bigKeyImages["inactive"] = bigKeyImageInactive
    bigKeyImages["inactiveHighlight"] = brightenImage(bigKeyImageInactive.copy(), HIGHLIGHT_BRIGHTEN_INACTIVE)
    bigKeyImages["active"] = bigKeyImage
    bigKeyImages["activeHighlight"] = brightenImage(bigKeyImage.copy(), HIGHLIGHT_BRIGHTEN)

    smallKeyImages = {}
    smallKeyImages["inactive"] = smallKeyImage
    smallKeyImages["inactiveHighlight"] = brightenImage(smallKeyImage.copy(), HIGHLIGHT_BRIGHTEN)
    smallKeyImages["active"] = smallKeyImages["inactive"]
    smallKeyImages["activeHighlight"] = smallKeyImages["inactiveHighlight"]

    i = 0

    for x in range(keysanityPanelData[0][0]):
        for y in range(keysanityPanelData[0][1]):
            buttonPosition = (x * (gridSize + buttonSpacing), y * (gridSize + buttonSpacing))
            itemCount = keysanityPanelData[5][i][0]
            keyCount = keysanityPanelData[5][i][1]
            smallButtons = []

            smallButtons.append(button.ChestButton("Item", ORIGIN, (SMALL_BUTTON_SIZE, SMALL_BUTTON_SIZE), chestImages, 1, itemCount))
            smallButtons.append(button.SimpleButton("Big Key", (SMALL_BUTTON_SIZE, 0), (SMALL_BUTTON_SIZE, SMALL_BUTTON_SIZE), bigKeyImages))
            smallButtons.append(button.KeyButton("Small Key", (0, SMALL_BUTTON_SIZE), (LARGE_BUTTON_SIZE, SMALL_BUTTON_SIZE), smallKeyImages, 1, keyCount))

            buttons.append(button.ButtonPanel(buttonPosition, (LARGE_BUTTON_SIZE, LARGE_BUTTON_SIZE), smallButtons))

            i += 1
    
    return button.ButtonPanel(panelPosition, panelSize, buttons)

def makeSMKeysanityPanel(panelData, gridSize, buttonSpacing):
    buttons = []
    panelSize = (panelData[0][0] * (gridSize + buttonSpacing) - buttonSpacing, panelData[0][1] * (gridSize + buttonSpacing) - buttonSpacing)
    panelPosition = panelData[1]

    for entry in panelData[2]:
        buttonPosition = (entry[1][0] * gridSize + math.floor(entry[1][0]) * buttonSpacing, entry[1][1] * gridSize + math.floor(entry[1][1]) * buttonSpacing)
        buttonSize = entry[2]

        if entry[0] == "LocationButton":
            buttons.append(makeLocationButton(buttonPosition, buttonSize, entry[3], entry[4], entry[5], entry[6]))

    chestImageA = singleImage(panelData[3][0][0])
    chestImageB = singleImage(panelData[3][0][1])
    bigKeyImage = singleImage(panelData[3][1])
    bigKeyImageInactive = dimImage(bigKeyImage.copy(), DIM_PERCENT)
    smallKeyImage = singleImage(panelData[3][2])

    chestImages = {}
    chestImages["inactive"] = chestImageA
    chestImages["inactiveHighlight"] = brightenImage(chestImageA.copy(), HIGHLIGHT_BRIGHTEN)
    chestImages["active"] = chestImageB
    chestImages["activeHighlight"] = brightenImage(chestImageB.copy(), HIGHLIGHT_BRIGHTEN)

    bigKeyImages = {}
    bigKeyImages["inactive"] = bigKeyImageInactive
    bigKeyImages["inactiveHighlight"] = brightenImage(bigKeyImageInactive.copy(), HIGHLIGHT_BRIGHTEN_INACTIVE)
    bigKeyImages["active"] = bigKeyImage
    bigKeyImages["activeHighlight"] = brightenImage(bigKeyImage.copy(), HIGHLIGHT_BRIGHTEN)

    smallKeyImages = {}
    smallKeyImages["inactive"] = smallKeyImage
    smallKeyImages["inactiveHighlight"] = brightenImage(smallKeyImage.copy(), HIGHLIGHT_BRIGHTEN)
    smallKeyImages["active"] = smallKeyImages["inactive"]
    smallKeyImages["activeHighlight"] = smallKeyImages["inactiveHighlight"]

    for entry in panelData[4]:
        gtButtons = []
        buttonPosition = (entry[0][0] * gridSize + math.floor(entry[0][0]) * buttonSpacing, entry[0][1] * gridSize + math.floor(entry[0][1]) * buttonSpacing)
        buttonSize = entry[1]

        gtButtons.append(button.ChestButton("Item Count", (0, SMALL_BUTTON_SIZE), (SMALL_BUTTON_SIZE, SMALL_BUTTON_SIZE), chestImages, 1, entry[4]))
        gtButtons.append(button.SimpleButton("Big Key", (SMALL_BUTTON_SIZE, 0), (SMALL_BUTTON_SIZE, SMALL_BUTTON_SIZE), bigKeyImages))
        gtButtons.append(button.KeyButton("Small Key", (SMALL_BUTTON_SIZE, SMALL_BUTTON_SIZE), (SMALL_BUTTON_SIZE, SMALL_BUTTON_SIZE), smallKeyImages, 1, entry[5]))

        buttons.append(button.LocationButton(entry[2], buttonPosition, buttonSize, entry[3], gtButtons, None))

    for entry in panelData[5]:
        foreButtons = []
        buttonPosition = (entry[0][0] * gridSize + math.floor(entry[0][0]) * buttonSpacing, entry[0][1] * gridSize + math.floor(entry[0][1]) * buttonSpacing)
        buttonSize = entry[1]

        foreButtons.append(button.KeyButton("Small Key", (SMALL_BUTTON_SIZE, 0), (SMALL_BUTTON_SIZE, SMALL_BUTTON_SIZE), smallKeyImages, 1, entry[4]))

        buttons.append(button.LocationButton(entry[2], buttonPosition, buttonSize, entry[3], foreButtons, None))
    
    return button.ButtonPanel(panelPosition, panelSize, buttons)