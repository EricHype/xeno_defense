from actors.squareFragment import SquareFragment


#class ExplodingSquare():
    #def __init__(center_x, center_y, rect_color, force_multiplier = 1.0):
def getExplodingSquareEntities(center_x, center_y, rect_color, fragment_size, force_multiplier = 1.0):
    entities = []

    #top left
    entities.append(SquareFragment(center_x - fragment_size, center_y - fragment_size, 
        fragment_size, rect_color, "left", 8 * force_multiplier, 6 * force_multiplier))
    #top right
    entities.append(SquareFragment(center_x, center_y - fragment_size, fragment_size, 
        rect_color, "right", 8 * force_multiplier, 3 * force_multiplier))
    #bottom left
    entities.append(SquareFragment(center_x - fragment_size, center_y, fragment_size, 
        rect_color, "left", 2 * force_multiplier, 6 * force_multiplier))
    #bottom right
    entities.append(SquareFragment(center_x, center_y, fragment_size, rect_color, 
        "right", 2 * force_multiplier, 3 * force_multiplier))

    return entities
