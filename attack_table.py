ROLL_SCALE = 1

HIT_SUPPRESSION = 100
BASE_MISS = (800 + HIT_SUPPRESSION) * ROLL_SCALE
BASE_DODGE = 650 * ROLL_SCALE + BASE_MISS
BASE_PARRY = 1400 * ROLL_SCALE + BASE_DODGE
BASE_GLANCE = 2400 * ROLL_SCALE + BASE_PARRY
BASE_CRIT = 0 * ROLL_SCALE + BASE_GLANCE
BASE_HIT = 4650 * ROLL_SCALE + BASE_CRIT

EXPERTISE_SOFT_CAP = 26
EXPERTISE_HARD_CAP = 56

MISS = 'miss'
DODGE = 'dodge'
PARRY = 'parry'
GLANCE = 'glance'
CRIT = 'crit'
HIT = 'hit'

BASE_ATTACK_TABLE = {'miss': BASE_MISS,
                     'dodge': BASE_DODGE,
                     'parry': BASE_PARRY,
                     'glance': BASE_GLANCE,
                     'crit': BASE_CRIT,
                     'hit': BASE_HIT}


def determine_roll_table_outcome(attack_table, roll):
    print(f'LOG: ROLL NUMBER {roll}')
    if attack_table['miss'] > 0 and roll <= attack_table['miss']:
        print('LOG: ROLLED MISS')
        return MISS
    if attack_table['dodge'] > 0 and roll <= attack_table['dodge']:
        print('LOG: ROLLED DODGE')
        return DODGE
    if attack_table['parry'] > 0 and roll <= attack_table['parry']:
        print('LOG: ROLLED PARRY')
        return PARRY
    if attack_table['glance'] > 0 and roll <= attack_table['glance']:
        print('LOG: ROLLED GLANCE')
        return GLANCE
    if attack_table['crit'] > 0 and roll <= attack_table['crit']:
        print('LOG: ROLLED CRIT')
        return CRIT
    if attack_table['hit'] > 0 and roll <= attack_table['hit']:
        print('LOG: ROLLED HIT')
        return HIT

def generate_new_attack_table(hit_chance, expertise, crit_chance):
    print(f'LOG: GENERATE ATTACK TABLE WITH hit_chance={hit_chance} converted to {hit_chance * 10 * ROLL_SCALE}')
    new_attack_table = BASE_ATTACK_TABLE.copy()
    dodge_reduction = calculate_dodge_reduction(expertise)
    parry_reduction = calculate_parry_reduction(expertise)
    crit_increase = calculate_crit_increase(crit_chance)

    new_miss = (BASE_MISS - int(hit_chance * 100 * ROLL_SCALE))

    new_dodge = (BASE_DODGE - dodge_reduction - BASE_MISS) + new_miss
    print(f'{new_dodge} = {BASE_DODGE} - {dodge_reduction} + {new_miss}')

    new_parry = (BASE_PARRY - parry_reduction - BASE_DODGE) + new_dodge

    new_glance = BASE_GLANCE + new_parry - BASE_PARRY

    new_crit = BASE_CRIT + crit_increase + new_glance - BASE_GLANCE
    print(f'new_crit {new_crit} = {BASE_CRIT} + {crit_increase} + {new_glance} - {BASE_GLANCE}')

    new_hit = BASE_HIT + new_crit - BASE_CRIT + int(hit_chance * 100 * ROLL_SCALE) + dodge_reduction + parry_reduction

    new_attack_table['miss'] = new_miss
    new_attack_table['dodge'] = new_dodge
    new_attack_table['parry'] = new_parry
    new_attack_table['glance'] = new_glance
    new_attack_table['crit'] = new_crit
    new_attack_table['hit'] = new_hit

    return new_attack_table


def calculate_crit_increase(crit_chance):
    return int(crit_chance * 100)


def calculate_dodge_reduction(expertise):
    if expertise < 0:
        print('ERROR: NEGATIVE EXPERTISE INVALID')
        exit()
    if expertise < EXPERTISE_SOFT_CAP:
        dodge_reduction = int(expertise) * 25
    elif expertise >= EXPERTISE_SOFT_CAP:
        dodge_reduction = 650

    return dodge_reduction * ROLL_SCALE


def calculate_parry_reduction(expertise):
    if expertise < 0:
        print('ERROR: NEGATIVE EXPERTISE INVALID')
        exit()
    if expertise < EXPERTISE_HARD_CAP:
        parry_reduction = int(expertise) * 25
    elif expertise >= EXPERTISE_HARD_CAP:
        parry_reduction = 1400

    return parry_reduction * ROLL_SCALE
