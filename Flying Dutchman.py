from math import *
from random import *
import pygame
import WFCBC
from spritedef import *
pygame.init()
win=pygame.display.set_mode((1200,600))
Bscreen=pygame.Surface((1200,600))
mouse_Q=[1200/win.get_width(),600/win.get_height()]
run=True
clock=pygame.time.Clock()
click=[0,0,0]
fonts={}
texts={}
def produce(font,size,text,color):
    global fonts,texts
    font_key=font+str(size)+text+str(color)
    if not font+str(size) in fonts:
        fonts[font+str(size)]=pygame.font.SysFont(font,size)
    if not font_key in texts:
        texts[font_key.html]=fonts[font+str(size)].render(text,1,color)
    return texts[font_key]
def eventall():
    global run, mouse_pos,keys,mouse_down,click
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    keys=pygame.key.get_pressed()
    mouse_pos=pygame.mouse.get_pos()
    mouse_pos=[mouse_pos[i]*mouse_Q[i] for i in range(2)]
    mouse_down=pygame.mouse.get_pressed()
    if keys[27]: run=False
    for i in range(3):
        if mouse_down[i]:
            click[i]+=1
        else:
            click[i]=0
sprite_name_list=[
    "Jeremy",
    "Matpat",
    "Madpat",
    "Sadpat",
    "Chadpat",
    "Draco",
    "Jenny",
    "Tyler",
    "R-02",
    ]
print("available skins:")
for i in sprite_name_list:
    print(i)
ch_skin=""#input("which skin would you prefer (leave blank for jeremy)?  ")
if ch_skin in sprite_name_list:
    pskin=sprite_name_list.index(ch_skin)+1
else:
    pskin=1
class ball:
    def __init__(self,tips=0):
        self.tips=tips
        self.gravity_amplifier=1
        self.sprite=pygame.image.load("Assets\\Designs\\chtest"+str(pskin)+".png")
        if self.tips==0:
            self.mass=3
        self.sprite=pygame.transform.scale(self.sprite,(40,40))
        self.sprite=pygame.transform.rotate(self.sprite,-90)
        self.sprite.set_colorkey(self.sprite.get_at((0,0)))
        self.xspeed=0
        self.yspeed=0
        self.vectors=[]
        self.y=0#-2733#0
        self.x=0#-2134#0
    def draw(self):
        self.sprite2=pygame.transform.rotate(self.sprite,0-self.angle*180/pi)
        self.sprite2.set_colorkey(self.sprite.get_colorkey())
        win.blit(self.sprite2,(600-self.sprite2.get_width()/2+camera_offset[0],300-self.sprite2.get_height()/2+camera_offset[1]))
    def exist(self):
        global angl,bullets,gun
        self.angle=atan2(-self.yspeed,-self.xspeed)
        for i in self.vectors:
            self.xspeed+=i[0]
            self.yspeed+=i[1]
        self.vectors=[]
        #self.x+=self.xspeed
        #self.y+=self.yspeed
        #self.next_x=self.x+self.xspeed
        #self.next_y=self.y+self.yspeed
        if self.y!=0:
            self.vectors.append([0,-0.0093*self.mass*self.gravity_amplifier])
        if gun==5 and bullets<=0:
            self.vectors.append([0,-0.093*self.mass])
        #self.x=min(1190,max(10,self.x))
        #if self.x==1190 or self.x==10:
        #    self.xspeed=-self.xspeed*0.9
        self.next_x=self.x+self.xspeed
        self.next_y=self.y+self.yspeed
        if MAP[MAP_X][MAP_Y][0]==1:
            ix=(MAP_X-len(MAP)/2)*100+MAP[MAP_X][MAP_Y][1]
            iy=MAP_Y*100+MAP[MAP_X][MAP_Y][2]
            
            pygame.display.set_caption(str(MAP_X)+"  "+str(MAP_Y))
            if sqrt((self.next_x-ix)**2+(self.next_y-iy)**2)<=40:#31:
                #radius should be 30, but its 31 to allow riding the sphere
                angl=atan2(self.next_y-iy,self.next_x-ix)
                angl=pi-(self.angle-(pi/2+angl))+(pi/2+angl)
                self.tspeed=sqrt(self.xspeed**2+self.yspeed**2)*1# normal: 0.85
                self.xspeed=self.tspeed*cos(angl)
                self.yspeed=self.tspeed*sin(angl)
                pbullets=bullets
                if gun in [0]:
                    bullets=2
                elif gun in [1]:
                    bullets=6
                elif gun in [2]:
                    bullets=min(8,bullets+1)
                elif gun in [3]:
                    bullets=9999
                elif gun in [4]:
                    bullets=70
                if self.y<iy:
                    bullets=max(pbullets,ceil(bullets/2))
                if gun in [5]:
                    bullets=0
            if sqrt((self.x-ix)**2+(self.y-iy)**2)<40: #40
                angl=atan2(self.y-iy,self.x-ix)
                self.x=ix+cos(angl)*40
                self.y=iy+sin(angl)*40
                
        self.x+=self.xspeed
        self.y+=self.yspeed
        self.x=min(890,max(-890,self.x))
        if abs(self.x)==890: self.xspeed=-self.xspeed
        self.xspeed*=0.991
        self.yspeed*=0.991
        if abs(self.x)<910:
            self.y=max(0,self.y)
            if self.y==0:
                self.yspeed=-self.yspeed*0.6
                if gun in [0]:
                    bullets=2
                elif gun in [1]:
                    bullets=6
                elif gun in [2]:
                    bullets=1
                elif gun in [3]:
                    bullets=9999
                elif gun in [4]:
                    bullets=70
                elif gun in [5]:
                    bullets=1200
                    
        else:
            if self.y<-80:
                self.x=0
                self.y=0
                self.xspeed=0
                self.yspeed=0
class projectile:
    def __init__(self,team,data=[0,0,0,0,None]):
        data=data.copy()
        self.team=team
        self.tips=data[0]
        self.x=data[1]
        self.y=data[2]
        self.angle=data[3]
        self.owner=data[4]
        self.stype="drawn"
        if self.tips==0:
            self.speed=5
            self.color=(0,120,120)
            self.radius=5
            self.damage=3
            self.bounces=3
        elif self.tips==1:
            self.speed=0
            self.phase="passive"
            self.stype="sprited"
            self.spriteI=0
            self.sprites=[Ssheet.subsurface()]
        self.xspeed=-cos(self.angle)*self.speed
        self.yspeed=sin(self.angle)*self.speed
        self.vectors=[]
    def exist(self):
        for i in self.vectors:
            self.xspeed+=i[0]
            self.yspeed+=i[1]
        self.vectors=[]
        self.x+=self.xspeed
        self.y+=self.yspeed
        self.next_x=self.x+self.xspeed
        self.next_y=self.y+self.yspeed
        #if self.team==0:
        #    for i in enemies:
        #        if sqrt((self.x-i.x)**2+(self.y-i.y)**2)<self.radius+i.hitradius:
        #            self.die()
        #            i.hp-=self.damage
        self.MAP_X=min(len(MAP)-1,max(0,round(len(MAP)/2+self.x/100)))
        self.MAP_Y=min(len(MAP[0])-1,max(1,round(self.y/100)))
        if MAP[self.MAP_X][self.MAP_Y][0]==1:
            ix=(self.MAP_X-100)*100+MAP[self.MAP_X][self.MAP_Y][1]
            iy=self.MAP_Y*100+MAP[self.MAP_X][self.MAP_Y][2]
            
            if sqrt((self.next_x-ix)**2+(self.next_y-iy)**2)<20+self.radius:
                #print("this is contact")
                angl=atan2(self.next_y-iy,self.next_x-ix)
                angl=pi-(self.angle-(pi/2+angl))+(pi/2+angl)
                self.xspeed=self.speed*cos(angl)
                self.yspeed=-self.speed*sin(angl)
                self.bounces-=1
                if self.bounces==0:
                    self.die()
            if sqrt((self.x-ix)**2+(self.y-iy)**2)<20+self.radius:
                angl=atan2(self.y-iy,self.x-ix)
                self.x=ix+cos(angl)*(20+self.radius)
                self.y=iy+sin(angl)*(20+self.radius)
        if abs(self.x-ball.x)>900 or abs(self.y-ball.y)>450:
            self.die()
        if 300>self.x>-300 and self.y<0:
            self.die()
        if self.y<-80:
            self.die()
    def draw(self):
        if self.stype=="drawn":
            pygame.draw.circle(win,self.color,(ball.x+600-self.x+camera_offset[0],ball.y+300-self.y+camera_offset[1]),self.radius)
        elif self.stype=="scripted":
            s2=pygame.transform.rotate(self.sprites[self.spriteI],0-self.angle/pi*180)
            win.blit(s2,(ball.x-self.x-s2.get_width()/2+600,ball.y-self.y-s2.get_height()/2+300))
    def die(self):
        self.x=0
        self.y=0
        if self in projectiles:
            projectiles.remove(self)
class Entity:
    def __init__(self,tips,data={}):
        self.tips=tips
        self.eframe=0
        if self.tips=="Book Worm":
            self.x=0
            self.y=5000
            self.vectors=[]
            self.xspeed=0
            self.yspeed=0
            self.topangle=0
            self.length=data["length"]
            self.body_dist=4
            self.pposes=[[10000,10000,0] for i in range(self.length*self.body_dist)]
            self.patterns=[randint(0,2) for i in range(self.length-2)]
    def exist(self):
        if self.tips=="Book Worm":
            self.angle=atan2(self.y-ball.y,self.x-ball.x)+2*pi
            if self.angle>self.topangle: self.topangle+=2*pi/200
            else: self.topangle-=2*pi/200
            self.vectors.append([-cos(self.topangle)/25,-sin(self.topangle)/25])
            for i in self.vectors:
                self.xspeed+=i[0]
                self.yspeed+=i[1]
            self.vectors=[]
            self.x+=self.xspeed
            self.y+=self.yspeed
            self.xspeed*=0.98
            self.yspeed*=0.98
            self.eframe+=1
            if self.eframe%3==0:
                self.pposes.pop(0)
                self.pposes.append([round(self.x),round(self.y),round(self.topangle,2)])
        pass
    def draw(self):
        if self.tips=="Book Worm":
            for i in range(self.length):
                if i==self.length-1:
                    sprite=sprites["bookworm"]["head"].copy()
                    pdist=sqrt((self.pposes[i*self.body_dist][0]-ball.x)**2+(self.pposes[i*self.body_dist][1]-ball.y)**2)
                    if pdist<40:
                        ball.gravity_amplifier+=0.1
                        ball.vectors.append([(random()-0.5)*10,5])
                elif i==0:
                    sprite=sprites["bookworm"]["tail"].copy()
                else:
                    sprite=sprites["bookworm"]["body"+str(self.patterns[i-1]+1)].copy()
                sprite=pygame.transform.rotate(sprite,270-self.pposes[i*self.body_dist][2]/pi*180)
                win.blit(sprite,(600+ball.x-self.pposes[i*self.body_dist][0]+camera_offset[0]-sprite.get_width()/2,300+ball.y-self.pposes[i*self.body_dist][1]+camera_offset[1]-sprite.get_height()/2))
            #print(self.pposes[-1],ball.x)
#print(PRNG_seed)
#50x50 area for a circle

def reworld():
    global MAP,back,enemies
    enemies=[]
    ball.gravity_amplifier=0.9+random()/5
    if floor==1:
        MAP=[[[randint(0,randint(0,1)),randint(-20,20),randint(-20,20),0] for i in range(36)] for i in range(18)]
        back=WFCBC.Background([36,18],["test1","torch","dangel","test2","test3","test4"],WFCBC.hb,[0,0],False,[100,10,1,1,1,1])
        back.S=pygame.transform.scale(back.draw(),(1800,3600))
        for i in range(18):
            for i1 in range(36):
                if MAP[i][i1][0]==1 and i1!=0:
                    genn_x=(17-i)*100-MAP[i][i1][1]+100
                    genn_y=(36-i1)*100-MAP[i][i1][2]-10
                    if randint(1,4)==1:
                        back.S.blit(sprites["balls"]["castle2"].copy(),(genn_x-20,genn_y-20))
                    else:
                        back.S.blit(sprites["balls"]["castle1"].copy(),(genn_x-20,genn_y-20))
                    
                    #pygame.draw.circle(back.S,(255,0,0),(genn_x,genn_y),20)
    elif floor==2:
        MAP=[[[randint(0,randint(0,1)),randint(-20,20),randint(-20,20),0] for i in range(36)] for i in range(18)]
        lis1=["generated_books"+str(i+1) for i in range(21)]
        lis2=[1 for i in range(20)]
        lis2.append(1/10)
        back=WFCBC.Background([18,9],lis1,WFCBC.lv2_2,[0,0],False,lis2)
        back.S=pygame.transform.scale(back.draw(),(1800,3600))
        for i in range(18):
            for i1 in range(36):
                if MAP[i][i1][0]==1 and i1!=0:
                    genn_x=(17-i)*100-MAP[i][i1][1]+100
                    genn_y=(36-i1)*100-MAP[i][i1][2]-10
                    pygame.draw.circle(back.S,(255,255,255),(genn_x,genn_y),20,6)
        bworm_data={
            "length":20
            }
        enemies.append(Entity("Book Worm",bworm_data))
    elif floor>=3:
        MAP=[[[randint(1,randint(1,1)),randint(-20,20),randint(-20,20),0] for i in range(36)] for i in range(18)]
        back=WFCBC.Background([18,9],["bookcases1","bookcases2","bookcasesangels","bookcaseslantern"],WFCBC.lv2,[0,0],False,[1,1,1/100,2/15])
        back.S=pygame.transform.scale(back.draw(),(1800,3600))
        for i in range(18):
            for i1 in range(36):
                if MAP[i][i1][0]==1 and i1!=0:
                    genn_x=(17-i)*100-MAP[i][i1][1]+100
                    genn_y=(36-i1)*100-MAP[i][i1][2]-10
                    pygame.draw.circle(back.S,(255,255,255),(genn_x,genn_y),20,6)
    
    
camera_offset=[0,0]
ball=ball()
projectiles=[]
enemies=[]
floor=2
reworld()
angl=0
atheta=0
gun=2
bullets=20
color_phase=0
pcolor=[0,0,0]
MAP_X=0
MAP_Y=0
while run:
    atheta+=2*pi/400
    eventall()
    mangle=atan2(300-mouse_pos[1]+camera_offset[1],600-mouse_pos[0]+camera_offset[0])
    if click[0]==1 and bullets>0:
        bullets-=1
        if gun==0:
            ball.vectors.append([cos(mangle)*7,sin(mangle)*7])
            for i in range(randint(2,3)):
                extrangle=(random()-0.5)*1
                projectiles.append(projectile(0,[0,ball.x,ball.y,-mangle+extrangle,ball]))
        elif gun==1:
            extrangle=(random()-0.5)*0.8
            ball.vectors.append([cos(mangle+extrangle)*2.5,sin(mangle+extrangle)*4.2])
            projectiles.append(projectile(0,[0,ball.x,ball.y,-mangle-extrangle,ball]))
        elif gun==2:
            if ball.y==0:
                ball.vectors.append([cos(mangle)*8,sin(mangle)*9])
            else:
                ball.vectors.append([cos(mangle)*6,sin(mangle)*7])
            projectiles.append(projectile(0,[0,ball.x,ball.y,-mangle,ball]))
        elif gun==3:
            ball.vectors.append([cos(mangle)*9,sin(mangle)*9])
    if mouse_down[0] and bullets>0:
        if gun in [4]:
            bullets-=1
            ball.vectors.append([cos(mangle)*0.19,sin(mangle)*0.19])
        elif gun in [5]:
            ball.vectors.append([cos(mangle)*(0.19+random()/10),sin(mangle)*(0.19+random()/10)])
    if gun==5 and ball.y>10:
        bullets-=1
    ppos=[MAP_X,MAP_Y]
    MAP_X=min(len(MAP)-1,max(0,round(len(MAP)/2+ball.x/100)))
    MAP_Y=min(len(MAP[0])-1,max(1,round(ball.y/100)))
    camera_offset[0]=0
    if ball.x>360:
        camera_offset[0]=min(360-ball.x,0)
    if ball.x<-360:
        camera_offset[0]=max(-360-ball.x,0)
    if ball.y<240:
        camera_offset[1]=max(240-ball.y,0)
    if ball.y>3350:
        camera_offset[1]=3350-ball.y
    win.fill((6,6,6))
    win.blit(back.S,(ball.x-300+camera_offset[0],ball.y-3290+camera_offset[1]))
    for i in projectiles:
        i.exist()
        i.draw()
    for i in enemies:
        i.exist()
        i.draw()
    ball.exist()
    ball.draw()
    clock.tick(120)
    if gun in [0,2,1]:
        for i in range(bullets):
            pygame.draw.rect(win,(255,0,0),(5,5+i*15,40,10))
    elif gun in [4]:
        pygame.draw.rect(win,(255,0,0),(5,5,40,bullets))
    elif gun in [5] and bullets>0:
        pygame.draw.rect(win,(255,0,0),(5,5,40,60*bullets/1200))
    if ball.y>3350:
        Bscreen.set_alpha(ball.y-3600+255)
        win.blit(Bscreen,(0,0))
        if ball.y>3600:
            floor+=1
            ball.y=0
            ball.yspeed=0
            ball.xspeed=0
            ball.x=0
            reworld()
    pygame.display.update()
pygame.quit()
