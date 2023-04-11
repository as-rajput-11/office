import random


def get_anon_name():
    return 'AnonUser' + str(random.randint(10000, 99999))


def get_random_rgba():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)
