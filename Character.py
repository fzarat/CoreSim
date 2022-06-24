import math

import attack_table
from attack_table import BASE_ATTACK_TABLE

BASE_AP_ORC = 190
BASE_CRIT_ORC = 1.1418181818181818181818181818182
HIT_CONVERSION_FACTOR = 15.76923 # exact value unknown, approx 1.3^-1


class Character:
    race = "orc"
    level = 70

    primary_stats = {
        "strength": 148,
        "agility": 93,
        "stamina": 135,
        "intellect": 30,
        "spirit": 54,
        "armor": 0
    }

    melee_stats = {
        'attack_power': 486,
        'hit_chance': 0.0,
        'crit_chance': 3.96,
        'haste': 0.0,
        'armor_penetration': 0,
        'expertise': 0.0
    }

    secondary_stats = {'hit_rating': 0,
                       'critical_strike_rating': 0,
                       'haste_rating': 0,
                       'expertise_rating': 0}

    special_stats = {'attack_power': 0,
                     'armor_penetration': 0}

    current_attack_table = BASE_ATTACK_TABLE.copy()

    base_gcd = 1.5
    wep_speed = 2.7
    norm_wep_speed = 2.4

    character_gear = {}

    combat_log = []

    def __init__(self, level):
        print(f'Initialize character superclass {self} level: {level}')
        self.level = level

    def append_data_entry(self, time, event_type, description, result):
        minutes = math.floor(time / 60)
        seconds = int(time % 60)
        milliseconds = time % 1
        ms_formatted = int(milliseconds * 1000)
        c_time = f'{minutes:02}:{seconds:02}:{ms_formatted:03}'
        entry = {'time': c_time,
                 'event_type': event_type,
                 'description': description,
                 'result': result}
        self.combat_log.append(entry)

    def gear_unequip(self, item_slot):
        unequipped_item = self.character_gear[item_slot]
        self.character_gear[unequipped_item.item_inventory_type] = None

        quantified_primary_stats = {'agility': 0, 'strength': 0, 'intellect': 0, 'spirit': 0, 'stamina': 0}
        quantified_secondary_stats = {'hit_rating': 0, 'critical_strike_rating': 0, 'haste_rating': 0,
                                      'expertise_rating': 0}
        quantified_special_stats = {'attack_power': 0, 'armor_penetration': 0}
        for stat_name in quantified_primary_stats.keys():
            if stat_name in unequipped_item.translated_primaries.keys():
                quantified_primary_stats[stat_name] += unequipped_item.translated_primaries[stat_name]
        for stat_name in quantified_secondary_stats.keys():
            if stat_name in unequipped_item.translated_secondaries.keys():
                quantified_secondary_stats[stat_name] += unequipped_item.translated_secondaries[stat_name]
        for stat_name in quantified_special_stats.keys():
            if stat_name in unequipped_item.translated_special.keys():
                quantified_special_stats[stat_name] += unequipped_item.translated_special[stat_name]

        for stats in quantified_primary_stats.keys():
            self.primary_stats[stats] -= quantified_primary_stats[stats]
        for stats in quantified_secondary_stats.keys():
            self.secondary_stats[stats] -= quantified_secondary_stats[stats]
        for stats in quantified_special_stats.keys():
            self.special_stats[stats] -= quantified_special_stats[stats]

        self.update_melee_stats()
        # print('MY SPECIAL STATS', self.special_stats)
        # print(self.secondary_stats)
        # print(self.melee_stats)

    def gear_equip(self, equipped_item):
        self.character_gear[equipped_item.item_inventory_type] = equipped_item

        quantified_primary_stats = {'agility': 0, 'strength': 0, 'intellect': 0, 'spirit': 0, 'stamina': 0}
        quantified_secondary_stats = {'hit_rating': 0, 'critical_strike_rating': 0, 'haste_rating': 0,
                                      'expertise_rating': 0}
        quantified_special_stats = {'attack_power': 0, 'armor_penetration': 0}
        for stat_name in quantified_primary_stats.keys():
            if stat_name in equipped_item.translated_primaries.keys():
                quantified_primary_stats[stat_name] += equipped_item.translated_primaries[stat_name]
        for stat_name in quantified_secondary_stats.keys():
            if stat_name in equipped_item.translated_secondaries.keys():
                quantified_secondary_stats[stat_name] += equipped_item.translated_secondaries[stat_name]
        for stat_name in quantified_special_stats.keys():
            if stat_name in equipped_item.translated_special.keys():
                quantified_special_stats[stat_name] += equipped_item.translated_special[stat_name]

        for stats in quantified_primary_stats.keys():
            self.primary_stats[stats] += quantified_primary_stats[stats]
        for stats in quantified_secondary_stats.keys():
            self.secondary_stats[stats] += quantified_secondary_stats[stats]
        for stats in quantified_special_stats.keys():
            self.special_stats[stats] += quantified_special_stats[stats]

        self.update_melee_stats()
        # print('MY SPECIAL STATS', self.special_stats)
        # print(self.secondary_stats)
        # print(self.melee_stats)

    def gear_quantify(self):
        quantified_primary_stats = {'agility': 0, 'strength': 0, 'intellect': 0, 'spirit': 0, 'stamina': 0}
        quantified_secondary_stats = {'hit_rating': 0, 'critical_strike_rating': 0, 'haste_rating': 0,
                                      'expertise_rating': 0}
        quantified_special_stats = {'attack_power': 0, 'armor_penetration': 0}

        for gear_item_slot in self.character_gear.keys():
            gear_item = self.character_gear[gear_item_slot]
            gear_item.print_item()
            for stat_name in quantified_primary_stats.keys():
                if stat_name in gear_item.translated_primaries.keys():
                    quantified_primary_stats[stat_name] += gear_item.translated_primaries[stat_name]
            for stat_name in quantified_secondary_stats.keys():
                if stat_name in gear_item.translated_secondaries.keys():
                    quantified_secondary_stats[stat_name] += gear_item.translated_secondaries[stat_name]
            for stat_name in quantified_special_stats.keys():
                if stat_name in gear_item.translated_special.keys():
                    quantified_special_stats[stat_name] += gear_item.translated_special[stat_name]

        for stats in quantified_primary_stats.keys():
            self.primary_stats[stats] += quantified_primary_stats[stats]
        for stats in quantified_secondary_stats.keys():
            self.secondary_stats[stats] += quantified_secondary_stats[stats]
        for stats in quantified_special_stats.keys():
            self.special_stats[stats] += quantified_special_stats[stats]

        self.update_melee_stats()
        # print('MY SPECIAL STATS', self.special_stats)
        # print(self.secondary_stats)
        # print(self.melee_stats)

    def update_melee_stats(self):
        self.update_attack_power()
        self.update_armor_penetration()
        self.update_hit_chance()
        self.update_expertise()
        self.update_critical_chance()
        self.update_haste()
        self.current_attack_table = attack_table.generate_new_attack_table(self.melee_stats['hit_chance'],
                                                                           self.melee_stats['expertise'],
                                                                           self.melee_stats['crit_chance'])
        print(f'LOG: BASE ATTACK TABLE={BASE_ATTACK_TABLE}')
        print(f'LOG: CURRENT ATTACK TABLE={self.current_attack_table}')

    def update_attack_power(self):
        self.melee_stats['attack_power'] = (BASE_AP_ORC
                                            + (self.primary_stats['strength'] * 2)
                                            + self.special_stats['attack_power'])

    def update_armor_penetration(self):
        self.melee_stats['armor_penetration'] = self.special_stats['armor_penetration']

    def update_critical_chance(self):
        self.melee_stats['crit_chance'] = (BASE_CRIT_ORC
                                           + (self.primary_stats['agility'] / 33)
                                           + (self.secondary_stats['critical_strike_rating'] / 22.1))

    def update_hit_chance(self):
        print('\n\n\t UPDATED HIT \n\n')
        self.melee_stats['hit_chance'] = (float(self.secondary_stats['hit_rating']) / HIT_CONVERSION_FACTOR)

    def update_expertise(self):
        self.melee_stats['expertise'] = (self.secondary_stats['expertise_rating'] / 3.9423)

    def update_haste(self):
        self.melee_stats['haste'] = (self.secondary_stats['haste_rating'] / 15.8)
