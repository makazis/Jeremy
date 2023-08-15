import pygame
pygame.init()

sprites={
    "bookworm":{
        "head":pygame.image.load("Assets\\Designs\\bookhead.png"),
        "body1":pygame.image.load("Assets\\Designs\\bookbody1.png"),
        "body2":pygame.image.load("Assets\\Designs\\bookbody2.png"),
        "body3":pygame.image.load("Assets\\Designs\\bookbody3.png"),
        "tail":pygame.image.load("Assets\\Designs\\booktail.png"),
        },
    "balls":{
        "castle1":pygame.image.load("Assets\\Designs\\ball1.png"),
        "castle2":pygame.image.load("Assets\\Designs\\ball3.png"),
        "undefined1":pygame.image.load("Assets\\Designs\\ball2.png"),
        },
    }
for i in sprites:
    for i1 in sprites[i]:
        if i=="bookworm":
            sprites[i][i1]=pygame.transform.scale(sprites[i][i1],(100,80))
            sprites[i][i1].set_colorkey((255,255,255))
        elif i=="balls":
            sprites[i][i1].set_colorkey((255,255,255))
