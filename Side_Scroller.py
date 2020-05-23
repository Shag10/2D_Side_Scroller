import pygame
from pygame.locals import *
import os
import sys
import math
import random

pygame.init()

W, H = 800, 437
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('Side Scroller')
bg = pygame.image.load('bg.png')
bgx = 0
bgx1 = bg.get_width()
clock = pygame.time.Clock()
music=pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

class player(object):
    run = [pygame.image.load(str(x) + '.png') for x in range(8,16)]
    jump = [pygame.image.load(str(x) + '.png') for x in range(1,8)]
    slide = [pygame.image.load('S1.png'),pygame.image.load('S2.png'),pygame.image.load('S2.png'),pygame.image.load('S2.png'), pygame.image.load('S2.png'),pygame.image.load('S2.png'), pygame.image.load('S2.png'), pygame.image.load('S2.png'), pygame.image.load('S3.png'), pygame.image.load('S4.png'), pygame.image.load('S5.png')]
    fall1=pygame.image.load('0.png')
    jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False
        self.fall=False

    def draw(self, win):
        if self.fall:
            win.blit(self.fall1,(self.x,self.y+30))
        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.3
            win.blit(self.jump[self.jumpCount//18], (self.x,self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitbox=(self.x+4,self.y,self.width-24,self.height-10)
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
                self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-10)
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp=True
            elif self.slideCount>20 and self.slideCount<80:
                self.hibox=(self.x,self.y+3,self.width-8,self.height-35)
            if self.slideCount >= 110:
                self.slideCount = 0
                self.slideUp = False
                self.runCount = 0
                self.hitbox=(self.x+4,self.y,self.width-24,self.height-10)
            win.blit(self.slide[self.slideCount//10], (self.x,self.y))
            self.slideCount += 1
        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount//6], (self.x,self.y))
            self.runCount += 1
            self.hitbox=(self.x+4,self.y,self.width-24,self.height-13)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
class blade():
    img=[pygame.image.load('SAW0.png'),pygame.image.load('SAW1.png'),pygame.image.load('SAW2.png'),pygame.image.load('SAW3.png')]
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.count=0
        self.vel=1.4

    def draw(self,win):
        self.hitbox=(self.x+10,self.y+5,self.width-20,self.height-5)
        if self.count>=8:
            self.count=0
        win.blit(pygame.transform.scale(self.img[self.count//2],(64,64)),(self.x,self.y))
        self.count+=1
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    def collide(self,rect):
        if rect[0]+rect[2]>self.hitbox[0] and rect[0]<self.hitbox[0]+self.hitbox[2]:
            if rect[1]+rect[3]>self.hitbox[1]:
                return True
        return False

class spike(blade):
    img=pygame.image.load('spike.png')
    def draw(self,win):
        self.hitbox=(self.x+10,self.y,28,315)
        win.blit(self.img,(self.x,self.y))
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    def collide(self,rect):
        if rect[0]+rect[2]>self.hitbox[0] and rect[0]<self.hitbox[0]+self.hitbox[2]:
            if rect[1]<self.hitbox[3]:
                return True
        return False

def ufile():
    f=open('scores.txt','r')
    file=f.readlines()
    l=int(file[0])
    if l< int(score):
        f.close()
        fi=open('scores.txt','w')
        fi.write(str(score))
        fi.close()
        return score
    return l

def exitS():
    global pause,obj,vel,score
    pause=0
    obj=[]
    vel=30
    run=True
    while run:
        pygame.time.delay(100)
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                run=False
                pygame.quit()
            if e.type==pygame.MOUSEBUTTONDOWN:
                run=False
                p1.fall=False
                p1.jumping=False
                p1.sliding=False
        win.blit(bg,(0,0))
        lfont=pygame.font.SysFont('comicsans',80)
        prevscore=lfont.render('Best Score: '+str(ufile()),1,(0,0,0))
        newscore=lfont.render('Score: '+str(score),1,(0,0,0))
        win.blit(prevscore,(W/2-prevscore.get_width()/2,200))
        win.blit(newscore,(W/2-newscore.get_width()/2,320))
        pygame.display.update()
    score=0

def redrawwin():
    lfont=pygame.font.SysFont('comicsans',30)
    txt=lfont.render('Score: '+str(score),1,(0,0,0))
    win.blit(bg,(bgx,0))
    win.blit(bg,(bgx1,0))
    p1.draw(win)
    for ob in obj:
        ob.draw(win)
    win.blit(txt,(700,10))
    pygame.display.update()

p1=player(200,313,64,64)    
pygame.time.set_timer(USEREVENT+1,500)
pygame.time.set_timer(USEREVENT+2,random.randrange(3000,5000))
vel=30
run=True
obj=[]
pause=0
fvel=0
while run:
    if pause>0:
        pause+=1
        if pause>fvel*2:
            exitS()
    score=vel//10-3
    for ob1 in obj:
        if ob1.collide(p1.hitbox):
            p1.fall=True
            if pause==0:
                pause=1
                fvel=vel
        if ob1.x<-64:
            obj.pop(obj.index(ob1))
        else:
            ob1.x-=1.4
    bgx-=1.4
    bgx1-=1.4
    if bgx<bg.get_width()*-1:
        bgx=bg.get_width()
    if bgx1<bg.get_width()*-1:
        bgx1=bg.get_width()
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            run=False
            pygame.quit()
        if e.type==USEREVENT+1:
            vel+=1
        if e.type==USEREVENT+2:
            r=random.randrange(0,2)
            if r==0:
                obj.append(blade(810,310,64,64))
            else:
                obj.append(spike(810,0,48,320))
    if p1.fall==False:
        keys=pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if not(p1.jumping):
                p1.jumping=True
        if keys[pygame.K_DOWN]:
            if not(p1.sliding):
                p1.sliding=True
    clock.tick(vel)
    redrawwin()
