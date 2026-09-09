""" route Public"""

def get_all_restaurants():
    return """renvoie la liste de tout les restaurants"""

def get_restaurants_by_id(restaurant_id: int):
    return """renvoie le restaurant correspondant à l'id"""

""" route réservée aux admins"""

def modify_restaurant(restaurant_id: int):
    return """modifie le restaurant correspondant à l'id"""

def modify_restaurant_status(restaurant_id: int):
    return """modifie le status du restaurant correspondant à l'id"""