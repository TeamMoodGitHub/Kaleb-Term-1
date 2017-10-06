# -*- coding: utf-8 -*-

import time # gonna be used to limit api key calls 
import numpy as np
import cv2
from mss import mss
import cassiopeia as cass
import argparse
from win32api import GetSystemMetrics as GSM
import imutils
sct=mss()

def mapLocate( ):
    """Finds the minimap, returns to main function with location and is then ready for Rito's API to be used. 
        """
    #all the things that are outside the loop should be loaded before it begins, 
    #all pictures, bool and generators should start outside of the loop.
    #cass should be in a seperate function, soft looping until a match is found
    Top=0
    Left=0
    Width=GSM(0)
    Height=GSM(1)
    templates=[cv2.imread('Temps/topLeft.png',0),
            cv2.imread('Temps/bottom right.png',0)]
    w,h =templates[0].shape[::-1]
    templates2=templates.copy()
    w2,h2=templates[1].shape[::-1]
    
    #The goal of this loop is to find the minimap
    while('recording'):
        mon,img=screenGrab(top=Top,left=Left,width=Width,height=Height)
        img2=img.copy()
        img2=cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)         
        res=[]
        for i in templates:
            x=cv2.matchTemplate(img2,i,cv2.TM_CCOEFF_NORMED)
            min_val,max_val,min_loc,max_loc=cv2.minMaxLoc(x)
            res.append(max_val)
            res.append(max_loc)

        if res[0] > 0.80 and res[2] > 0.80  :
            wallFloor=(res[3][0]+w2,res[3][1]+h2)
            cv2.destroyAllWindows()
            Top=res[1][1]
            Left=res[1][0]
            Width=wallFloor[0]-res[1][0]
            Height=wallFloor[1]-res[1][1]

            return Top,Left,Width,Height,templates
def ritoGrab():
    Top,Left,Width,Height,templates=mapLocate()
    
    while('record'):
        mon,img=screenGrab(top=Top,left=Left,width=Width,height=Height)
        img2=img.copy()
        cv2.imshow('img',img2)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break





def screenGrab(**mon):
    img=np.array(sct.grab(mon))
    return mon, img



ritoGrab()