#! /usr/bin/python

import pygame
from pygame import *
import os.path
import random
import time

WIN_WIDTH = 500
WIN_HEIGHT = 440
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 16
FLAGS = 0
CAMERA_SLACK = 30
FPS = 30

WIN = 5

WYGRANA = 0

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (34,177,76)
YELLOW = (200,200,0)
LIGHT_GREEN = (0,255,0)
LIGHT_RED = (255,0,0)
LIGHT_YELLOW = (255,255,0)

pygame.init()

pygame.mixer.music.load("Kubson.mp3" )
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
pygame.display.set_caption("GHOSTBUSTERS")
timer = pygame.time.Clock()


smallfont = pygame.font.SysFont("comicsansms", 20)
medfont = pygame.font.SysFont("comicsansms", 25)
bigfont = pygame.font.SysFont("comicsansms", 90)

def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "med":
        textSurface = medfont.render(text, True, color)
    if size == "big":
        textSurface = bigfont.render(text, True, color)
    
    return textSurface, textSurface.get_rect()

def text_to_button(msg,color,buttonx,buttony,buttonW,buttonH,size="small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = ((buttonx+(buttonW/2)), (buttony+(buttonH/2)))
    screen.blit(textSurf, textRect)
    
def message_to_screen(msg,color,y_ile=0,size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (WIN_WIDTH/2), (WIN_HEIGHT/2)+y_ile
    screen.blit(textSurf, textRect)
    
def button (text,x,y,W,H,inactiv_C,activ_C,ACTION=None):
    cur = pygame.mouse.get_pos()    
    click = pygame.mouse.get_pressed()
    
    if x + W > cur[0] > x and y + H > cur[1] > y:
        pygame.draw.rect(screen,activ_C, (x,y,W,H))
        if click[0] == 1 and ACTION != None:
            if ACTION == "end":
                pygame.quit()
                quit()
            elif ACTION == "start":
                main()
    else:
        pygame.draw.rect(screen,inactiv_C, (x,y,W,H))
    text_to_button(text,BLACK,x,y,W,H)
    
def pauza():
    paused = True
    message_to_screen("Pauza",RED,0,"big")
    message_to_screen("C aby kontynuowac, Q aby wylaczyc!",RED,50,"small")
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    
        #screen.fill(WHITE)

       
        timer.tick(5)

def wynik(score):
    text = medfont.render("Score: "+str(score),True, RED)
    screen.blit(text,[10,10])
    
def zycia():
    serce = loadImage("serce.png")
    if player.zycie == 3:
        screen.blit(serce,[100,11])
        screen.blit(serce,[140,11])
        screen.blit(serce,[180,11])
    elif player.zycie == 2:
        screen.blit(serce,[100,11])
        screen.blit(serce,[140,11])
    else:
        screen.blit(serce,[100,11])
        

   
def game_intro():
    intro = True
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit() 
            
        screen.fill(BLACK)
        message_to_screen("ZACZYNAMY!", RED,-100,"big")
        message_to_screen("ZLAP JAK NAJWIECEJ DUCHOW!",WHITE,-20,"med")
        message_to_screen("UWOLNIJ KSIEZNICZKE",WHITE,5,"med")
        message_to_screen("I nie daj sie trafic!",WHITE,30,"med")
        

        button("start", 100,300,100,50,GREEN,LIGHT_GREEN,ACTION="start")
        button("koniec", 300,300,100,50,RED,LIGHT_RED,ACTION="end")
                
        pygame.display.update()
        timer.tick(FPS)    
    
class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)


def loadImage(name,Key=False):
    fullname = os.path.join("Grafika",name)
    image = pygame.image.load(fullname)
    
    return image
    
def loadSound(name):
    fullname = os.path.join("Grafika",name)
    sound = pygame.mixer.Sound(fullname)
    return sound

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = loadImage("g1"+".png")
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
        self.zycie = 3
        self.wynik = 0
        
        self.z = 0
        self.xvel = 0
        self.yvel = 0
        self.n = 0
        self.d_n = 0
     
        self.pozycja = []
        self.zmienna_pozycji = True
        
        self.obrot = ["g1","g36","g35","g34","g33","g32","g31","g30","g29","g28","g27","g26","g25","g24","g23","g22","g21","g20","g19","g18","g17","g16","g15","g14","g13","g12","g11","g10","g9","g8","g7","g6","g5","g4","g3","g2"]
        self.ruch = [(0,-9),(-1,-8),(-2,-7),(-3,-6),(-4,-5),(-5,-4),(-6,-3),(-7,-2),(-8,-1),(-9,0),(-8,1),(-7,2),(-6,3),(-5,4),(-4,5),(-3,6),(-2,7),(-1,8),(0,9),(1,8),(2,7),(3,6),(4,5),(5,4),(6,3),(7,2),(8,1),(9,0),(8,-1),(7,-2),(6,-3),(5,-4),(4,-5),(3,-6),(2,-7),(1,-8)]
        
    def update(self, up, down, left, right, platforms):
        
        
        self.xvel,self.yvel = self.ruch[self.n]
        
        self.collide(self.xvel, self.yvel, myPlayer,myPlatforms)
        self.n += self.d_n
        self.spr_n = self.n
        
        if up:
            self.z = 1
            self.rect.top += self.yvel
            self.rect.left += self.xvel
        if down:
            self.z = 2
            self.rect.top -= self.yvel
            self.rect.left -= self.xvel    
        
        if self.zmienna_pozycji == True:
            self.pozycja.append(self.rect.center)
            del self.pozycja[:-2]
        else:
            pass
        if left:
            self.d_n = 1
        if right:
            self.d_n = -1
        if not(left or right):
            self.d_n = 0
        if not(down or up):
            self.yvel = 0;
        
        if self.n < 0:
            self.n = 35
        elif self.n > 35:
            self.n = 0   
        
        
        
        self.a = self.obrot[self.n]+".png"
        self.image = loadImage(self.a)  
  
    def collide(self, xvel, yvel, myPlayer,myPlatforms):
            if pygame.sprite.groupcollide(myPlayer,myPlatforms,0,0):
                for hit in pygame.sprite.groupcollide(myPlayer,myPlatforms,0,0):
                    self.zmienna_pozycji = False
                    self.rect.center = self.pozycja[-2]
            else:
                self.zmienna_pozycji = True                        
                        
class Gracz_strzal(pygame.sprite.Sprite):
    def __init__(self,pos,predkosc):
        pygame.sprite.Sprite.__init__(self)
        self.image = loadImage("pocisk3.png")
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
        self.v_x,self.v_y = predkosc
    def update(self,platforms):    
        self.rect.top += self.v_y*2
        self.rect.left += self.v_x*2
        self.collide(platforms)
    def collide(self, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                self.kill()
                        
                    
class Wrog(pygame.sprite.Sprite):
    def __init__(self,x,y,a,b):
        pygame.sprite.Sprite.__init__(self)
        self.image = loadImage("wrog3.png")
        self.rect = self.image.get_rect()
        
        self.x = x
        self.y = y
        self.rect.center = (self.x,self.y)
        self.d_x = 0
        self.d_y = 0
        self.z_x = a
        self.z_y = b
        
        
    def update(self,x1,y1,platforms):
        
        self.d_x = (x1 - self.x+self.z_x)/60
        self.d_y = (y1 - self.y+self.z_y)/60
        self.x += self.d_x
        self.y += self.d_y
        
        self.rect.center = (self.x,self.y)
        
        self.collide(platforms)
        
        fire = random.randint(1,100)
        if fire <= 10:
            myStrzal.add(Wrog_strzal(self.rect.center,self.d_x,self.d_y))                    
    def collide(self, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                pass
                
class Wrog_strzal(pygame.sprite.Sprite):
    def __init__(self,pos,v_x,v_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = loadImage("pocisk.png")
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.v_x = v_x
        self.v_y = v_y
    
    def update(self,platforms):
        if self.v_x == 0 and self.v_y == 0 :
            self.kill()
        self.rect.top += self.v_y*2
        self.rect.left += self.v_x*2
        
        self.collide(platforms)
    def collide(self,platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                self.kill()

class Ksiezniczka(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = loadImage("ksiezniczka.png")
        self.rect = self.image.get_rect()
        self.rect.center = 1175, 270
    def update(self):
        if player.wynik == WIN:
            self.rect.center = 1175, 370

         
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Surface((48, 48))
        self.image.convert()
        self.image.fill(Color("#000000"))
        self.rect = Rect(x, y, 48, 48)

    def update(self):
        pass

def main():
    gameExit = False
    gameOver = False
    
    global cameraX, cameraY


    up = down = left = right = False
    bg = Surface((48,48))
    bg.convert()
    bg.fill(Color("#DDDDDD"))
    entities = pygame.sprite.Group()
    global player
    player = Player(800, 350)
    ksiezniczka = Ksiezniczka()
    platforms = []
    entities.add(player)
    
    global myPlatforms
    global myPlayer
    
    wystrzalFX = loadSound("strzal.wav")
    zgon_wrogFX = loadSound("zgon.wav")
    zgonFX = loadSound("explode2.wav")
    koniecFX = loadSound("koniec.wav")
    
    
    myPlayer = pygame.sprite.RenderClear()
    myKsiezniczka = pygame.sprite.RenderClear()
    myStrzalGracza = pygame.sprite.RenderClear()
    
    myPlatforms = pygame.sprite.RenderClear()
    
    myWrogowie = pygame.sprite.RenderClear()
    
    global myStrzal 
    myStrzal= pygame.sprite.RenderClear()
    
    myWrogowie.add(Wrog(random.randint(100,300),random.randint(100,400),random.randint(0,2),random.randint(0,2)))
    myPlayer.add(player)
    myKsiezniczka.add(ksiezniczka)

    x = y = 0
    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                 PPPP     P",
        "P    PPPPPPPPPPPP                 PPPP     P",
        "P    PPPPPPPPPPPP                          P",
        "P    PPPPPPPPPPPP    PPPPPPPP     PPPP     P",
        "P                    PPP PPPP     PPPP     P",
        "P                    PPPPPPPP              P",
        "P                                          P",
        "P    PPPPPPPP                              P",
        "P    PPPPPPPP                      PPPP    P",
        "P    PPPPPPPP                PPPPP PPPP    P",
        "P                 PPPPPP     PPPPP PPPP    P",
        "P                 PPPPPP     PPPPP         P",
        "P  PPPPP    PPPPPPPPPPPP     PPPPPPPPPP    P",
        "P  PPPPP    PPPPPPPPPPPP                   P",
        "P                                          P",
        "PP PPPPPPPPPPPP   PPPPPPPPPPPPPPPPPPPP     P",
        "PP PPPPPP     P   PPPPPPPPPPPPPPPPPPPP     P",
        "PP PPPPPP PPP P               PPPPPPPP     P",
        "PP        P       PPPP PPPPPP PPPPPPPP     P",
        "PPPPP PPPPP       PPPP PPPPPP    PPPPP     P",
        "P PPP PPPPP       PPPP PPPPPPPPP PPPPP     P",
        "P PPP PPPPP       PPPP PPPPPPPPP PPPPP     P",
        "P       PPPPPP                             P",
        "PPPPPPP                                    P",    
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
    
    #tworzy plansze
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                myPlatforms.add(p)
                platforms.append(p)
                entities.add(p)
            x += 48
        y += 48
        x = 0

    total_level_width  = len(level[0])*48
    total_level_height = len(level)*48
    camera = Camera(complex_camera, total_level_width, total_level_height)

    while not gameExit:
        if gameOver == True:
            if WYGRANA == 0:
                screen.fill(BLACK)
                message_to_screen("Koniec gry!", RED, -50,"big")
                message_to_screen("Nacisnij C aby zagrac ponownie, Q aby wylaczyc gre!", WHITE,50,"med")
            if WYGRANA == 1:
                screen.fill(WHITE)
                message_to_screen("WYGRANA!", RED, -50,"big")
                message_to_screen("Nacisnij C aby zagrac ponownie, Q aby wylaczyc gre!", BLACK,50,"med")
            pygame.display.update()
        while gameOver == True:      
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                    WYGRANA = 0                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                        WYGRANA = 0  
                    elif event.key == pygame.K_c:
                        main()
        timer.tick(FPS)

        for e in pygame.event.get():
            if e.type == QUIT: raise SystemExit, "QUIT"
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit, "ESCAPE"
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                myStrzalGracza.add(Gracz_strzal(player.rect.center,player.ruch[player.n]))
                entities.add(myStrzalGracza)
                wystrzalFX.play()
            if e.type == KEYDOWN and e.key == K_p:
                pauza()
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False  
            
        # rysuje tlo
        for y in range(48):
            for x in range(32):
                screen.blit(bg, (x * 48, y * 48))

        camera.update(player)
        
        for hit in pygame.sprite.groupcollide(myWrogowie,myStrzalGracza,1,1):
            player.wynik += 1
            myWrogowie.add(Wrog(random.randint(50,2055),random.randint(50,1185),random.randint(0,2),random.randint(0,2)))
            zgon_wrogFX.play()
        for hit in pygame.sprite.groupcollide(myPlayer,myStrzal,0,1):
            player.zycie -= 1
            zgonFX.play()
            player.rect.center = 800,350        
            if player.zycie == 0:
                koniecFX.play()
                gameOver = True
                WYGRANA = 0
        for hit in pygame.sprite.groupcollide(myPlayer,myKsiezniczka,0,0):
            gameOver = True
            WYGRANA = 1
                    
        entities.add(myStrzal)
        entities.add(myWrogowie)
        entities.add(myKsiezniczka)
       
        player.update(up, down, left, right, platforms)
        myStrzalGracza.update(platforms)
        myStrzal.update(platforms)
        myKsiezniczka.update()
        myWrogowie.update(player.rect.right,player.rect.top,platforms)
        
        
        # rysuje reszte
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        
        wynik(player.wynik)
        zycia()
        pygame.display.update()
    pygame.quit()
    quit()
    
game_intro() 
main()