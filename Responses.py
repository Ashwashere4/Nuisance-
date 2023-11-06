import numpy as np

fuckList = ["Oh wow, someone has a potty mouth!", "Oh? MMMM harder!!", 
                 "Do you kiss your mother with that mouth?", "Someone learned how to curse! Good job!"
]

killList = ["Waaaa, Waaa someone is acting like a big baby!", 
            "Do it bitch i'm tired of hearing you bitch and moan", "Life is worth living! (Said no one ever)"]


def fuckResponse():
    random = np.random.randint(len(fuckList))

    return fuckList[random]

def killResponse():
    random = np.random.randint(len(killList))

    return killList[random]