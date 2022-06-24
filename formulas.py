
def calculate_miss_chance(target_level, character_level):
    if target_level - character_level < 3:
        miss_chance = 5 + (target_level - character_level) * .5
    else:
        hit_suppression = (target_level - character_level - 2)
        miss_chance = 5 + (target_level - character_level) + hit_suppression
    return miss_chance


def calculate_glance_chance(target_level, character_level):
    glance_chance = max(0, 6 + (target_level - character_level) * 6)


