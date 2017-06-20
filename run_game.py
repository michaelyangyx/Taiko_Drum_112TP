import menu
import main
import instruction
import pygame
import sys
import choose_song

pygame.init()

if __name__ == "__main__":
    screen=pygame.display.set_mode((800,600),0,32)
    functions={'Start': choose_song.Choose_File(screen).go,
               'Help': instruction.Instruction(screen).run,
               'Quit': sys.exit}
    menu_items=functions.keys()
    pygame.display.set_caption('Pokemon Drum')
    new_menu=menu.GameMenu(screen,menu_items,functions)
    new_menu.run()
