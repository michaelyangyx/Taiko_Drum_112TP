import pygame
import os
import main
import menu
import sys
import instruction
import run_game
import choose_song

WHITE=(255,255,255)
GREEN=(0,255,0)
BLACK=(0,0,0)


"""
Thanks to this great menu tutorial:
http://nebelprog.wordpress.com/2013/08/14/
create-a-simple-game-menu-with-pygame-pt-1-
writing-the-menu-options-to-the-screen/
"""

def run_menu(screen): #main menu pressed, call this function
    functions={'Start': choose_song.Choose_File(screen).go,
               'Help': instruction.Instruction(screen).run,
               'Quit': sys.exit}
    menu_items=functions.keys()
    pygame.display.set_caption('Pokemon Drum')
    new_menu=menu.GameMenu(screen,menu_items,functions)
    new_menu.run()

class MenuItem(pygame.font.Font):
    def __init__(self,text,font,font_size=60,font_color=WHITE,
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

class GameMenu(object): #mostly similar to the one in menu.py
    """background picture from:
       http-//www.superbwallpapers.com/minimalistic/wobbuffet-14875/"""
    def __init__(self,screen,items,file,font=None,
                 font_size=60,font_color=WHITE):
        self.screen=screen
        self.screen_width=self.screen.get_rect().width
        self.screen_height=self.screen.get_rect().height
        self.clock=pygame.time.Clock()
        self.items=[]
        for i in xrange(len(items)):
            item=items[i]
            menu_item=MenuItem(item, font, font_size, font_color)
            menu_height=len(items)*menu_item.height
            left=(self.screen_width/2)-(menu_item.width/2)
            top=(self.screen_height/2)-(menu_height/2)+(i*menu_item.height)
            menu_item.set_position(left,top)
            self.items.append(menu_item)
        self.mouse_mode=True
        self.keyboard_item=None
        self.file=file

    def set_mouse_visible(self):
        if self.mouse_mode:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

    def set_item_selection(self, key):
        for item in self.items:
            item.set_font_color(WHITE)
        if self.keyboard_item is None:
            self.keyboard_item=0
        else:
            if key==pygame.K_UP and self.keyboard_item>0:
                self.keyboard_item-=1
            elif key==pygame.K_UP and self.keyboard_item==0:
                #at the top and still up, to the bottom
                self.keyboard_item=len(self.items)-1
            elif key==pygame.K_DOWN and self.keyboard_item<len(self.items)-1:
                self.keyboard_item+=1
            elif key==pygame.K_DOWN and self.keyboard_item==len(self.items)-1:
                #at the bottom and still down, to the top
                self.keyboard_item=0
        self.items[self.keyboard_item].set_font_color(GREEN)
        if key == pygame.K_SPACE or key == pygame.K_RETURN:
            text=self.items[self.keyboard_item].text
            pygame.mixer.music.stop() #stop the music if return to main menu
            main.Game(self.screen,text).run(self.file)

    def set_mouse_selection(self, item, mpos):#set color green at mouse choice
        if item.mouseSelection(mpos):
            item.set_font_color(GREEN)
        else:
            item.set_font_color(WHITE)

    def check_event(self,mouse_pos,event):
        if event.type==pygame.QUIT:
            self.mainloop=False
            sys.exit()
        if event.type==pygame.KEYDOWN: #mouse invisible, key determine
            self.mouse_mode=False
            self.set_item_selection(event.key)
        if event.type==pygame.MOUSEBUTTONDOWN:
            for item in self.items:
                if item.mouseSelection(mouse_pos):
                    text=item.text
                    pygame.mixer.music.stop()
                    if text=='Main Menu': run_menu(self.screen)
                    else: main.Game(self.screen,text).run(self.file)

    def run(self):
        self.mainloop,fps,background_pos=True,60,(-80,0)
        pygame.mixer.init()
        music=pygame.mixer.music.load(self.file)
        pygame.mixer.music.play()
        while self.mainloop:
            self.clock.tick(fps)
            mouse_pos=pygame.mouse.get_pos()
            for event in pygame.event.get(): self.check_event(mouse_pos,event)
            if pygame.mouse.get_rel()!=(0,0): #mouse movement
                self.mouse_mode,self.keyboard_item=True,None
            background_image_filename=os.path.join('pics','menubg.jpg')
            self.set_mouse_visible()
            background=pygame.image.load(background_image_filename).convert()
            self.screen.blit(background,background_pos)
            for item in self.items:
                if self.mouse_mode:
                    mpos=pygame.mouse.get_pos()
                    self.set_mouse_selection(item, mpos)
                self.screen.blit(item.item, item.position)
            pygame.display.flip()
