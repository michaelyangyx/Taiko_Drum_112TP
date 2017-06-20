import main
import pygame

pygame.init()

def test_main():
    print "Testing Main...",
    screen=pygame.display.set_mode((800,600),0,32)
    game=main.Game(screen,'Hard')
    assert(game.drum_interval==18)
    wobbuffet=main.WobbuffetDrum(0)
    assert(wobbuffet.left==800)
    jiggly=main.JigglyDrum(0)
    assert(jiggly.left==800)
    charmander=main.CharmanderDrum(0)
    assert(charmander.left==800)
    print "Passed!"

test_main()
