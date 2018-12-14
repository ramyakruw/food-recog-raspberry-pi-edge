import sys
import json
import time
from grovepi import *
from grove_rgb_lcd import *

class DisplayManager(object):
    def __init__(self):
        # LCD initial Display
        setText("Nutrition Assessment")
        setRGB(0, 128, 64)
    
    # Display name, calorie and fat value in LCD Display
    def display_nutrition_facts(self, nutrition_facts):
        print("Displaying " + strImage)
        food_name = str(nutrition_facts['item_name'])
        calories = str(nutrition_facts['nf_calories'])
        total_fat = str(nutrition_facts['nf_total_fat'])
        setText(food_name + "\n")	
        time.sleep(5)
        setText_norefresh("{} calories.\n {} total fat." + "Calories\n".format(calories, total_fat))
        time.sleep(5)
        setText("Nutrition Assessment")
        setRGB(0, 128, 64)

