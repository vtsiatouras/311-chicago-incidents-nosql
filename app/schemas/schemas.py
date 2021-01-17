from enum import Enum


class TypeOfServiceRequest(str, Enum):
    abandoned_vehicle = 'ABANDONED_VEHICLE'
    alley_lights = 'ALLEY_LIGHTS'
    graffiti = 'GRAFFITI'
    garbage = 'GARBAGE_CART'
    pothole = 'POTHOLE'
    rodent_baiting = 'RODENT_BAITING'
    sanitation_violation = 'SANITATION_VIOLATION'
    street_one_light = 'STREET_ONE_LIGHT'
    street_all_lights = 'STREET_ALL_LIGHTS'
    tree_trims = 'TREE_TRIMS'
    tree_debris = 'TREE_DEBRIS'
