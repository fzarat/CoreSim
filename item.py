

ITEM_INVENTORY_TYPES = {1: 'head', 2: 'neck', 3: 'shoulders', 4: 'shirt', 5: 'chest', 6: 'waist', 7: 'legs', 8: 'feet',
                        9: 'wrists', 10: 'hands', 11: 'finger', 12: 'trinket', 13: '1h_weapon', 14: 'shield', 15: 'bow',
                        16: 'back', 17: '2h_weapon', 20: 'cloth_chest', 21: 'other_1h_weapon', 22: 'oh_weapon',
                        23: 'oh_item', 24: 'ammo', 25: 'thrown', 26: 'crossbow_gun_wand', 28: 'totem_idol_libram'}

ITEM_CLASSES = {2: 'weapon', 4: 'equipment'}

ITEM_SUBCLASSES_WEAPON = {2: 'bow', 7: '1h'}

ITEM_SUBCLASSES_EQUIPMENT = {0: 'none', 1: 'cloth', 2: 'leather', 3: 'mail', 4: 'plate'}

ITEM_STAT_TYPES_PRIMARY = {3: 'agility', 4: 'strength', 5: 'intellect', 6: 'spirit?', 7: 'stamina'}
ITEM_STAT_TYPES_SECONDARY = {31: 'hit_rating', 32: 'critical_strike_rating', 36: 'haste_rating', 37: 'expertise_rating'}

ITEM_SOCKET_COLORS = {1: 'meta', 2: 'red', 3: -1, 4: 'yellow', 5: -1, 6: -1, 7: -1, 8: 'blue'}

ITEM_SPELL_IDS = {39885: ('attack_power', 126),
                  44810: ('armor_penetration', 182),
                  15821: ('attack_power', 72),
                  40933: ('attack_power', 120),
                  42113: ('armor_penetration', 210),
                  42098: ('armor_penetration', 140),
                  15815: ('attack_power', 58),
                  40258: ('armor_penetration', 150),
                  40679: ('armor_penetration', 161),
                  15818: ('attack_power', 66),
                  15826: ('attack_power', 80),
                  45355: ('blackened_naaru_sliver_effect', 1),
                  45354: ('shard_of_contempt_effect', 1),
                  15810: ('attack_power', 44),
                  42095: ('armor_penetration', 175),
                  15806: ('attack_power', 34),
                  44983: ('armor_penetration', 231),
                  33782: ('attack_power', 108),
                  47524: ('cursed_vision_sense_demon_effect', 1),
                  30645: ('gas_cloud_tracking', 1),
                  40273: ('stealth_detection', 1),
                  12883: ('longsight', 1),
                  15817: ('attack_power', 64)}


class Item:
    def __init__(self, list_init_values):
        self.item_id = list_init_values['entry']
        self.item_type = ITEM_CLASSES[list_init_values['class']]
        if self.item_type == 'weapon':
            self.item_subtype = ITEM_SUBCLASSES_WEAPON[list_init_values['subclass']]
        elif self.item_type == 'equipment':
            self.item_subtype = ITEM_SUBCLASSES_EQUIPMENT[list_init_values['subclass']]
        self.name = list_init_values['name']
        self.item_quality = list_init_values['Quality']
        self.item_inventory_type = ITEM_INVENTORY_TYPES[list_init_values['InventoryType']]
        self.item_level = list_init_values['ItemLevel']

        spell_ids = []
        spell_ids.append(list_init_values['spellid_1'])
        spell_ids.append(list_init_values['spellid_2'])
        spell_ids.append(list_init_values['spellid_3'])
        spell_ids.append(list_init_values['spellid_4'])
        spell_ids.append(list_init_values['spellid_5'])

        # parse item stats
        stat_types = []
        stat_types.append(list_init_values['stat_type1'])
        stat_types.append(list_init_values['stat_type2'])
        stat_types.append(list_init_values['stat_type3'])
        stat_types.append(list_init_values['stat_type4'])
        stat_types.append(list_init_values['stat_type5'])
        stat_types.append(list_init_values['stat_type6'])
        stat_types.append(list_init_values['stat_type7'])
        stat_types.append(list_init_values['stat_type8'])
        stat_types.append(list_init_values['stat_type9'])
        stat_types.append(list_init_values['stat_type10'])


        stat_values = []
        stat_values.append(list_init_values['stat_value1'])
        stat_values.append(list_init_values['stat_value2'])
        stat_values.append(list_init_values['stat_value3'])
        stat_values.append(list_init_values['stat_value4'])
        stat_values.append(list_init_values['stat_value5'])
        stat_values.append(list_init_values['stat_value6'])
        stat_values.append(list_init_values['stat_value7'])
        stat_values.append(list_init_values['stat_value8'])
        stat_values.append(list_init_values['stat_value9'])
        stat_values.append(list_init_values['stat_value10'])

        self.translated_primaries = {}
        self.translated_secondaries = {}

        for n, my_type in enumerate(stat_types):
            if my_type in ITEM_STAT_TYPES_PRIMARY:
                # print("FOUND PRIMARY")
                self.translated_primaries[ITEM_STAT_TYPES_PRIMARY[my_type]] = stat_values[n]
            if my_type in ITEM_STAT_TYPES_SECONDARY:
                # print("FOUND SECONDARY")
                self.translated_secondaries[ITEM_STAT_TYPES_SECONDARY[my_type]] = stat_values[n]

            # print(my_type, stat_values[n])

        print(self.translated_primaries)
        print(self.translated_secondaries)

        self.translated_special = {}
        for my_spellid in spell_ids:
            if my_spellid > 0 and my_spellid in ITEM_SPELL_IDS:
                self.translated_special[ITEM_SPELL_IDS[my_spellid][0]] = ITEM_SPELL_IDS[my_spellid][1]
                print(ITEM_SPELL_IDS[my_spellid])
                print(self.translated_special)
            elif my_spellid > 0 and my_spellid not in ITEM_SPELL_IDS:
                print(f'ERROR: spell entry not found for ITEM_SPELL_ID={my_spellid}')
                exit()

    def print_item(self):
        print("LOG: PRINT ITEM")
        print(f'Item ID:{self.item_id}')
        print(f'Item Type:{self.item_type}')
        print(f'Item Subtype:{self.item_subtype}')
        print(f'Item Name:{self.name}')
        print(f'Item Quality:{self.item_quality}')
        print(f'Item Slot ID:{self.item_inventory_type}')
        print(f'iLvl:{self.item_level}')

        print(f'Primary Stats:{self.translated_primaries}')
        print(f'Secondary Stats:{self.translated_secondaries}')
        print(f'Special Stat:{self.translated_special}')
