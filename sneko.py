from ST7735 import TFT
from sysfont import sysfont
from machine import SPI, Pin, ADC
import utime
import time
import math
import random
import drawer
spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11), miso=None)
tft=TFT(spi,16,17,18)
tft.initr()
tft.rgb(True)


class Joystick:
    def __init__(self, pin_x, pin_y, pin_button, deadzone=2000):
        self.x_axis = ADC(Pin(pin_x))
        self.y_axis = ADC(Pin(pin_y))
        self.button = Pin(pin_button, Pin.IN, Pin.PULL_UP)
        self.deadzone = deadzone

    def read_x(self):
        x_value = self.x_axis.read_u16()
        if x_value < 32768 - self.deadzone:
            return -(x_value - (32768 - self.deadzone))/(32768 - self.deadzone)
        elif x_value > 32768 + self.deadzone:
            return -(x_value - (32768 + self.deadzone))/(32768 - self.deadzone)
        else:
            return 0

    def read_y(self):
        y_value = self.y_axis.read_u16()
        if y_value < 32768 - self.deadzone:
            return (y_value - (32768 - self.deadzone))/(32768 - self.deadzone)
        elif y_value > 32768 + self.deadzone:
            return (y_value - (32768 + self.deadzone))/(32768 - self.deadzone)
        else:
            return 0

    def read_button(self):
        return 0 if self.button.value() else 1

    def read_joystick(self):
        x_status = self.read_x()
        y_status = self.read_y()
        button_status = self.read_button()
        return x_status, y_status, button_status




joystick = Joystick(pin_x=26, pin_y=27, pin_button=0, deadzone=2000)


map = [[6 for _ in range(16)] for _ in range(16)]
sneko = [(6,7), (7,7), (8,7), (9,7)]
nextLetter = 0
lastSnakeDir = 4
snakeDir = 0

def updateDir():
    global snakeDir
    x, y, b = joystick.read_joystick()
    newSnakeDir = snakeDir
    if abs(x) > abs(y):
        newSnakeDir = 4 if x > 0 else 2
    if abs(y) > abs(x):
        newSnakeDir = 1 if y > 0 else 3
    if (newSnakeDir - lastSnakeDir) % 4 != 2:
        snakeDir = newSnakeDir

def by8(XY):
    (x, y) = XY
    return (8 * x, 8 * y)

def wait(t):
    time.sleep_ms(t)

def waitWhileJoystick(t):
    step = 10
    while t > 0:
        wait(step)
        updateDir()
        t -= step

def readMap(XY):
    global map
    return map[XY[0]][XY[1]]

def clearAll():
    tft.fill(TFT.BLACK)

def drawEmpty(XY):
    tft.fillrect(by8(XY), (8, 8), tft.BLACK)

def drawBlood(XY):
    tft.fillrect(by8(XY), (8, 8), tft.RED)

def drawWall(XY):
    tft.fillrect(by8(XY), (8, 8), tft.WHITE)

def drawEggplant(XY):
    (x, y) = XY
    drawer.draw_bmp('eggplant.bmp', (8 * x - 4, 8 * y - 4))

def drawLetter(XY, letter):
    drawEmpty(XY)
    tft.text(by8(XY), letter, TFT.WHITE, sysfont, 1)

def writeMap(XY, content):
    map[XY[0]][XY[1]] = content
    if content == 0:
        drawLetter(XY, "S")
    elif content == 1:
        drawLetter(XY, "E")
    elif content == 2:
        drawLetter(XY, "K")
    elif content == 3:
        drawLetter(XY, "O")
    elif content == 4:
        drawWall(XY)
    elif content == 5:
        drawEggplant(XY)
    elif content == 6:
        drawEmpty(XY)
    elif content == 7:
        drawBlood(XY)

def rewriteMap(XY):
    print("redraw")
    writeMap(XY, readMap(XY))

def rewriteMapPeriphery(XY):
    (x, y) = XY
    for i in range(max(0, x - 1), 1 + min(15, x + 1)):
        for j in range(max(0, y - 1), 1 + min(15, y + 1)):
            rewriteMap((i, j))

def dropEggplant():
    while True:
        x = random.randint(0, 15)
        y = random.randint(0, 15)
        if map[x][y] == 6:
            writeMap((x, y), 5)
            break

def moveMod16(head):
    global lastSnakeDir
    (x, y) = head
    if snakeDir == 1:
        y += 1
    elif snakeDir == 2:
        x -= 1
    elif snakeDir == 3:
        y -= 1
    elif snakeDir == 4:
        x += 1
    x = x % 16
    y = y % 16
    lastSnakeDir = snakeDir
    return (x,y)

def retractTail():
    oldTail = sneko.pop(0)
    writeMap(oldTail, 6)

def advanceHeadOnly(nextHead):
    global nextLetter
    sneko.append(nextHead)
    writeMap(nextHead, nextLetter)
    nextLetter = (nextLetter + 1) % 4

def die(nextHead):
    writeMap(nextHead, 7)
    wait(300)
    (x, y) = nextHead
    for i in range(8):
        radio = i//2 + random.randint(3, 7)
        posX = 8 * x + 3.5 + random.randint(-5 - i, 5 + i)
        posY = 8 * y + 3.5 + random.randint(-5 - i, 5 + i)
        tft.fillcircle((posX, posY), radio, tft.RED)
        wait(30)
    wait(1000)
    drawer.draw_bmp('deathscreen.bmp', (0, 0))

def runGame():
    clearAll()

    timeStep = 400
    timeDecrease = 5
    
    wait(timeStep)
    writeMap((6,7), 0)
    wait(timeStep)
    writeMap((7,7), 1)
    wait(timeStep)
    writeMap((8,7), 2)
    wait(timeStep)
    writeMap((9,7), 3)
    wait(timeStep)

    for i in range(8):
        writeMap((4 + i,8), 4)
        wait(100)

    wait(timeStep)
    dropEggplant()
    wait(timeStep)
    
    while True:
        head = sneko[-1]
        nextHead = moveMod16(head)

        if head != nextHead:
            mapNextHead = readMap(nextHead)
            if mapNextHead == 6:
                retractTail()
                advanceHeadOnly(nextHead)
            elif mapNextHead == 5:
                advanceHeadOnly(nextHead)
                rewriteMapPeriphery(nextHead)
                dropEggplant()
                timeStep -= timeDecrease
            else:
                if nextHead == sneko[0]:
                    retractTail()
                    advanceHeadOnly(nextHead)
                else:
                    retractTail()
                    die(nextHead)
                    break
        waitWhileJoystick(timeStep)


runGame()

