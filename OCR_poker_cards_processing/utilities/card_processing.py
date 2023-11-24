import cv2
from pytesseract import pytesseract
from numpy import array

thresholdValue = 110
path_to_tesseract = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def get_text(img):        
    pytesseract.tesseract_cmd = path_to_tesseract
    gray_scale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray_scale_img, thresholdValue, 255, cv2.THRESH_BINARY)[1]
    text = pytesseract.image_to_string(thresh, config="--psm 6 -c tessedit_char_whitelist=023456789JQKA")
    return text.strip()



'''
Get suit logic. Make a square around the suit. Then we check color of the 4 points 
and the point at the centre:
Note: If color of background_color or suit changes make those changes in config file and 
        they shall reflect here
Rules:
Diamond : 4 corners of square are background_color color and the centre is 
            red
Heart : Top 2 corners and the centre is red while the bottom two points lie on background_color
Spade and club : both have same value for all the five points hence we use a different 
                apporach. We draw lines along the height and check. As club has a curve
                if you track color change along the line you can figure out if its 
                spade or club.

NOTE: spade and club logic need more generalisation to work 100% with color changes for cards                
'''

def helper(color, black_suit_color, red_suit_color):
    if(color>=black_suit_color[0] and color<=black_suit_color[1]):
        return 2
    if(color>=red_suit_color[0] and color<=red_suit_color[1]):
        return 3
    return 1
    
def get_suit(img, cordinates, background_color, black_suit_color, red_suit_color):
    temp = []
    suit = ""
    #converting the RGB values to gray scale using simple average
    for cordinate in cordinates:
        temp.append(int(sum(img[cordinate[0],cordinate[1]])/3))

    if(temp[4]>=red_suit_color[0] and temp[4]<=red_suit_color[1] 
       and temp[0]>=background_color[0] and temp[0]<=background_color[1] 
       and temp[1]>=background_color[0] and temp[1]<=background_color[1] 
       and temp[2]>=background_color[0] and temp[2]<=background_color[1] 
       and temp[3]>=background_color[0] and temp[3]<=background_color[1]):
        suit = "diamond"
    
    elif(temp[4]>=red_suit_color[0] and temp[4]<=red_suit_color[1]
         and temp[0]>=red_suit_color[0] and temp[0]<=red_suit_color[1] 
         and temp[1]>=red_suit_color[0] and temp[1]<=red_suit_color[1] 
         and temp[2]>=background_color[0] and temp[2]<=background_color[1] 
         and temp[3]>=background_color[0] and temp[3]<=background_color[1]):
        suit = "heart"

    elif(temp[4]>=black_suit_color[0] and temp[4]<=black_suit_color[1]
         and temp[0]>=background_color[0] and temp[0]<=background_color[1] 
         and temp[1]>=background_color[0] and temp[1]<=background_color[1]
         and temp[2]>=black_suit_color[0] and temp[2]<=black_suit_color[1] 
         and temp[3]>=black_suit_color[0] and temp[3]<=black_suit_color[1]):
        change_counter = 0
        for i in range(cordinates[0][1]-3,cordinates[4][1]):
            previous_color = helper(int(sum(img[i,cordinates[0][0]])/3), black_suit_color, red_suit_color)
            change_counter = 0
            #print("------------>")
            for j in range(cordinates[0][0]+1,cordinates[2][0],1):
                current_color = helper(int(sum(img[j,i])/3), black_suit_color, red_suit_color)
                #print("(%d,%d,%d,%d)"%(previous_color,current_color, i,j))
                if(previous_color == 2 and current_color !=2):
                    #print("in")
                    change_counter+=1
                if(change_counter ==1 and previous_color !=2 and current_color ==2):
                    change_counter+=1
                if(change_counter>1):
                    break
                previous_color = current_color
            if(change_counter>1):
                break
        
        if(change_counter < 2):
            suit = "spade"
        else:
            suit = "club"
    else:
        suit = "unknown"
    return suit
