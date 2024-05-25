from ST7735 import TFT
from sysfont import sysfont
from machine import SPI,Pin
import joystickcontrol
import time
import math
import random
spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11), miso=None)
tft=TFT(spi,16,17,18)
tft.initr()
tft.rgb(True)


map = [[0 for _ in range(16)] for _ in range(16)]
sneko = [(7,6), (7,7), (7,8), (7,9)]
nextLetter = 0


def wait(t):
    time.sleep_ms(t)

def clearAll():
    tft.fill(TFT.BLACK)

def drawEmpty(XY):
    tft.fillrect(16 * XY, (8, 8), tft.BLACK)

def drawBlood(XY):
    tft.fillrect(16 * XY, (8, 8), tft.RED)

def drawWall(XY):
    tft.fillrect(16 * XY, (8, 8), tft.WHITE)

def drawEggplant(XY):
    tft.fillcircle(16 * XY, 4, tft.BLUE)

def drawLetter(XY, letter):
    tft.text(16 * XY, letter, TFT.WHITE, sysfont, 1)

def fill(XY, content):
    map[XY[0]][XY[1]] = content
    match content:
        case 0:
            drawLetter(XY, "S")
        case 1:
            drawLetter(XY, "E")
        case 2:
            drawLetter(XY, "K")
        case 3:
            drawLetter(XY, "O")
        case 4:
            drawWall(XY)
        case 5:
            drawEggplant(XY)
        case 6:
            drawEmpty(XY)
        case 7:
            drawBlood(XY)

def dropEggplant():
    while True:
        x = random.randrange(16)
        y = random.randrange(16)
        if map[x][y] == 6:
            fill((x, y), 5)
            break




def runGame():
    clearAll()

    timeStep = 600
    timeDecrease = 5
    
    fill((7,6), 0)
    fill((7,7), 1)
    fill((7,8), 2)
    fill((7,9), 3)

    dropEggplant()
    
    while True:
        dropEggplant()
        timeStep -= timeDecrease
        wait(timeStep)




runGame()

