import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from PIL import Image,ImageTk
import pdf2image
import cv2
import numpy as np
import pygame
import threading
import curses as cs
import sys
from latex_operations import *
from time import sleep


def preview():
    global current_slide
    global s
    global w
    global h
    pygame.init()
    screen = pygame.display.set_mode((w,h))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

        screen.fill((0,0,0))
        screen.blit(s[current_slide], (0,0))

        pygame.display.flip()

def to_surface(f):
    f = np.asarray(f)
    f = cv2.resize(tmp, (w,h))[:,::-1]
    f = np.rot90(f)
    s.append(pygame.surfarray.make_surface(f))

def main(sc):
    def astr(y,x,c,extra=None):
        if y<h and x<w:
            if extra == None:
                sc.addstr(y,x,c)
            else:
                sc.addstr(y,x,c,extra)
    def rect(x, y, w, h,fill='',title=''):
        astr(y,x,ctl)
        astr(y+h,x,cbl)
        astr(y,x+w,ctr)
        astr(y+h,x+w,cbr)
        for i in range(x+1,x+w):
            astr(y,i,ch)
        for i in range(x+1,x+w):
            astr(y+h,i,ch)
        for i in range(y+1,y+h):
            astr(i,x,cv)
        for i in range(y+1,y+h):
            astr(i,x+w,cv)

        if fill!='':
            for i in range(1,h):
                astr(y+i,x+1,fill*(w-2))
        if title != "":
            astr(y+1,x+w//2-len(title)//2,title)
            astr(y+2,x,chr(0x251C)+ch*(w-1)+chr(0x2524))
            pass

    global current_slide
    global command_mode
    global command
    global commands
    global setting

    cs.curs_set(0)
    cs.init_pair(1, cs.COLOR_BLACK, cs.COLOR_WHITE)
    cs.init_pair(2, cs.COLOR_BLUE, cs.COLOR_BLACK)
    cs.init_pair(3, cs.COLOR_GREEN, cs.COLOR_BLACK)


    si,sedit = 0, False

    while True:
        sc.clear()
        
        h, w = sc.getmaxyx()

        x = w//7

        for i in range(h):
            sc.addstr(i,x,cv)

        for i in range(0, length):
            rx,ry,rw,rh = 0, (h//5)*i, w//7-1, h//5-1
            if i==current_slide:
                sc.attron(cs.color_pair(2))
            rect(rx,ry,rw,rh)
            if i==current_slide:
                sc.attroff(cs.color_pair(2))
            mx, my = rx+rw//2-len(str(i+1))//2, ry+rh//2
            astr(my, mx, str(i+1))

        if command_mode:
            try:
                l = [i for i in commands if command in i]
                if command != "":
                    for i in range(len(l)):
                        astr(h-2-i,0,' '+l[i])
                astr(h-1,0,':'+command)

            except:
                command_mode = False
                cs.curs_set(0)
                command = ""

        if setting:
            if len(settings.keys())==0:
                settings["title"]=""
                settings["subtitle"]=""
                settings["author"]=""
                settings["theme"]="Nord"
                settings["aspectratio"] = "169"
                settings["font"] = "Montserrat"
                si = 0

            sc.attron(cs.color_pair(2))
            rect(w//4,1,w//2,h-3,' ',"Settings")
            sc.attroff(cs.color_pair(2))

            si = (len(settings)+si)%len(settings)

            s = "Title: "
            s2 = settings["title"] if "title" in settings.keys() else ""
            astr(5,w//2-(len(s+s2)+min(83-len(s+s2),w//2-1-len(s+s2)))//2,s,cs.A_BOLD)
            if si == 0:
                sc.attron(cs.color_pair(3 if sedit else 2))
                s2 += iic
            astr(5,len(s)+w//2-(len(s+s2)+min(83-len(s+s2),w//2-1-len(s+s2)))//2,s2+ic*min(83-len(s+s2),w//2-1-len(s+s2)))
            if si == 0:
                sc.attroff(cs.color_pair(3 if sedit else 2))

            s = "Subtitle: "
            s2 = settings["subtitle"] if "subtitle" in settings.keys() else ""
            astr(7,w//2-(len(s+s2)+min(83-len(s+s2),w//2-1-len(s+s2)))//2,s,cs.A_BOLD)
            if si == 1:
                sc.attron(cs.color_pair(3 if sedit else 2))
                s2 += iic
            astr(7,len(s)+w//2-(len(s+s2)+min(83-len(s+s2),w//2-1-len(s+s2)))//2,s2+ic*min(83-len(s+s2),w//2-1-len(s+s2)))
            if si == 1:
                sc.attroff(cs.color_pair(3 if sedit else 2))
            
            s = "Author: "
            s2 = settings["author"] if "author" in settings.keys() else ""
            astr(9,w//2-(len(s+s2)+min(83-len(s+s2),w//2-1-len(s+s2)))//2,s,cs.A_BOLD)
            if si == 2:
                sc.attron(cs.color_pair(3 if sedit else 2))
                s2 += iic
            astr(9,len(s)+w//2-(len(s+s2)+min(83-len(s+s2),w//2-1-len(s+s2)))//2,s2+ic*min(83-len(s+s2),w//2-1-len(s+s2)))
            if si == 2:
                sc.attroff(cs.color_pair(3 if sedit else 2))

            s = "Theme: "
            s2 = settings["theme"] if "theme" in settings.keys() else ""
            astr(11,w//2-(len(s+s2)+min(83-len(s+s2),w//2-1-len(s+s2)))//2,s,cs.A_BOLD)
            if si == 3:
                sc.attron(cs.color_pair(3 if sedit else 2))
                s2 += iic
            astr(11,len(s)+w//2-(len(s+s2)+min(83-len(s+s2),w//2-1-len(s+s2)))//2,s2+ic*min(83-len(s+s2),w//2-1-len(s+s2)))
            if si == 3:
                sc.attroff(cs.color_pair(3 if sedit else 2))

            s = "Font: "
            s2 = settings["font"] if "font" in settings.keys() else ""
            astr(13,w//2-(len(s+s2)+min(83-len(s+s2),w//2-1-len(s+s2)))//2,s,cs.A_BOLD)
            if si == 5:
                sc.attron(cs.color_pair(3 if sedit else 2))
                s2 += iic
            astr(13,len(s)+w//2-(len(s+s2)+min(83-len(s+s2),w//2-1-len(s+s2)))//2,s2+ic*min(83-len(s+s2),w//2-1-len(s+s2)))
            if si == 5:
                sc.attroff(cs.color_pair(3 if sedit else 2))



        sc.refresh()
        key = sc.getch()
        if setting+command_mode==0:
            if key == ord('q'):
                break
            if key == ord('n') or key == ord('J'):
                current_slide = (current_slide+1)%length
            if key == ord('N') or key == ord('K'):
                current_slide = (length+current_slide-1)%length
            if key == ord(':'):
                cs.curs_set(1)
                command_mode = True
                command = ""
                continue
        if command_mode:
            if key == 10 or key == 13:
                command_mode = False
                cs.curs_set(0)
                if command == 'preview':
                    start_preview()
                elif command == 'settings':
                    setting = True
                    si = 0
                    sedit = False
                    continue
            elif key == 127 or key == 263:
                if len(command)==0:
                    command_mode = False
                    cs.curs_set(0)
                command = command[:-1]
            else:
                command += chr(key)
        if setting:
            if sedit:
                if key == 127 or key == 263:
                    if si!=4:settings[list(settings.keys())[si]]=settings[list(settings.keys())[si]][:-1]
                else:
                    if si!=4:settings[list(settings.keys())[si]]+=chr(key)
            else:
                if key == ord('q'):
                    setting = False
                if key == ord('j'):
                    si+=1
                if key == ord('k'):
                    si-=1
            if key == 10 or key == 13:
                sedit = not sedit
                if sedit==False:
                    if si!=4:settings[list(settings.keys())[si]]=settings[list(settings.keys())[si]][:-1]



def start_preview():
    thread = threading.Thread(target=preview)
    thread.daemon = True
    thread.start()

ic,ch,cv,ctl,ctr,cbl,cbr,iic=chr(0x2581),chr(0x2500),chr(0x2502),chr(0x250C),chr(0x2510),chr(0x2514),chr(0x2518),chr(0x2588)

if __name__=='__main__':
    if len(sys.argv)>1:
        path = sys.argv[1]
        struct,settings = load(path)
        length = struct2text(struct).count('\\begin{frame}')
        setting = False
    else:
        length = 0
        settings = {}
        setting = True

    current_slide = 0
    command_mode = False
    command = ""
    commands = ['preview','settings']


    pages = pdf2image.convert_from_path('beamerthemenord.pdf', size=(3200,1800))
    w,h = 1920, 1080


    s = []
    for i in pages:
        tmp = np.asarray(i)
        f = cv2.resize(tmp, (w,h))[:,::-1]
        f = np.rot90(f)
        s.append(pygame.surfarray.make_surface(f))

    cs.wrapper(main)

