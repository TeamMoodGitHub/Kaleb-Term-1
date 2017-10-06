
import time
import threading, imutils, os, cv2, requests
from mss import mss 
import numpy as np
import PIL.Image
from PIL import ImageTk
from tkinter import *
from tkinter.ttk import *
from win32api import GetSystemMetrics as GSM
sct=mss()
class Application(Frame):
 

    def __init__(self, master=None):
        
        Frame.__init__(self, master=None)
        self.master= master        
        
        self.frame=None
        self.thread=None
        self.stopEvent=None
        self.panel=None
        self.init_window()

        
        
        
        
        
    def init_window(self):
        self.master.title('Testing')
        self.pack(fill=BOTH,expand=1)
        
        self.v=StringVar()
        self.v.set('na1')
        
        
        self.key=StringVar()
        self.key.set('')
        self.name=StringVar()
        self.name.set('')
        #########
        b1label=Label(self,text='Reigon', font=("Helvetica", 12)).grid(row=0,sticky=W)
        b2label=Label(self,text='Summoner Name:', font=("Helvetica", 12)).place(x=60,y=70)
        b3label=Label(self,text='API Key:', font=("Helvetica", 12)).place(x=60,y=100)
        
        
        summonerName=Entry(self,textvariable=self.name).place(x=190,y=70)
        keyEntry=Entry(self,textvariable=self.key).place(x=190,y=100)
        
        
        button1=Radiobutton(self,text='NA',variable= self.v,value='na1').grid(row=1,sticky=W)
        button2=Radiobutton(self,text='BR',variable= self.v,value='br1').grid(row=2,sticky=W)
        button3=Radiobutton(self,text='EUNE',variable= self.v,value='eune1').grid(row=3,sticky=W)
        button4=Radiobutton(self,text='EUW',variable= self.v,value='euw1').grid(row=4,sticky=W)
        button5=Radiobutton(self,text='LAN',variable= self.v,value='lan').grid(row=5,sticky=W)
        button6=Radiobutton(self,text='LAS',variable= self.v,value='las1').grid(row=6,sticky=W)
        button7=Radiobutton(self,text='OCE',variable= self.v,value='oce1').grid(row=7,sticky=W)
        button8=Radiobutton(self,text='RU',variable= self.v,value='ru').grid(row=8,sticky=W)
        button9=Radiobutton(self,text='TR',variable= self.v,value='tr1').grid(row=9,sticky=W)
        button10=Radiobutton(self,text='JP',variable= self.v,value='jp1').grid(row=10,sticky=W)
        button11=Radiobutton(self,text='SEA',variable= self.v,value='sea1').grid(row=9,sticky=W)
        button12=Radiobutton(self,text='KR',variable= self.v,value='kr').grid(row=10,sticky=W)
        
        #The Threaded event will handle the monitor grab

        ##########
        quitButton=Button(self, text="Quit",
                          command=self.client_exit)
        quitButton.place(x=525,y=20)
        
        
        
        outButton=Button(self, text="BEGIN",
                         command=self.begin)
        outButton.place(x=600,y=20)
    def vidFeed(self):
        
        def screenGrab(**mon):
            """Gathers screen info and returns it"""
            img=np.array(sct.grab(mon))
            return mon,img
        
        def mapLocate():
            """Finds the minimap, returns the coordinates to a seperate function. Should 
            loop once every 5 seconds until a game is found."""
            #all the things that are outside the loop should be loaded before it begins, 
            #all pictures, bool and generators should start outside of the loop.
            Top=0
            Left=0
            Width=GSM(0)
            Height=GSM(1)
            templates=[cv2.imread('Temps/topLeft.png',0),
                    cv2.imread('Temps/bottom right.png',0)]
            w,h =templates[0].shape[::-1]
            w2,h2=templates[1].shape[::-1]
            try:
                while not self.stopEvent.is_set():
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
                        found=True
                        return Top,Left,Width,Height,templates
            except (AttributeError,ValueError):
                self.stopEvent.is_set()
                root.destroy
                
                
        def threadedLoop():
            """this is where the output should be"""
            Top,Left,Width,Height,templates=mapLocate()            
            try:
                while not self.stopEvent.is_set():
                    monitor={'top':Top,'left':Left,'width':Width,'height':Height}
                    sct_img=sct.grab(monitor)
                    
                    ###This is where the MIA SEARCH CODE Should go###
                    
                    image=PIL.Image.frombytes('RGB',sct_img.size,sct_img.rgb)
                    image=ImageTk.PhotoImage(image,)
                    
                    
                    if self.panel is None:
                        self.panel = Label(image=image)
                        self.panel.image = image
                        self.panel.pack(side='left',fill=BOTH,expand=1)
                    else:
                        self.panel.configure(image=image)
                        self.panel.image = image
                        
            except RuntimeError:
                print('[INFO] Thread Closed')
                self.stopEvent.is_set()
                root.destroy
        threadedLoop()

    def client_exit(self):
    		# set the stop event, cleanup the camera, and allow the rest of
		# the quit process to continue
        print("[INFO] closing...")
        try:
            
            self.stopEvent.is_set()
            print ('[INFO] Thread Closed')
        except AttributeError:
            pass
        root.destroy()
        
        
    def begin(self):

        
        ######
                        
                        
                
        
        
        
        def requestInGameInfo(reigon,ID,APIKey):        
            URL='https://'+reigon+'.api.riotgames.com/lol/spectator/v3/active-games/by-summoner/'+str(ID)+'?api_key='+APIKey
            response=requests.get(URL)
            IGResponse=response.json()
            try:
                if IGResponse['status']['status_code'] == 404:
                    print('got stuck on status 404!')
                    return None
                elif IGResponse['status']['status_code'] == 403:
                    print('got stuck on status 403!')
                    return None
            except KeyError:
                pass
            print('got to IGR!')
            #print(IGResponse)
            return IGResponse
        def requestSummonerID(reigon,summonerName,APIKey):
            URL= 'https://'+reigon+'.api.riotgames.com/lol/summoner/v3/summoners/by-name/'+summonerName+'?api_key='+APIKey
            response= requests.get(URL)
            IDResponse = response.json()
            ID=IDResponse.pop('id',None)
            #print (IDResponse)
            return ID 
        def requestChampionNames(reigon,APIKey,keyList):
            URL='https://'+reigon+'.api.riotgames.com/lol/static-data/v3/champions?locale=en_US&tags=keys&dataById=true&api_key='+APIKey
            response=requests.get(URL)
            CNResponse=response.json()
            nameList=[]
            for i in x:
                nameList.append(CNResponse['data'][str(i)]['key'])
           
            return nameList
        
        
        reigon=self.v.get()
        summonerName=self.name.get()
        APIKey=self.key.get()
        ID=requestSummonerID(reigon,summonerName,APIKey)
        champlist=requestInGameInfo(reigon,ID,APIKey)
        y=champlist
        x=[]
        summonerList=[]
        count =0
        team=None
        if champlist != None:
            for i in y['participants']:
                x.append(i['championId'])
            for i in y['participants']:
                summonerList.append(i['summonerName'])
                if summonerName== i['summonerName']:
                    if count <= 4:
                        team=True
                        print('im team blue!')
                    else:
                        team=False
                        print('im team red!')
                else:
                    if team == True or team == False:
                        pass
                    else:
                        count+=1
                        print(count)
        nameList=requestChampionNames(reigon,APIKey,x)
        
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.vidFeed, args=())
        self.thread.start()              
        
        #######
# Okay, so here is where the hard part begins. You have all the info to start the loop and pull your pictures, the __init__ has threading initialized, so you just have to 
#invoke and begin your window in the corner of your screen.
        #nameList has your champions in a list, count holds where the players position is, team True means blue, team False means red
            

root=Tk()

root.geometry('680x600')
app = Application(root)
root.mainloop()
