
import requests
import constants

# Gets the nutrtion facts for a given food name from nutritionix apis
def get_nutrition_facts(food_name):
    print('Getting nutrition facts for food: ', food_name)

    if food_name == UNKNOWN_FOOD:
        return {
            "item_name": UNKNOWN_FOOD,
            "nf_calories": 0,
            "nf_total_fat": 0,
            "nf_serving_size_qty": 0,
            "nf_serving_size_unit": "serving"
        }

    request_headers = {
        "X-Mashape-Key": "m9TeetANyXmshi54UehLdicX1ph2p1yBBvBjsnKyqHgBwP8aZv",
        "Accept": "application/json"
    }
    url = "https://nutritionix-api.p.mashape.com/v1_1/search/{}?fields=item_name%2Cnf_calories%2Cnf_total_fat".format(food_name)

    response = requests.get(url, headers=request_headers)
    
    print(str(response))
    return response.hits[0].fields
