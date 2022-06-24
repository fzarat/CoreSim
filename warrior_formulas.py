
def calculate_base_damage(low_end, top_end):
    base_damage = (low_end + top_end) / 2
    return base_damage


def calculate_rage_conversion_value(level):
    return (.0091107836 * (level ** 2)) + (3.225598133 * level) + 4.2652911


def calculate_hit_factor(weapon_type, hit_type):
    if weapon_type == "mainhand":
        if hit_type == "normal":
            return 3.5
        elif hit_type == "crit":
            return 7.0
    elif weapon_type == "offhand":
        if hit_type == "normal":
            return 1.75
        elif hit_type == "crit":
            return 3.5


# original formula R = 15d/(4c) + (f*s)/2 <= 15d/c
def calculate_rage_generated(damage, rage_c_val, weapon_speed, hit_factor):
    rage_generated = (3.75 * damage / rage_c_val) + ((hit_factor * weapon_speed) / 2)
    return rage_generated


def calculate_oh_coefficient(dwield_spec):
    return 0.025 * dwield_spec + 0.5


def calculate_bloodthirst_damage(attack_power):
    damage = attack_power * .45
    return damage


def calculate_whirlwind_damage(base_damage, attack_power, normalized_speed):
    damage = base_damage + attack_power / 14 * normalized_speed
    return damage


def calculate_auto_attack(base_damage, attack_power, base_speed):
    damage = base_damage + (attack_power / 14) * base_speed
    return damage
