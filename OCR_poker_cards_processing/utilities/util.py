
def update_config(config, img_dimension):
    if(config["default_resolution"]["Y"] == img_dimension[0] 
       and config["default_resolution"]["X"] == img_dimension[1]):
            return 
    y_ratio = img_dimension[0]/config["default_resolution"]["Y"]
    x_ratio = img_dimension[1]/config["default_resolution"]["X"]
    print("%s %s"%(y_ratio,x_ratio))
    config["user_cards"]["number"]["Y"][0] *= y_ratio 
    config["user_cards"]["number"]["Y"][1] *= y_ratio
    config["user_cards"]["number"]["X"][0] *= x_ratio
    config["user_cards"]["number"]["X"][1] *= x_ratio
    config["user_cards"]["suit"]["cards"][0]["Y"][0] *= y_ratio
    config["user_cards"]["suit"]["cards"][0]["Y"][1] *= y_ratio
    config["user_cards"]["suit"]["cards"][0]["X"][0] *= x_ratio
    config["user_cards"]["suit"]["cards"][0]["X"][1] *= x_ratio
    config["user_cards"]["suit"]["cards"][1]["Y"][0] *= y_ratio
    config["user_cards"]["suit"]["cards"][1]["Y"][1] *= y_ratio
    config["user_cards"]["suit"]["cards"][1]["X"][0] *= x_ratio
    config["user_cards"]["suit"]["cards"][1]["X"][1] *= x_ratio
    config["user_cards"]["suit"]["test_box"]["Y"][0] *= y_ratio
    config["user_cards"]["suit"]["test_box"]["Y"][1] *= y_ratio
    config["user_cards"]["suit"]["test_box"]["X"][0] *= x_ratio
    config["user_cards"]["suit"]["test_box"]["X"][1] *= x_ratio
