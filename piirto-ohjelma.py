import sys
import pygame
import ctypes


#alustetaan pygame
pygame.init()
fps = 300 #ruudunpäivitysnopeus
fpsClock = pygame.time.Clock()
width, height = 640, 480 #ikkunan koko
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE) #piirto-ohjelman ikkuna
font = pygame.font.SysFont('Arial', 20)

#muuttujat

objects = [] #napit
drawColor = [0, 0, 0] #aloitusväri
brushSize = 30 #alun pensselin koko
brushSizeSteps = 3
canvasSize = [800, 800] #piirto alue

#nappi
class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False

        objects.append(self)

    def process(self):

        mousePos = pygame.mouse.get_pos()

        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction()

                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)



#värin muutos
def changeColor(color):
    global drawColor
    drawColor = color

#muuta kynän kokoa
def changebrushSize(dir):
    global brushSize
    if dir == 'greater':
        brushSize += brushSizeSteps
    else:
        brushSize -= brushSizeSteps

#tallenna piirustus 
def save():
    pygame.image.save(canvas, "canvas.png")



#napin muuttujat
buttonWidth = 120
buttonHeight = 35

#nappien toiminnot
buttons = [
    ['Black', lambda: changeColor([0, 0, 0])],
    ['White', lambda: changeColor([255, 255, 255])],
    ['Blue', lambda: changeColor([0, 0, 255])],
    ['Green', lambda: changeColor([0, 255, 0])],
    ['Brush Larger', lambda: changebrushSize('greater')],
    ['Brush Smaller', lambda: changebrushSize('smaller')],
    ['Save', save],
]

#nappien tekeminen
for index, buttonName in enumerate(buttons):
    Button(index * (buttonWidth + 10) + 10, 10, buttonWidth,
           buttonHeight, buttonName[0], buttonName[1])

#piirto alusta
canvas = pygame.Surface(canvasSize)
canvas.fill((255, 255, 255))

#piirron loop
while True:
    screen.fill((30, 30, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #napit
    for object in objects:
        object.process()

    #tehdään piirtocanvas
    x, y = screen.get_size()
    screen.blit(canvas, [x/2 - canvasSize[0]/2, y/2 - canvasSize[1]/2])

    #mahdollistetaan piirtäminen
    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()

        
        dx = mx - x/2 + canvasSize[0]/2
        dy = my - y/2 + canvasSize[1]/2

        pygame.draw.circle(
            canvas,
            drawColor,
            [dx, dy],
            brushSize,
        )

    #viitepiste
    pygame.draw.circle(
        screen,
        drawColor,
        [100, 100],
        brushSize,
    )

    pygame.display.flip()
    fpsClock.tick(fps)