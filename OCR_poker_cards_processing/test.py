import json
import utilities.card_processing as card_processing
import glob
import cv2
from utilities.util import update_config
from copy import deepcopy
import numpy as np
#path to folder with test screenshot
sample_folder_path = ".\\poker_screenshot_processing\\test_sample"


#read config data from JSON file
config_file = open(".\\poker_screenshot_processing\\config.json","r")
#read raw data from the opened file
raw_data = config_file.read()
config_file.close()
#converting raw JSON data to python dictonary
config_data = json.loads(raw_data)
samples = glob.glob(sample_folder_path + "\\*.png")
samples.sort()

def get_user_suit_with_preporcesing(img, color_thressold, suit_cordinates, test_box):
    suit = []
    for suit_cor in suit_cordinates:
        suit.append(get_suit_helper(img, color_thressold, test_box, suit_cor))
    return suit

def get_suit_helper(img, color_thressold, test_box, suit_cor):
    return card_processing.get_suit(
            img[suit_cor["Y"][0]:suit_cor["Y"][1],suit_cor["X"][0]:suit_cor["X"][1]],
            [
                [test_box["Y"][0],test_box["X"][0]],
                [test_box["Y"][0],test_box["X"][1]],
                [test_box["Y"][1],test_box["X"][0]],
                [test_box["Y"][1],test_box["X"][1]],
                [int((test_box["Y"][0] + test_box["Y"][1] )/2),
                 int((test_box["X"][0]+ test_box["X"][1])/2)]
            ],
            color_thressold["background"],
            color_thressold["black"],
            color_thressold["red"]
        )

def get_user_cards(config, img, flag):
    number_cordinates = config["user_cards"]["number"]
    if(flag == True):
            new_img = img.copy()
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            new_img = cv2.filter2D(new_img,-1,kernel)
            card_numbers = card_processing.get_text(new_img[
                (number_cordinates["Y"][0]):(number_cordinates["Y"][1]),
                (number_cordinates["X"][0]):(number_cordinates["X"][1]),
                ])
            if(len(card_numbers) == 1):
                card_numbers += card_processing.get_text(new_img[
                    number_cordinates["exepction_case"]["Y"][0]:number_cordinates["exepction_case"]["Y"][1],
                    number_cordinates["exepction_case"]["X"][0]:number_cordinates["exepction_case"]["X"][1],
                ])
    else:
        card_numbers = card_processing.get_text(img[
            number_cordinates["Y"][0]:number_cordinates["Y"][1],
            number_cordinates["X"][0]:number_cordinates["X"][1],
        ])
        if(len(card_numbers) == 1):
            card_numbers += card_processing.get_text(img[
                number_cordinates["exepction_case"]["Y"][0]:number_cordinates["exepction_case"]["Y"][1],
                number_cordinates["exepction_case"]["X"][0]:number_cordinates["exepction_case"]["X"][1],
            ])
    suit_cordinates = config["user_cards"]["suit"]["cards"]
    test_box = config["user_cards"]["suit"]["test_box"]
    suit = get_user_suit_with_preporcesing(img,config["color_thressold"], suit_cordinates, test_box)
    
    return card_numbers,suit

def get_table_cards(config, img, flag):
    cards = []
    suit = []
    number_cordinates = config["table_cards"]["numbers"]
    offset = config["table_cards"]["offset"]
    test_box = config["table_cards"]["suit"]["test_box"]
    color_thressold = config["color_thressold"]
    base_suit_cor = config["table_cards"]["suit"]
    for i in range(5):
        '''cv2.imshow("test2" + str(i),img[
            (number_cordinates["Y"][0]):(number_cordinates["Y"][1]),
            (number_cordinates["X"][0]+ offset * i):(number_cordinates["X"][1]+ offset * i),
            ])'''
        #Below part of code needs to be optimized
        if(flag == True):
            new_img = img.copy()
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            new_img = cv2.filter2D(new_img,-1,kernel)
            card = card_processing.get_text(new_img[
                (number_cordinates["Y"][0]):(number_cordinates["Y"][1]),
                (number_cordinates["X"][0]+ offset * i):(number_cordinates["X"][1]+ offset * i),
                ])
        else:
            card = card_processing.get_text(img[
                (number_cordinates["Y"][0]):(number_cordinates["Y"][1]),
                (number_cordinates["X"][0]+ offset * i):(number_cordinates["X"][1]+ offset * i),
                ])
        '''if the card value is an empty string that means that
            there is no next card.
        '''
        if(card.strip() == ""):
            break
        else:
            cards.append(card)
        suit_cor = deepcopy(base_suit_cor)
        suit_cor["X"][0]+= i*offset
        suit_cor["X"][1]+= i*offset
        #cv2.imshow("test suit 1" + str(i),img[suit_cor["Y"][0]:suit_cor["Y"][1],suit_cor["X"][0]:suit_cor["X"][1]])
        suit.append(get_suit_helper(img, color_thressold, test_box, suit_cor))
    cv2.waitKey(0)
    return cards, suit

def image_pre_processing(img):
    height = img.shape[0]
    new_img = cv2.resize(img.copy()[29:-1,:], (850,585))
    cv2.imwrite("test1.png", new_img)
    return new_img, height <=585


for sample in samples:
    #sample = ".\\poker_screenshot_processing\\test_sample\\sample (13).png"
    #we create a copy of config so that each file can have its resolution and specific data related to it
    config = config_data.copy()
    img, flag = image_pre_processing(cv2.imread(sample))
    card_numbers, suit = get_user_cards(config, img, flag)
    table_cards, table_cards_suit = get_table_cards(config, img, flag)
    print("%s the cards are :"%sample)
    print("Cards in hand = (%s,%s)"%(str(list(card_numbers)),str(suit)))
    print("Table Cards = (%s,%s)"%(str(table_cards),str(table_cards_suit)))