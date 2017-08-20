import cv2
import mss
import numpy
sct = mss.mss()

def screenGrab():
    mon = {'top':0, 'left':40, 'width':1000, 'height':1000}
    
    img = numpy.array(sct.grab(mon))
    return mon,img    


def mainLoop():
    while 'screen records':
        mon, img = screenGrab()
        img2 = img.copy()
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        
        template = cv2.imread('C:/Users/Kaleb/documents/pictures/Champions/FioraSquare.png',0)
        
        w, h = template.shape[::-1]
        method = 'cv2.TM_CCOEFF'
        temp = template.copy()
        res = cv2.matchTemplate(img2,temp,cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        print'min loc: ',min_loc, 'max loc', max_loc
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(img,top_left, bottom_right, 255, 2)
        cv2.imshow('openCV ScreenCapture', img)
        
        cv2.imshow('mod color', img2)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


mainLoop()        