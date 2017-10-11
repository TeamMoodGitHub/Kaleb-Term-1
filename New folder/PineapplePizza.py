
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
        self.team=None
        
        
        
        
        
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
        quitButton.place(x=450,y=20)
        STOPButton=Button(self, text="Stop",
                          command=self.stop_thread)
        STOPButton.place(x=525,y=20)
        
        
        
        
        outButton=Button(self, text="BEGIN",
                         command=self.begin)
        outButton.place(x=600,y=20)
    def stop_thread(self):
        print("[INFO] closing thread...")
        try:
            if not self.stopEvent.is_set():
                self.stopEvent.is_set()
                print ('[INFO] Thread Closed')
            else:
                print('No current thread exists')
        except AttributeError:
            pass
        
        
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
                    #img2=cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
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
            tempList=[]
            if self.team == True:
                for i in self.nameList[0:5]:
                    tempList.append(cv2.imread('Champions/'+i+'Square.png',0))
                    print(i)
            if self.team == False:
                for i in self.nameList[5:10]:
                    tempList.append(cv2.imread('Champions/'+i+'Square.png',0))
                    print(i)
            try:
                while not self.stopEvent.is_set():
                    monitor={'top':Top,'left':Left,'width':Width,'height':Height}
                    sct_img=sct.grab(monitor)
                    img=np.array(sct_img)
                    img2=img.copy()   
                    img2=cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)                                     
                    ###This is the template match for champion icons.###
                    for i in tempList:
                        res,tl,br=matching(img2,i)
                        
                        if res >=0.55:        
                            cv2.rectangle(img,tl,br,200,2)
                        else:
                            print(res)
                            pass
                    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                    image=PIL.Image.fromarray(img)
                    #image=PIL.Image.frombytes('RGB',img.size,img.rgb)
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
        def matching(img, template):
            """a catch all matching sequence"""
            try:
                template=imutils.resize(template,width=20 )
                w,h=template.shape[::-1]
                #img=cv2.threshold(img,255,cv2.THRESH_BINARY)
                #template=cv2.threshold(template,127,255,cv2.THRESH_BINARY)
                res=cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
                min_val,max_val,min_loc,max_loc=cv2.minMaxLoc(res)
                top_left=max_loc
                bottom_right=(top_left[0]+w,top_left[1]+h)
                return max_val, top_left,bottom_right
            except AttributeError:
                self.panel = Label(text='NO CHAMPIONS FOUND')
                self.stopEvent.is_set()
                
        threadedLoop()

    def client_exit(self):
    	#Quit the thread, and close the window. 
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
            status=None
            try:
                
                if IGResponse['status']['status_code'] == 404:
                    print('got stuck on status 404!')
                    self.panel = Label(self,text='GAME NOT FOUND', font=("Helvetica", 18)).grid(row=11,sticky=W)                  

                    status=404
                    return None,status
                elif IGResponse['status']['status_code'] == 429:
                    print('Rate Limit Exceeded')
                    self.panel = Label(self,text='API KEY RATE LIMIT EXCEEDED, TRY AGAIN IN 2 MINUTES.', font=("Helvetica", 18)).grid(row=11,sticky=W) 
                    status=403
                    return None,status
                elif IGResponse['status']['status_code'] == 403:
                    print('got stuck on status 403!')
                    self.panel = Label(self,text='API KEY EXPIRED', font=("Helvetica", 18)).grid(row=11,sticky=W) 
    
                    status=403
                    return None,status
            except KeyError:
                pass
            print('got to IGR!')
            #print(IGResponse)
            return IGResponse, status
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
        champlist, status=requestInGameInfo(reigon,ID,APIKey)
        y=champlist
        x=[]
        summonerList=[]
        count =0
        self.team=None
        if champlist != None:
            for i in y['participants']:
                x.append(i['championId'])
            for i in y['participants']:
                summonerList.append(i['summonerName'])
                if summonerName.upper()== i['summonerName'].upper():
                    if count <= 4:
                        self.team=True
                        print('im team blue!')
                    else:
                        self.team=False
                        print('im team red!')
                else:
                    if self.team == True or self.team == False:
                        pass
                    else:
                        count+=1
                        print(count)
        self.nameList=requestChampionNames(reigon,APIKey,x)
        if status != 404 or status != 403 or status != 429:
            self.stopEvent = threading.Event()
            self.thread = threading.Thread(target=self.vidFeed, args=())
            self.thread.start()
        else:
            if status == 404:
                print('Game not found!')
            if status == 403:
                print('API Key Expired.')
            if status == 429:
                print('rate limit exceeded, please wait 2 minutes.')
            else:
                pass
        
        #######
            
if __name__ == '__main__':
    root=Tk()
    
    root.geometry('680x600')
    app = Application(root)
    root.mainloop()
