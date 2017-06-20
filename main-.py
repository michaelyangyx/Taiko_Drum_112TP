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

BLACK=(0,0,0)
RED=(255,0,0)
CHARCOAL=(28,28,28)
DARK_GREY=(54,54,54)
LIGHT_GREY=(232,232,232)

def load_png(name):
    full_name=os.path.join('pics',name)
    image=pygame.image.load(full_name)
    if image.get_alpha()==None:#RGBA style or not
        image=image.convert()
    else: image=image.convert_alpha()
    return image, image.get_rect()

class Game(object):
    """background.jpeg from:
    http-//www.dan-dare.org/FreeFun/Images/CartoonsMoviesTV/PokemonWallpaper1024
    .jpeg
    """
    def __init__(self,screen,difficulty,width=800,height=600):
        self.width=800
        self.height=600
        self.screen=screen
        self.game_over=False
        self.max_combo=0
        self.difficulty=difficulty
        if difficulty=='Easy': self.drum_interval=30 #30/60=0.5 sec
        elif difficulty=='Medium': self.drum_interval=24
        else: self.drum_interval=18

    def init(self):
        self.spectrum,self.duration=spectrum.spectrum(self.music_file,
                                                      self.difficulty)
        self.isExist=True
        self.timeCounter=0
        self.i=0 #move through the amplitude list
        self.fontSize=18
        myDrumX,myDrumY=210,350
        self.font=pygame.font.SysFont("Helvetica",self.fontSize)
        self.myDrum=MyDrum(myDrumX,myDrumY)
        self.charmander,self.wobbuffet,self.jiggly=[],[],[]
        self.bonusCounter,self.normalCounter=0,0
        self.score,self.state=0,None
        self.combo=0
        self.perfectR,self.goodR,self.okR=3,15,30
        self.perfectScore,self.goodScore,self.okScore=5000,2500,1000

    def check_max_combo(self):
        if self.combo>self.max_combo:
            self.max_combo=self.combo

    def checkExist(self):
        rightBound=150 #bound of the state rectangle
        for cmd in self.charmander:
            if cmd.right<rightBound: #out of bound, clear
                cmd.isExist=False
            if cmd.isExist==False:
                self.screen.blit(self.background,cmd.rect,cmd.rect)
                cmd.fly()
                if cmd.rect[0]>600:
                    self.charmander.remove(cmd)
                    self.screen.blit(self.background,cmd.rect,cmd.rect)
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

    def checkCMD(self):
        count_before,count_after=0,0
        #check if charmander drum is in hit area
        for cmd in self.charmander:
            if cmd.isExist==False: count_before+=1
            if (cmd.cx>=self.myDrum.cx-self.perfectR and
                cmd.cx<=self.myDrum.cx+self.perfectR):
                self.score+=self.perfectScore
                cmd.isExist=False
                self.state="Perfect!"
                self.combo+=1
                break #only one drum can be removed at one hit
            elif (cmd.cx>=self.myDrum.cx-self.goodR and
                  cmd.cx<=self.myDrum.cx+self.goodR):
                self.score+=self.goodScore
                cmd.isExist=False
                self.state="Good!"
                self.combo+=1
                break
            elif (cmd.cx>=self.myDrum.cx-self.okR and
                  cmd.cx<=self.myDrum.cx+self.okR):
                self.score+=self.okScore
                cmd.isExist=False
                self.state="Ok"
                self.combo+=1
                break
        for cmd in self.charmander:
            if cmd.isExist==False: count_after+=1
        if count_before==count_after: self.combo=0

    def checkWBF(self):
        count_before,count_after=0,0
        #check if wobbuffet drum is in hit area
        for wbf in self.wobbuffet:
            if wbf.isExist==False: count_before+=1
            if (wbf.cx>=self.myDrum.cx-self.perfectR and
                wbf.cx<=self.myDrum.cx+self.perfectR):
                self.score+=self.perfectScore
                wbf.isExist=False
                self.state="Perfect!"
                self.combo+=1
                break
            elif (wbf.cx>=self.myDrum.cx-self.goodR and
                  wbf.cx<=self.myDrum.cx+self.goodR):
                self.score+=self.goodScore
                wbf.isExist=False
                self.state="Good!"
                self.combo+=1
                break
            elif (wbf.cx>=self.myDrum.cx-self.okR and
                  wbf.cx<=self.myDrum.cx+self.okR):
                self.score+=self.okScore
                wbf.isExist=False
                self.state="Ok"
                self.combo+=1
                break
        for wbf in self.wobbuffet:
            if wbf.isExist==False: count_after+=1
        if count_before==count_after: self.combo=0

    def checkJGL(self):
        count_before,count_after=0,0
        #check if jiggly drum is in hit area
        for jgl in self.jiggly:
            if jgl.isExist==False: count_before+=1
            if (jgl.cx>=self.myDrum.cx-self.perfectR and
                jgl.cx<=self.myDrum.cx+self.perfectR):
                self.score+=self.perfectScore
                jgl.isExist=False
                self.state="Perfect!"
                self.combo+=1
                break
            elif (jgl.cx>=self.myDrum.cx-self.goodR and
                  jgl.cx<=self.myDrum.cx+self.goodR):
                self.score+=self.goodScore
                jgl.isExist=False
                self.state="Good!"
                self.combo+=1
                break
            elif (jgl.cx>=self.myDrum.cx-self.okR and
                  jgl.cx<=self.myDrum.cx+self.okR):
                self.score+=self.okScore
                jgl.isExist=False
                self.state="Ok"
                self.combo+=1
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
            self.clock.tick(60) #frame rate=60
            self.timeCounter+=1
            self.addDrum()
            charmandersprites=pygame.sprite.RenderPlain(tuple(self.charmander))
            wobbuffetsprites=pygame.sprite.RenderPlain(tuple(self.wobbuffet))
            jigglysprites=pygame.sprite.RenderPlain(tuple(self.jiggly))
            self.drawDrumTrack()
            charmandersprites.update()
            wobbuffetsprites.update()
            jigglysprites.update() #sprites for better update support
            self.check_max_combo()
            self.checkExist()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.mixer.music.stop()
                    sys.exit()
                else: self.keyCheck(event)
            self.draw(charmandersprites,wobbuffetsprites,jigglysprites)
            if self.game_over: break
            pygame.display.update()

    def draw(self,c_sprites,w_sprites,j_sprites):
        c_sprites.draw(self.screen)
        w_sprites.draw(self.screen)
        j_sprites.draw(self.screen)
        self.drawTexts()
        self.checkTime()

    def checkTime(self):
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
        self.myDrum.draw(self.screen)

    def drawTexts(self):
        smltopleft,smlwidth=(0,275),(150,150)
        pygame.draw.rect(self.screen,LIGHT_GREY,(smltopleft,smlwidth))
        scoreText="Score:%d"%(self.score)
        scoreText_surface=self.font.render(scoreText,True,BLACK)
        stateText="None" if self.state==None else self.state
        stateText_surface=self.font.render(stateText,True,BLACK)
        comboText="%d Combo!" % (self.combo)
        comboText_surface=self.font.render(comboText,True,RED)
        scorePos,statePos,comboPos=(600,100),(40,350),(30,300)
        scoreTextRect=scoreText_surface.get_rect().move(scorePos)
        self.screen.blit(self.background,scoreTextRect,scoreTextRect)
        self.screen.blit(comboText_surface,comboPos)
        self.screen.blit(scoreText_surface,scorePos)
        self.screen.blit(stateText_surface,statePos)

    def run(self,music_file):
        pygame.init()
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
        self.fly_dx=19.6
        self.fly_dy=-12
        self.i=0

    def update(self):
        newPos=self.calcNewPos(self.rect)
        self.rect=newPos
        self.left=self.rect[0]
        self.cx=self.left+self.halfWidth

    def fly(self):
        if self.i==0: self.rect[1]=275-self.rect[3]
        self.i+=1
        self.rect=self.rect.move(self.fly_dx,self.fly_dy)
        self.fly_dy+=0.2
        print self.cx, self.rect[1]


    def calcNewPos(self,rect):
        return rect.move(self.dx,0) #move rect to the updated position

class WobbuffetDrum(pygame.sprite.Sprite):
    """wobbuffetdrum.png from:
    http://nanouw.deviantart.com/art/Qulbutodon-Wobbudon-302357883
    """
    def __init__(self,dx):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect=load_png('wobbuffetdrum.png')
        self.rect=self.rect.move(W_STARTPOSITION)
        screen=pygame.display.get_surface()
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

class JigglyDrum(pygame.sprite.Sprite):
    """jigglydrum.png from:
    http://nanouw.deviantart.com/art/Rondoudon-Jigglydon-283691242
    """
    def __init__(self,dx):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect=load_png('jigglydrum.png')
        self.rect=self.rect.move(STARTPOSITION)
        screen=pygame.display.get_surface()
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
