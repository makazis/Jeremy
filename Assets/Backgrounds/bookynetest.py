from random import *
from math import *
import pygame
pygame.init()
win=pygame.Surface((60,60))
for i3 in range(20):
    win.fill((125,65,0))
    for i in range(6):
        pygame.draw.line(win,(95,45,0),(0,i*10),(60,i*10))
        c=59
        while c>-1:
            book_size=randint(3,randint(3,6))
            book_y_size=randint(0,randint(1,3))
            book_p_color=[randint(0,155) for i in range(3)]
            book_d_color=[i/1.5 for i in book_p_color]
            engraving_color=[[randint(100,255),randint(100,255),randint(100,255)],
                             [205,205,205],
                             [255,225,0]
                             ][randint(0,randint(0,2))]
            if c<2:
                break
            elif c-book_size>=-1:
                pygame.draw.rect(win,book_p_color,(c-book_size+1,i*10+1+book_y_size,book_size,9-book_y_size))
                for i1 in range(book_size):
                    for i2 in range(7-book_y_size):
                        if randint(1,5)>2:
                            darkness=randint(20,150)
                            c2=engraving_color.copy()
                            for i7 in range(3):
                                c2[i7]=max(0,c2[i7]-darkness)
                            win.set_at((c-i1-1,i*10+2+book_y_size+i2),c2)
                pygame.draw.line(win,book_d_color,(c,i*10+1+book_y_size),(c,i*10+9))
                pygame.draw.line(win,book_d_color,(c-book_size+1,i*10+1+book_y_size),(c-book_size+1,i*10+9))
                c-=book_size
    pygame.image.save(win,"generated_books"+str(i3+1)+".png")
