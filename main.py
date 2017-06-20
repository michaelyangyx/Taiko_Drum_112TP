import pygame
import os
from pygame.locals import *
import sys
import random
import spectrum
import menu
import result
import instruction
import time
import choose_song

"""
Thanks for the following Tutorials with Pygame:
http://eyehere.net/2011/python-pygame-novice-professional-7/
(in Chinese)
http://www.pygame.org/docs/tut/tom/games6.html
(English)
I cannot complete this term project without these two awesome tutorials.
"""

"""
This is a game developed by Michael Yang (yuxuany) using Pygame.
As Term Project for F14-15112.
Drum Game with Pokemon Elements.
Hit 'K' when you see Wobbuffet reaching main drum,
'D' for Charmander and 'Space' for Jiggly.
The beats are transformed according to the amplitude of the music file.
Enjoy!
"""
pygame.init()

BLACK=(0,0,0)
RED=(255,0,0)
CHARCOAL=(28,28,28)
DARK_GREY=(54,54,54)
LIGHT_GREY=(232,232,232)
WHITE=(255,255,255)
GREEN=(0,255,0)

FONTSIZE=18
FONT=pygame.font.SysFont("Helvetica",FONTSIZE)

FPS=60 #60 frames per second
FUNCTION={"MAIN MENU": lambda screen: run_menu(screen)}

def run_menu(screen):
    functions={'Start': choose_song.Choose_File(screen).go,
               'Help': instruction.Instruction(screen).run,
               'Quit': sys.exit}
    menu_items=functions.keys()
    pygame.display.set_caption('Pokemon Drum')
    new_menu=menu.GameMenu(screen,menu_items,functions)
    new_menu.run()

def load_png(name):
    full_name=os.path.join('pics',name)
    image=pygame.image.load(full_name)
    if image.get_alpha()==None: #RGBA style
        image=image.convert()
    else: image=image.convert_alpha()
    return image, image.get_rect()

class Text(pygame.font.Font):
    def __init__(self,text,font=None,font_size=28,font_color=BLACK,
                 (left,top)=(0,0)):
        pygame.font.Font.__init__(self,font,font_size)
        self.text=text
        self.font_size=font_size
        self.font_color=font_color
        self.item=self.render(self.text,True,self.font_color)
        self.width=self.item.get_rect().width
        self.height=self.item.get_rect().height
        self.dimensions=(self.width,self.height)
        self.left=left
        self.top=top
        self.position=left,top

    def set_position(self, x, y):
        self.position=(x, y)
        self.left=x
        self.top=y

class MenuItem(pygame.font.Font):
    def __init__(self,text,font=None,font_size=40,font_color=BLACK,
                 (left,top)=(0, 0)):
        pygame.font.Font.__init__(self,font,font_size)
        self.text=text
        self.font_size=font_size
        self.font_color=font_color
        self.item=self.render(self.text,True,self.font_color)
        self.width=self.item.get_rect().width
        self.height=self.item.get_rect().height
        self.dimensions=(self.width,self.height)
        self.left=left
        self.top=top
        self.position=left,top
        self.is_selected=False

    def set_position(self, x, y):
        self.position=(x, y)
        self.left=x
        self.top=y

    def set_font_color(self, rgb):
        self.font_color=rgb
        self.item=self.render(self.text,True,self.font_color)

    def mouseSelection(self,(x,y)):
        #if keyboard is used, then mouse disappear
        #prevent mouse affecting keyboard choice
        if (x>=self.left and x<=self.left+self.width) and \
            (y>=self.top and y<=self.top+self.height):
            return True
        return False

class Game(object):
    """background.jpeg from:
    http-//www.dan-dare.org/FreeFun/Images/CartoonsMoviesTV/PokemonWallpaper1024
    .jpeg
    """
    """sun image from:
       http://icons.iconarchive.com/icons/dapino/summer-holiday/256/sun-icon.png
    """
    def __init__(self,screen,difficulty,function=FUNCTION):
        self.sun_image,self.sun_rect=load_png('sun.png')
        self.screen=screen
        self.screen_width=self.screen.get_rect().width
        self.screen_height=self.screen.get_rect().height
        self.game_over=False
        self.max_combo,self.difficulty=0,difficulty
        if difficulty=='Easy': self.drum_interval=30 #30/60=0.5 sec
        elif difficulty=='Medium': self.drum_interval=24
        else: self.drum_interval=18
        self.function,self.func_keys=FUNCTION,FUNCTION.keys()
        items,self.items=[],[]
        items+=function.keys()
        for i in xrange(len(items)):
            item=items[i]
            if item not in self.func_keys: inst_item=Text(item)
            else: inst_item=MenuItem(item)
            left,top=20,20
            inst_item.set_position(left,top)
            self.items.append(inst_item)

    def set_item_selection(self, key):
        for item in self.items:
            item.set_font_color(WHITE)

    def set_mouse_selection(self, item, mpos):#set color green at mouse choice
        if item.mouseSelection(mpos):
            item.set_font_color(GREEN)
        else:
            item.set_font_color(WHITE)

    def check_event(self,mouse_pos,event):
        if event.type==pygame.MOUSEBUTTONDOWN:
            item=self.items[-1]
            if item.mouseSelection(mouse_pos):
                pygame.mixer.music.stop()
                self.function[item.text](self.screen)

    def init(self):
        self.spectrum,self.duration=spectrum.spectrum(self.music_file,
                                                      self.difficulty)
        self.isExist=True
        self.timeCounter=0
        self.i=0 #move through the amplitude list
        myDrumX,myDrumY=210,350
        self.myD=MyDrum(myDrumX,myDrumY)
        self.charmander,self.wobbuffet,self.jiggly=[],[],[]
        self.bonusCounter,self.normalCounter=0,0
        self.score,self.state=0,None
        self.combo=0
        self.pR,self.gR,self.oR=4,20,40 #perfect, good, ok
        self.pScore,self.gScore,self.oScore=5000,2500,1000
        self.is_sun,self.sun_counter=False,0

    def check_max_combo(self):#overwrite max combo if current is higher
        if self.combo>self.max_combo:
            self.max_combo=self.combo

    def checkExist(self):
        rightBound=150 #bound of the state rectangle
        for cmd in self.charmander:
            if cmd.right<rightBound: #out of bound, clear
                cmd.isExist=False
            if cmd.isExist==False:
                self.charmander.remove(cmd)
        for wbf in self.wobbuffet:
            if wbf.right<rightBound: #out of bound, clear
                wbf.isExist=False
            if wbf.isExist==False:
                self.wobbuffet.remove(wbf)
        for jgl in self.jiggly:
            if jgl.right<rightBound: #out of bound, clear
                jgl.isExist=False
            if jgl.isExist==False:
                self.jiggly.remove(jgl)

    def run_perfect(self,drum): #called when drum is hit in perfect region
        self.score+=self.pScore
        drum.isExist=False
        self.state,self.is_sun="Perfect!",True #hit, sun appear
        self.combo+=1

    def run_good(self,drum): #called when drum is hit in good region
        self.score+=self.gScore
        drum.isExist=False
        self.state,self.is_sun="Good!",True
        self.combo+=1

    def run_ok(self,drum): #called when drum is hit in ok region
        self.score+=self.oScore
        drum.isExist=False
        self.state,self.is_sun="OK",True
        self.combo+=1

    def checkCMD(self):
        count_before,count_after=0,0
        #check if charmander drum is in hit area
        for cmd in self.charmander:
            if cmd.isExist==False: count_before+=1
            if (cmd.cx>=self.myD.cx-self.pR and cmd.cx<=self.myD.cx+self.pR):
                self.run_perfect(cmd)
                break #only one drum can be removed at one hit
            elif (cmd.cx>=self.myD.cx-self.gR and cmd.cx<=self.myD.cx+self.gR):
                self.run_good(cmd)
                break
            elif (cmd.cx>=self.myD.cx-self.oR and cmd.cx<=self.myD.cx+self.oR):
                self.run_ok(cmd)
                break
        for cmd in self.charmander:
            if cmd.isExist==False: count_after+=1
        if count_before==count_after: self.combo=0

    def checkWBF(self):
        count_before,count_after=0,0
        #check if wobbuffet drum is in hit area
        for wbf in self.wobbuffet:
            if wbf.isExist==False: count_before+=1
            if (wbf.cx>=self.myD.cx-self.pR and wbf.cx<=self.myD.cx+self.pR):
                self.run_perfect(wbf)
                break
            elif wbf.cx>=self.myD.cx-self.gR and wbf.cx<=self.myD.cx+self.gR:
                self.run_good(wbf)
                break
            elif (wbf.cx>=self.myD.cx-self.oR and wbf.cx<=self.myD.cx+self.oR):
                self.run_ok(wbf)
                break
        for wbf in self.wobbuffet:
            if wbf.isExist==False: count_after+=1
        if count_before==count_after: self.combo=0

    def checkJGL(self):
        count_before,count_after=0,0
        #check if jiggly drum is in hit area
        for jgl in self.jiggly:
            if jgl.isExist==False: count_before+=1
            if (jgl.cx>=self.myD.cx-self.pR and jgl.cx<=self.myD.cx+self.pR):
                self.run_perfect(jgl)
                break
            elif (jgl.cx>=self.myD.cx-self.gR and jgl.cx<=self.myD.cx+self.gR):
                self.run_good(jgl)
                break
            elif (jgl.cx>=self.myD.cx-self.oR and jgl.cx<=self.myD.cx+self.oR):
                self.run_ok(jgl)
                break
        for jgl in self.jiggly:
            if jgl.isExist==False: count_after+=1
        if count_before==count_after: self.combo=0

    def addDrum(self):
        jigglyBeat,charmanderBeat,wobbuffetBeat=0.5,0.2,0.1
        dx=-4
        if self.timeCounter%self.drum_interval==0 and self.i<len(self.spectrum):
        #to ensure game quality, no more than 2 drums is created per interval
            if self.spectrum[self.i]>jigglyBeat:
                newDrum=JigglyDrum(dx)
                self.jiggly.append(newDrum)
            elif self.spectrum[self.i]>charmanderBeat:
                newDrum=CharmanderDrum(dx)
                self.charmander.append(newDrum)
            elif self.spectrum[self.i]>wobbuffetBeat:
                newDrum=WobbuffetDrum(dx)
                self.wobbuffet.append(newDrum)
            self.i+=1

    def loop(self):
        while True:
            self.clock.tick(FPS) #frame rate=60
            self.timeCounter+=1
            self.addDrum()
            charmandersprites=pygame.sprite.RenderPlain(tuple(self.charmander))
            wobbuffetsprites=pygame.sprite.RenderPlain(tuple(self.wobbuffet))
            jigglysprites=pygame.sprite.RenderPlain(tuple(self.jiggly))
            self.drawDrumTrack()
            self.updateSprites(charmandersprites,wobbuffetsprites,jigglysprites)
            self.check_max_combo()
            self.checkExist()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.mixer.music.stop()
                    sys.exit()
                else:
                    self.mouseCheck(event)
                    self.keyCheck(event)
            self.draw(charmandersprites,wobbuffetsprites,jigglysprites)
            if self.game_over: break
            pygame.display.update()

    def updateSprites(self,c_sprites,w_sprites,j_sprites):
        c_sprites.update()
        w_sprites.update()
        j_sprites.update() #sprites for better update support

    def draw(self,c_sprites,w_sprites,j_sprites):
        sun_pos,sun_bound=(170,305),10
        c_sprites.draw(self.screen)
        w_sprites.draw(self.screen)
        j_sprites.draw(self.screen)
        for cmd in self.charmander:
            cmd.draw_text()
        for wbf in self.wobbuffet:
            wbf.draw_text()
        for jgl in self.jiggly:
            jgl.draw_text()
        if self.is_sun and self.sun_counter<=sun_bound:
            #sun_bound - the max time sun appears
            self.sun_counter+=1
            self.screen.blit(self.sun_image,sun_pos)
            if self.sun_counter==sun_bound:
                self.is_sun,self.sun_counter=False,0
        self.drawTexts()
        self.checkTime()

    def checkTime(self):
        #if time of song is over, game over and go to result interface
        now_time=time.time()
        if now_time-self.start_time>=self.duration:
            new_result=result.Result(self.screen,self.max_combo,
                                 self.score,self.duration)
            self.game_over=True
            new_result.run()

    def keyCheck(self,event):
        if event.type==KEYDOWN:
            if event.key==K_d:
                self.checkCMD()
                self.checkExist()
            elif event.key==K_k:
                self.checkWBF()
                self.checkExist()
            elif event.key==K_SPACE:
                self.checkJGL()
                self.checkExist()

    def drawDrumTrack(self):
        topleft,width=(0,275),(800,150)
        pygame.draw.rect(self.screen,DARK_GREY,(topleft,width))
        self.myD.draw(self.screen)

    def drawTexts(self):
        smltopleft,smlwidth=(0,275),(150,150)
        pygame.draw.rect(self.screen,LIGHT_GREY,(smltopleft,smlwidth))
        scoreText="Score:%d"%(self.score)
        scoreText_surface=FONT.render(scoreText,True,BLACK)
        stateText="None" if self.state==None else self.state
        stateText_surface=FONT.render(stateText,True,BLACK)
        comboText="%d Combo!" % (self.combo)
        comboText_surface=FONT.render(comboText,True,RED)
        scorePos,statePos,comboPos=(600,100),(40,350),(30,300)
        scoreTextRect=scoreText_surface.get_rect().move(scorePos)
        self.screen.blit(self.background,scoreTextRect,scoreTextRect)
        self.screen.blit(comboText_surface,comboPos)
        self.screen.blit(scoreText_surface,scorePos)
        self.screen.blit(stateText_surface,statePos)
        for item in self.items:
            self.screen.blit(item.item, item.position)

    def run(self,music_file):
        pygame.mixer.init()
        self.music_file=music_file
        music=pygame.mixer.music.load(music_file)
        pygame.mixer.music.play()
        self.start_time=time.time()
        pygame.display.set_caption('Pokemon Drum')
        background_image_filename=os.path.join('pics','background.jpeg')
        self.background=pygame.image.load(background_image_filename).convert()
        self.init()
        self.screen.blit(self.background,(0,0))
        pygame.display.flip()
        self.clock=pygame.time.Clock()
        self.loop()

    def mouseCheck(self,event):
        mouse_pos=pygame.mouse.get_pos()
        self.check_event(mouse_pos,event)
        item=self.items[-1]
        mpos=pygame.mouse.get_pos()
        self.set_mouse_selection(item, mpos)

class MyDrum(Game):
    def __init__(self,top,left):
        self.screen=pygame.display.get_surface()
        self.top=top
        self.left=left
        self.radius=40
        self.cx=self.top+self.radius

    def draw(self,screen):
        topleft,radius=(self.top,self.left),(self.radius)
        pygame.draw.circle(screen,CHARCOAL,topleft,radius)

STARTPOSITION=(800,310)
W_STARTPOSITION=(800,305)

class CharmanderDrum(pygame.sprite.Sprite):
    """
    charmander.png from:
    http://nanouw.deviantart.com/art/Saladon-Charmandon-284891511
    """
    def __init__(self,dx):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect=load_png('charmanderdrum.png')
        self.rect=self.rect.move(STARTPOSITION) #move pic to the start position
        self.screen=pygame.display.get_surface()
        self.left,self.top=self.rect[0],self.rect[1]
        self.halfWidth=self.rect[2] #(left,right,width,height)
        self.cx=self.left+self.halfWidth
        self.right=self.left+self.rect[2]
        self.dx=dx
        self.isExist=True

    def update(self):
        newPos=self.calcNewPos(self.rect)
        self.rect=newPos
        self.left=self.rect[0]
        self.cx=self.left+self.halfWidth

    def calcNewPos(self,rect):
        return rect.move(self.dx,0) #move rect to the updated position

    def draw_text(self):#draw instruction under drums of which key to press
        charmanderText="D"
        charmanderPos=(self.left+self.halfWidth/2,390)
        charmanderText_surface=FONT.render(charmanderText,True,WHITE)
        self.screen.blit(charmanderText_surface,charmanderPos)


class WobbuffetDrum(pygame.sprite.Sprite):
    """wobbuffetdrum.png from:
    http://nanouw.deviantart.com/art/Qulbutodon-Wobbudon-302357883
    """
    def __init__(self,dx):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect=load_png('wobbuffetdrum.png')
        self.rect=self.rect.move(W_STARTPOSITION)
        self.screen=pygame.display.get_surface()
        self.left,self.top=self.rect[0],self.rect[1]
        self.halfWidth=self.rect[2] #(left,right,width,height)
        self.cx=self.left+self.halfWidth
        self.dx=dx
        self.right=self.left+self.rect[2]
        self.isExist=True

    def update(self):
        newPos=self.calcNewPos(self.rect)
        self.rect=newPos
        self.left=self.rect[0]
        self.cx=self.left+self.halfWidth

    def calcNewPos(self,rect):
        return rect.move(self.dx,0)

    def draw_text(self):
        wobbuffetText="K"
        wobbuffetPos=(self.left+self.halfWidth/2,390)
        wobbuffetText_surface=FONT.render(wobbuffetText,True,WHITE)
        self.screen.blit(wobbuffetText_surface,wobbuffetPos)

class JigglyDrum(pygame.sprite.Sprite):
    """jigglydrum.png from:
    http://nanouw.deviantart.com/art/Rondoudon-Jigglydon-283691242
    """
    def __init__(self,dx):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect=load_png('jigglydrum.png')
        self.rect=self.rect.move(STARTPOSITION)
        self.screen=pygame.display.get_surface()
        self.left,self.top=self.rect[0],self.rect[1]
        self.halfWidth=self.rect[2] #(left,right,width,height)
        self.cx=self.left+self.halfWidth
        self.dx=dx
        self.right=self.left+self.rect[2]
        self.isExist=True

    def update(self):
        newPos=self.calcNewPos(self.rect)
        self.rect=newPos
        self.left=self.rect[0]
        self.cx=self.left+self.halfWidth

    def calcNewPos(self,rect):
        return rect.move(self.dx,0)

    def draw_text(self):
        jigglyText="Space"
        jigglyPos=(self.left+10,390)
        jigglyText_surface=FONT.render(jigglyText,True,WHITE)
        self.screen.blit(jigglyText_surface,jigglyPos)
