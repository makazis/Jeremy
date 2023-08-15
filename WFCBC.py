from math import *
from random import *
import pygame
pygame.init()
class Background:
    def __init__(self,size,sprites,hitboxes,start=[0,0],rotated=True,probabilities=[]):
        self.size=size
        self.rotated=rotated
        self.sprites=[pygame.transform.scale(pygame.image.load("Assets\\Backgrounds\\"+i+".png"),(60,60)) for i in sprites]
        self.shapes=hitboxes
        self.list=[[-1 for i1 in range(size[1]*3)] for i in range(size[0]*3)]
        if self.rotated:
            self.spritelist=[[[-1,-1] for i in range(size[1])] for i in range(size[0])]
        else:
            self.spritelist=[[-1 for i in range(size[1])] for i in range(size[0])]
        self.checked=[]
        self.unchecked=[start]
        while len(self.checked)<size[0]*size[1]:
            best=len(hitboxes)*4
            best_options=[]
            for i in self.unchecked:
                possible_states=[]
                if rotated:
                    for i2 in hitboxes:
                        rotated_state=i2.copy()
                        for i5 in range(4):
                            fit=True
                            for i3 in range(3):
                                for i4 in range(3):
                                    #print(i2)
                                    if not self.list[i3+i[0]*3][i4+i[1]*3] in [-1,rotated_state[i3][i4]]:
                                        fit=False
                            if fit:
                                possible_states.append([rotated_state,i5])
                            rotated_state=[[rotated_state[2][0],rotated_state[1][0],rotated_state[0][0]],
                                       [rotated_state[2][1],rotated_state[1][1],rotated_state[0][1]],
                                       [rotated_state[2][2],rotated_state[1][2],rotated_state[0][2]],
                                       rotated_state[3]]
                    pass #will finish later, this is a prototype
                    #for i2 in hitboxes:
                    #    for i1 in range(4):
                else:
                    for i2 in hitboxes:
                        fit=True
                        for i3 in range(3):
                            for i4 in range(3):
                                #print(i2)
                                if not self.list[i3+i[0]*3][i4+i[1]*3] in [-1,i2[i3][i4]]:
                                    fit=False
                        if fit:
                            possible_states.append(i2)
                if len(possible_states)<best:
                    best=len(possible_states)
                    best_options=[[i,possible_states]]
                elif len(possible_states)==best:
                    best_options.append([i,possible_states])
            chosen_one=choice(best_options)
            if rotated:
                try:
                    #print(chosen_one)
                    chosen_option=choice(chosen_one[1])
                except:
                    for i in range(3):
                        for i1 in range(3):
                            print(self.list[chosen_one[0][0]*3+i][chosen_one[0][1]*3+i1],end="\t")
                        print()
                #print(chosen_option,i)
                for i in range(5):
                    for i1 in range(5):
                        true_i=min(3,max(1,i))-1
                        true_i1=min(3,max(1,i1))-1
                        try:
                            if self.list[i+chosen_one[0][0]*3-1][i1+chosen_one[0][1]*3-1]==-1:
                                self.list[i+chosen_one[0][0]*3-1][i1+chosen_one[0][1]*3-1]=chosen_option[0][true_i][true_i1]
                        except:
                            pass
                probs=[sum(probabilities[:i+1]) for i in chosen_option[0][3]]
            
            else:
                try:
                    #print(chosen_one)
                    chosen_option=choice(chosen_one[1])
                except:
                    for i in range(3):
                        for i1 in range(3):
                            print(self.list[chosen_one[0][0]*3+i][chosen_one[0][1]*3+i1],end="\t")
                        print()
                for i in range(5):
                    for i1 in range(5):
                        true_i=min(3,max(1,i))-1
                        true_i1=min(3,max(1,i1))-1
                        try:
                            if self.list[i+chosen_one[0][0]*3-1][i1+chosen_one[0][1]*3-1]==-1:
                                self.list[i+chosen_one[0][0]*3-1][i1+chosen_one[0][1]*3-1]=chosen_option[true_i][true_i1]
                        except:
                            pass
                probs=[sum(probabilities[:i+1]) for i in chosen_option[3]]
            epsilon=random()
            #probs=[sum(probabilities[:i+1]) for i in chosen_option[3]]
            psum=probs[-1]
            probs=[i/psum for i in probs]
            for i in range(len(probs)):
                if epsilon<probs[i]:
                    break
            if rotated:
                #print(chosen_option)
                self.spritelist[chosen_one[0][0]][chosen_one[0][1]]=[chosen_option[0][3][i],chosen_option[1]]
            else:
                self.spritelist[chosen_one[0][0]][chosen_one[0][1]]=chosen_option[3][i]
            self.checked.append(chosen_one[0])
            if rotated:
                if chosen_one[0][0]>0:
                    if self.spritelist[chosen_one[0][0]-1][chosen_one[0][1]]==[-1,-1] and not([chosen_one[0][0]-1,chosen_one[0][1]] in self.checked or [chosen_one[0][0]-1,chosen_one[0][1]] in self.unchecked):
                        self.unchecked.append([chosen_one[0][0]-1,chosen_one[0][1]])                    
                if chosen_one[0][1]>0:
                    if self.spritelist[chosen_one[0][0]][chosen_one[0][1]-1]==[-1,-1] and not([chosen_one[0][0],chosen_one[0][1]-1] in self.checked or [chosen_one[0][0],chosen_one[0][1]-1] in self.unchecked):
                        self.unchecked.append([chosen_one[0][0],chosen_one[0][1]-1])                    
                if chosen_one[0][0]<self.size[0]-1:
                    if self.spritelist[chosen_one[0][0]+1][chosen_one[0][1]]==[-1,-1] and not([chosen_one[0][0]+1,chosen_one[0][1]] in self.checked or [chosen_one[0][0]+1,chosen_one[0][1]] in self.unchecked):
                        self.unchecked.append([chosen_one[0][0]+1,chosen_one[0][1]])                    
                if chosen_one[0][1]<self.size[1]-1:
                    if self.spritelist[chosen_one[0][0]][chosen_one[0][1]+1]==[-1,-1] and not([chosen_one[0][0],chosen_one[0][1]+1] in self.checked or [chosen_one[0][0],chosen_one[0][1]+1] in self.unchecked):
                        self.unchecked.append([chosen_one[0][0],chosen_one[0][1]+1])                    
            else:
                if chosen_one[0][0]>0:
                    if self.spritelist[chosen_one[0][0]-1][chosen_one[0][1]]==-1 and not([chosen_one[0][0]-1,chosen_one[0][1]] in self.checked or [chosen_one[0][0]-1,chosen_one[0][1]] in self.unchecked):
                        self.unchecked.append([chosen_one[0][0]-1,chosen_one[0][1]])                    
                if chosen_one[0][1]>0:
                    if self.spritelist[chosen_one[0][0]][chosen_one[0][1]-1]==-1 and not([chosen_one[0][0],chosen_one[0][1]-1] in self.checked or [chosen_one[0][0],chosen_one[0][1]-1] in self.unchecked):
                        self.unchecked.append([chosen_one[0][0],chosen_one[0][1]-1])                    
                if chosen_one[0][0]<self.size[0]-1:
                    if self.spritelist[chosen_one[0][0]+1][chosen_one[0][1]]==-1 and not([chosen_one[0][0]+1,chosen_one[0][1]] in self.checked or [chosen_one[0][0]+1,chosen_one[0][1]] in self.unchecked):
                        self.unchecked.append([chosen_one[0][0]+1,chosen_one[0][1]])                    
                if chosen_one[0][1]<self.size[1]-1:
                    if self.spritelist[chosen_one[0][0]][chosen_one[0][1]+1]==-1 and not([chosen_one[0][0],chosen_one[0][1]+1] in self.checked or [chosen_one[0][0],chosen_one[0][1]+1] in self.unchecked):
                        self.unchecked.append([chosen_one[0][0],chosen_one[0][1]+1])                    
            self.unchecked.remove(chosen_one[0])
    def draw(self):
        surface=pygame.Surface((self.size[1]*60,self.size[0]*60))
        for i in range(self.size[0]):
            for i1 in range(self.size[1]):
                if self.rotated:
                    #print(self.spritelist[i][i1])
                    surface.blit(pygame.transform.rotate(self.sprites[self.spritelist[i][i1][0]],-self.spritelist[i][i1][1]*90),(i1*60,i*60))
                else:
                    surface.blit(self.sprites[self.spritelist[i][i1]],(i1*60,i*60))
        return surface
hb=[
    [
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,1,2]
        ],
    [
        [0,1,0],
        [0,1,0],
        [0,1,0],
        [3]
        ],
    [
        [0,1,0],
        [0,1,0],
        [0,0,0],
        [4]
        ],
    [
        [0,0,0],
        [0,1,0],
        [0,1,0],
        [5]
        ],
    ]
lv2=[hb[0]]
lv2[0][3].append(3)
for i in range(10):
    hb.append(hb[0])
lv2_2=[hb[0]]
lv2_2[0][3]=[i for i in range(21)]
"""
    [
        [0,1,0],
        [0,1,0],
        [0,1,0],
        [1]
        ],
    [
        [0,1,0],
        [0,1,0],
        [0,0,0],
        [2]
        ],
    [
        [0,0,0],
        [0,1,0],
        [0,1,0],
        [3]
        ],
    """
rot_test=[
    [
        [0,1,0],
        [0,1,0],
        [0,0,0],
        [0,5],
        ],
    [
        [0,1,0],
        [0,1,0],
        [0,1,0],
        [1,4],
        ],
    [
        [0,1,0],
        [1,1,0],
        [0,0,0],
        [2],
        ],
    [
        [0,1,0],
        [1,1,0],
        [0,1,0],
        [3],
        ],
    
    ]
#b=Background([30,30],["generated_books"+str(i+1) for i in range(20)],lv2_2,[0,0],False,[1 for i in range(20)])
#b=Background([30,30],["bookcases1","bookcases2","bookcasesangels","bookcaseslantern"],lv2,[0,0],False,[1,1,2/100,2/15])
#b=Background([30,30],["test1","torch","dangel","test2","test3","test4"],hb,[0,0],False,[100,10,1,1,1,1])
b=Background([10,10],["Spunk1","Spunk2","Spunk4","Spunk3","Spunk5","Spunk6"],rot_test,[0,0],True,[1/5,1,1,1,1/3,1])
pygame.image.save(b.draw(),"wfc_Test.jpg")
#for i in b.list:
#    for i1 in i:
#        print(" #"[i1],end="")
#    print()
#pygame.quit()
