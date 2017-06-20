import pygame
import menu
import os
import run_game
import instruction
import main
import sys
import choose_song

def run_menu(screen):
    functions={'Start': choose_song.Choose_File(screen).go,
               'Help': instruction.Instruction(screen).run,
               'Quit': sys.exit}
    menu_items=functions.keys()
    pygame.display.set_caption('Pokemon Drum')
    new_menu=menu.GameMenu(screen,menu_items,functions)
    new_menu.run()

WHITE=(255,255,255)
BLACK=(0,0,0)
GREEN=GREEN=(0,255,0)
FUNCTION={'Main Menu': lambda screen: run_menu(screen)}


class Text(pygame.font.Font):
    def __init__(self,text,font=None,font_size=40,font_color=BLACK,
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

    def set_font_color(self, rgb):
        self.font_color=rgb
        self.item=self.render(self.text,True,self.font_color)

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

class Result(object):
    """Background image from:
    http://www.tophostgames.com/wp-content/uploads/2014/03/
    pikachu-wallpapers-hddownload-pokemon-wallpaper-
    1280x800-full-hd-wallpapers-59qttq3f.jpg"""

    def __init__(self,screen,max_combo,score,song_length,function=FUNCTION):
        self.screen=screen
        self.screen_width=self.screen.get_rect().width
        self.screen_height=self.screen.get_rect().height
        self.clock=pygame.time.Clock()
        self.max_combo=max_combo
        self.score=score
        self.song_length=song_length
        self.function,self.func_keys=FUNCTION,FUNCTION.keys()
        items=self.set_items()
        items+=function.keys()
        self.items=[]
        for i in xrange(len(items)):
            item=items[i]
            if item not in self.func_keys: inst_item=Text(item)
            else: inst_item=MenuItem(item)
            inst_height=len(items)*inst_item.height
            left=(self.screen_width/2)-(inst_item.width/2)
            top=(self.screen_height/2)-(inst_height/2)+(i*inst_item.height)
            inst_item.set_position(left,top)
            self.items.append(inst_item)
        self.mouse_mode=True
        self.keyboard_item=None

    def set_items(self):
        items=[]
        items+=["The length of this song is %d seconds."%(self.song_length)]
        items+=["Your score is: %d." %(self.score)]
        items+=["The max combo is: %d."%(self.max_combo)]
        items+=[" "]
        return items

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
            self.funcs[text]()

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
            item=self.items[-1]
            if item.mouseSelection(mouse_pos):
                self.function[item.text](self.screen)

    def run(self):
        self.mainloop,background_pos,fps=True,(-80,0),60
        while self.mainloop:
            self.clock.tick(fps)
            mouse_pos=pygame.mouse.get_pos()
            for event in pygame.event.get():
                self.check_event(mouse_pos,event)
            if pygame.mouse.get_rel()!=(0,0): #mouse movement
                self.mouse_mode=True
                self.keyboard_item=None
            background_image_filename=os.path.join('pics','menubg.jpg')
            self.set_mouse_visible()
            background=pygame.image.load(background_image_filename).convert()
            self.screen.blit(background,background_pos)
            item=self.items[-1]
            if self.mouse_mode:
                mpos=pygame.mouse.get_pos()
                self.set_mouse_selection(item, mpos)
            for item in self.items:
                self.screen.blit(item.item, item.position)
            pygame.display.flip()
