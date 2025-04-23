import pygame
import sys

#alustetaan Pygame
pygame.init()

#näytön mitat
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Piirrosohjelma")

#fontti ja kello
font = pygame.font.SysFont("Arial", 16)
clock = pygame.time.Clock()

#värit ja oletusarvot(sivellin, piirtotyyli
draw_color = (0, 0, 0)
brush_size = 10
draw_mode = "free"  # "free", "circle", "square"

#piirtoalusta(valkoinen, toolbar ylhäällä)
canvas = pygame.Surface((WIDTH, HEIGHT - 100))
canvas.fill((255, 255, 255))

#button luokka, luo painettavan napin
class Button:
    def __init__(self, x, y, w, h, text, callback):
        self.rect = pygame.Rect(x, y, w, h) #napin koko ja sijainti
        self.text = text #napin teksti
        self.callback = callback #toiminto, joka tapahtuu painettaessa
        self.hovered = False #hiiren osoitin napin päällä

    def draw(self, surface):
        #väri riippuen siitä, onko hiiri napin päällä
        #rikottu sininen napin värinä ja jos hiiri päällä niin puhdas sininen
        color = (70, 70, 225) if not self.hovered else (0, 0, 225)
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2) # Musta reuna
        #piirretään napin teksti keskelle
        text_surf = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        #tarkistetaan, onko hiiri napin päällä ja onko klikattu
    def update(self, mouse_pos, mouse_click):
        self.hovered = self.rect.collidepoint(mouse_pos)
        if self.hovered and mouse_click:
            self.callback() #suoritetaan napin toiminto
#toolbar luokka, jonka sisäl napit
class Toolbar:
    def __init__(self):
        self.buttons = [] # Lista napeista
        self.create_buttons() # Luodaan napit

    def create_buttons(self):
        #napin koko ja sijaintien asetuksia
        spacing = 10
        x, y = spacing, spacing
        w, h = 200, 20

        #värit ja niiden napit
        self.buttons.append(Button(x, y, w, h, "Musta", lambda: change_color((0, 0, 0))))
        x += w + spacing
        self.buttons.append(Button(x, y, w, h, "Sininen", lambda: change_color((0, 0, 255))))
        x += w + spacing
        self.buttons.append(Button(x, y, w, h, "Vihreä", lambda: change_color((0, 255, 0))))
        x += w + spacing
        self.buttons.append(Button(x, y, w, h, "Keltainen", lambda: change_color((225, 255, 0))))

        #piirtotyylit(vapaa, ympyrä, neliö)
        x = spacing
        y += h + spacing
        self.buttons.append(Button(x, y, w, h, "Vapaa", lambda: change_mode("free")))
        x += w + spacing
        self.buttons.append(Button(x, y, w, h, "Ympyrä", lambda: change_mode("circle")))
        x += w + spacing
        self.buttons.append(Button(x, y, w, h, "Neliö", lambda: change_mode("square")))

        #siveltimen koon säätö
        x = spacing
        y += h + spacing
        self.buttons.append(Button(x, y, w, h, "Koko +", lambda: change_brush("up")))
        x += w + spacing
        self.buttons.append(Button(x, y, w, h, "Koko -", lambda: change_brush("down")))


    def draw(self, surface):
        #piirretään kaikki napit ruudulle
        for btn in self.buttons:
            btn.draw(surface)

    def update(self, mouse_pos, mouse_click):
        #päivitetään nappien tila 
        for btn in self.buttons:
            btn.update(mouse_pos, mouse_click)
#määritellää nappien toiminnot
def change_color(color):
    global draw_color
    draw_color = color

def change_mode(mode):
    global draw_mode
    draw_mode = mode

def change_brush(direction):
    global brush_size
    if direction == "up":
        brush_size += 5
    elif direction == "down":
        brush_size = max(1, brush_size - 5)


#luodaan toolbar
toolbar = Toolbar()

#pää looppi
while True:
    #täytetään tausta magenta värillä
    screen.fill((255, 0, 255))
    # Haetaan hiiren sijainti ja klikkaustieto
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]

    #tapahtumien käsittely
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #toolbar ylhäällä
    toolbar.update(mouse, click)
    toolbar.draw(screen)

    #piirtoalue (alla toolbarin jälkeen)
    screen.blit(canvas, (0, 100))

    #piirtäminen canvasille
    if click and mouse[1] > 100:
        x, y = mouse[0], mouse[1] - 100 #siirretään koordinaatit canvasin sisään
        if draw_mode == "free":
            pygame.draw.circle(canvas, draw_color, (x, y), brush_size)
        elif draw_mode == "circle":
            pygame.draw.circle(canvas, draw_color, (x, y), brush_size, 2)
        elif draw_mode == "square":
            rect = pygame.Rect(x - brush_size, y - brush_size, brush_size * 2, brush_size * 2)
            pygame.draw.rect(canvas, draw_color, rect, 2)
    #päivitetään näyttö
    pygame.display.flip()
    clock.tick(60)
