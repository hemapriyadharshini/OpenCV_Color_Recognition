import cv2 #Opencv library
import numpy as np
import pandas as pd
import argparse #Module for calling command line interfaces

#Creating argument parser to take image path from command line
ap = argparse.ArgumentParser() #Create ArgParser Object
ap.add_argument('-i', '--image', required=True, help="Image Path") #call add_argument method; Retrieves command line strings and turn them into Objects 
args = vars(ap.parse_args()) #Parse arguments from command line; Returns integer and accumulate (Sum, max,etc.,)


#Reading the image with opencv
img_path = args['image'] #Parse image path
img = cv2.imread(img_path) #Read image details

#declaring global variables (are used later on)
clicked = False #Initialize Global variable for click event
r = g = b = xpos = ypos = 0 # Initialize RGB and x,y axis values to 0

#Reading csv file with pandas and giving names to each column as there is no header
index=["color","color_name","hex","R","G","B"] #Create column names
csv = pd.read_csv('colors.csv', names=index, header=None) #Assign column names in array

#function to calculate minimum distance from all colors and get the most matching color
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

#function to get x,y coordinates of mouse double click --EVENT_LBUTTONDBLCLK, EVENT_LBUTTONDOWN, 
def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_MOUSEMOVE:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
       
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_function)

while(1):

    cv2.imshow("image",img)
    if (clicked):
   
        #cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle 
        cv2.rectangle(img,(20,20), (650,60), (b,g,r), -2)

        #Creating text string to display( Color name and RGB values )
        text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
        
        #cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

        #For very light colours we will display text in black colour
        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
            
        clicked=False

    #Break the loop when user hits 'esc' key    
    if cv2.waitKey(20) & 0xFF ==27:
        break
    
cv2.destroyAllWindows()
