from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView

from sim_database import *
import sys

import mainwindow
from item import Item

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = mainwindow.Ui_MainWindow()

connection = create_server_connection("localhost", "simuser", "Simpw77!", "item_db")


def populate_summary_table():
    ui.summary_table.setRowCount(10)
    total_damage_name = QTableWidgetItem('Total Damage')
    total_damage_item = QTableWidgetItem(str(ui.simEngine.my_warr.total_damage))
    ui.summary_table.setItem(0, 0, total_damage_name)
    ui.summary_table.setItem(0, 1, total_damage_item)

def custom_setup():
    ui.simEngine.sim_complete.connect(lambda: ui.combatLog.populate_combat_log(ui.simEngine.my_warr.combat_log))
    ui.simEngine.sim_complete.connect(lambda: populate_summary_table())

    head_items = ["Coif of Alleria", "Crown of Anasterian", "Mayhem Projection Goggles", "Cursed Vision of Sargeras",
                  "Helm of the Illidari Shatterer", "Onslaught Battle-Helm"]
    neck_items = ["Hard Khorium Choker", "Clutch of Demise", "Choker of Endless Nightmares",
                  "Choker of Serrated Blades", "Pendant of the Perilous", "Telonicus's Pendant of Mayhem"]
    shoulders_items = ["Pauldrons of Berserking", "Demontooth Shoulderpads", "Mantle of the Golden Forest",
                       "Onslaught Shoulderblades", "Swiftsteel Shoulders"]
    back_items = ["Cloak of Unforgivable Sin", "Shadowmoon Destroyer's Drape", "Dory's Embrace", "Cloak of Darkness"]
    chest_items = ["Bladed Chaos Tunic", "Hard Khorium Battleplate", "Warharness of Reckless Fury",
                   "Onslaught Breastplate", "Midnight Chestguard", "Vengeful Gladiator's Plate Chestpiece"]
    wrists_items = ["Onslaught Bracers", "Deadly Cuffs", "Bindings of Lightning Reflexes", "Bracers of Eradication",
                    "Master Assassin Wristwraps", "Bladespire Warbands", "Furious Shackles", "Eternium Rage-shackles"]
    hands_items = ["Thalassian Ranger Gauntlets", "Gloves of Immortal Dusk", "Borderland Paingrips",
                   "Grips of Silent Justice", "Onslaught Gauntlets"]
    waist_items = ["Onslaught Belt", "Belt of One-Hundred Deaths", "Bladeangel's Money Belt", "Red Belt of Battle",
                   "Girdle of the Endless Pit", "Chain of Unleashed Rage"]
    legs_items = ["Felfury Legplates", "Leggings of the Immortal Night", "Leggings of Divine Retribution",
                  "Shady Dealer's Pantaloons", "Legguards of Endless Rage", "Onslaught Greaves"]
    feet_items = ["Onslaught Treads", "Dreadboots of the Legion", "Warboots of Obliteration", "Ironstriders of Urgency"]
    finger_items = ["Band of Ruinous Delight", "Hard Khorium Band", "Stormrage Signet Ring", "Angelista's Revenge",
                    "Signet of Primal Wrath", "Unstoppable Aggressor's Ring", "Band of Devastation",
                    "Band of the Ranger-General", "Band of the Eternal Champion"]
    trinket_items = ["Blackened Naaru Sliver", "Shard of Contempt", "Dragonspine Trophy", "Berserker's Call",
                     "Madness of the Betrayer", "Tsunami Talisman", "Bloodlust Brooch", "Hourglass of the Unraveller",
                     "Badge of the Swarmguard"]
    mh_items = ["Warglaive of Azzinoth (mainhand)", "Brutal Gladiator's Slicer", "Brutal Gladiator's Cleaver",
                "Muramasa",
                "Hand of the Deceiver", "Dragonstrike", "Blade of Infamy", "Talon of Azshara"]
    oh_items = ["Warglaive of Azzinoth (offhand)", "Brutal Gladiator's Slicer", "Brutal Gladiator's Cleaver",
                "Muramasa",
                "Mounting Vengeance", "Dragonscale-Encrusted Longblade", "Blade of Infamy"]
    ranged_items = ["Golden Bow of Quel\\\'Thalas", "Crossbow of Relentless Strikes", "Ancient Amani Longbow",
                    "Twisted Blades of Zarak", "Serpent Spine Longbow", "Barrel-Blade Longrifle",
                    "Sunfury Bow of the Phoenix"]

    ui.headComboBox.clear()
    ui.headComboBox.addItems(head_items)
    ui.neckComboBox.addItems(neck_items)
    ui.shouldersComboBox.addItems(shoulders_items)
    ui.backComboBox.addItems(back_items)
    ui.chestComboBox.addItems(chest_items)
    ui.wristsComboBox.addItems(wrists_items)
    ui.handsComboBox.addItems(hands_items)
    ui.waistComboBox.addItems(waist_items)
    ui.legsComboBox.addItems(legs_items)
    ui.feetComboBox.addItems(feet_items)
    ui.finger1ComboBox.addItems(finger_items)
    ui.finger2ComboBox.addItems(finger_items)
    ui.finger2ComboBox.setCurrentIndex(1)
    ui.trinket1ComboBox.addItems(trinket_items)
    ui.trinket2ComboBox.addItems(trinket_items)
    ui.trinket2ComboBox.setCurrentIndex(1)
    ui.mainWeaponComboBox.addItems(mh_items)
    ui.offHandComboBox.addItems(oh_items)
    ui.rangedComboBox.addItems(ranged_items)

    ui.summary_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

    ui.simEngine.my_warr.character_gear = init_item_reads()

    ui.simEngine.my_warr.gear_quantify()

    update_attributes_table()
    update_melee_stats_table()
    print('DEBUG: MY MELEE STATS: ', ui.simEngine.my_warr.melee_stats)
    custom_connects_setup()


def custom_connects_setup():
    ui.headComboBox.item_swap.connect(lambda: update_gear(ui.headComboBox.currentText()))
    ui.neckComboBox.item_swap.connect(lambda: update_gear(ui.neckComboBox.currentText()))
    ui.shouldersComboBox.item_swap.connect(lambda: update_gear(ui.shouldersComboBox.currentText()))
    ui.backComboBox.item_swap.connect(lambda: update_gear(ui.backComboBox.currentText()))
    ui.chestComboBox.item_swap.connect(lambda: update_gear(ui.chestComboBox.currentText()))
    ui.wristsComboBox.item_swap.connect(lambda: update_gear(ui.wristsComboBox.currentText()))
    ui.handsComboBox.item_swap.connect(lambda: update_gear(ui.handsComboBox.currentText()))
    ui.waistComboBox.item_swap.connect(lambda: update_gear(ui.waistComboBox.currentText()))
    ui.legsComboBox.item_swap.connect(lambda: update_gear(ui.legsComboBox.currentText()))
    ui.feetComboBox.item_swap.connect(lambda: update_gear(ui.feetComboBox.currentText()))
    ui.finger1ComboBox.item_swap.connect(lambda: update_gear(ui.finger1ComboBox.currentText()))
    ui.finger2ComboBox.item_swap.connect(lambda: update_gear(ui.finger2ComboBox.currentText()))
    ui.trinket1ComboBox.item_swap.connect(lambda: update_gear(ui.trinket1ComboBox.currentText()))
    ui.trinket2ComboBox.item_swap.connect(lambda: update_gear(ui.trinket2ComboBox.currentText()))
    ui.mainWeaponComboBox.item_swap.connect(lambda: update_gear(ui.mainWeaponComboBox.currentText()))
    ui.offHandComboBox.item_swap.connect(lambda: update_gear(ui.offHandComboBox.currentText()))
    ui.rangedComboBox.item_swap.connect(lambda: update_gear(ui.rangedComboBox.currentText()))




def update_attributes_table():
    ui.attributes_table.setColumnCount(1)
    ui.attributes_table.setItem(0, 0, QTableWidgetItem(str(ui.simEngine.my_warr.primary_stats['strength'])))
    ui.attributes_table.setItem(0, 1, QTableWidgetItem(str(ui.simEngine.my_warr.primary_stats['agility'])))
    ui.attributes_table.setItem(0, 2, QTableWidgetItem(str(ui.simEngine.my_warr.primary_stats['stamina'])))
    ui.attributes_table.setItem(0, 3, QTableWidgetItem(str(ui.simEngine.my_warr.primary_stats['intellect'])))
    ui.attributes_table.setItem(0, 4, QTableWidgetItem(str(ui.simEngine.my_warr.primary_stats['spirit'])))
    ui.attributes_table.setItem(0, 5, QTableWidgetItem(str(ui.simEngine.my_warr.primary_stats['armor'])))


def update_melee_stats_table():
    ui.melee_stats_table.setColumnCount(1)
    ui.melee_stats_table.setItem(0, 0, QTableWidgetItem(str('null')))
    ui.melee_stats_table.setItem(0, 1, QTableWidgetItem(str('null')))
    ui.melee_stats_table.setItem(0, 2, QTableWidgetItem(str(ui.simEngine.my_warr.melee_stats['attack_power'])))
    ui.melee_stats_table.setItem(0, 3, QTableWidgetItem(str(ui.simEngine.my_warr.melee_stats['hit_chance'])))
    ui.melee_stats_table.setItem(0, 4, QTableWidgetItem(str(ui.simEngine.my_warr.melee_stats['crit_chance'])))
    ui.melee_stats_table.setItem(0, 5, QTableWidgetItem(str(ui.simEngine.my_warr.melee_stats['expertise'])))
    ui.melee_stats_table.resizeColumnsToContents()


def init_item_reads():
    init_gear_dict = {'head': read_item(ui.headComboBox.currentText()),
                      'neck': read_item(ui.neckComboBox.currentText()),
                      'shoulders': read_item(ui.shouldersComboBox.currentText()),
                      'back': read_item(ui.backComboBox.currentText()),
                      'chest': read_item(ui.chestComboBox.currentText()),
                      'wrists': read_item(ui.wristsComboBox.currentText()),
                      'hands': read_item(ui.handsComboBox.currentText()),
                      'waist': read_item(ui.waistComboBox.currentText()),
                      'legs': read_item(ui.legsComboBox.currentText()),
                      'feet': read_item(ui.feetComboBox.currentText()),
                      'finger1': read_item(ui.finger1ComboBox.currentText()),
                      'finger2': read_item(ui.finger2ComboBox.currentText()),
                      'trinket1': read_item(ui.trinket1ComboBox.currentText()),
                      'trinket2': read_item(ui.trinket2ComboBox.currentText()),
                      'mainhand': read_item(ui.mainWeaponComboBox.currentText()),
                      'offhand': read_item(ui.offHandComboBox.currentText()),
                      'ranged': read_item(ui.rangedComboBox.currentText())}
    return init_gear_dict


def read_item(item_name):
    if item_name in ["item1", "item2", "item3", "item4", "item5"]:
        print("*--LOG: DEFAULT ITEM")
        return

    read_gear_query = f"""SELECT * FROM items WHERE name LIKE '{item_name}';"""
    query_result = read_query(connection, read_gear_query)

    if len(query_result) == 0:
        print(f'ERROR: ITEM WITH NAME [{item_name}] NOT FOUND')
        exit()

    elif len(query_result) > 1:
        print("\n\tMULTIPLE RESULTS")
        print('\t', query_result)
        return
    # column_query = """SELECT column_name FROM information_schema.columns WHERE TABLE_NAME='items';"""
    # column_query_result = read_query(connection, column_query)
    # print(f'*--LOG: init_read_gear({item_name})')
    # print(f'*--LOG: read_gear_query = {read_gear_query}')
    # print(f'*--LOG: query_result = {query_result}')

    # item_desc_list = []
    # for n, column in enumerate(column_query_result):
    #     item_desc_entry = {column[0]: query_result[0][n]}
    #     item_desc_list.append(item_desc_entry)
    #
    # print(item_desc_list)
    # return item_desc_list

    print('\n\t', query_result)
    my_item = Item(query_result[0])
    my_item.print_item()
    return my_item
    # for q_column in query_result[0]:
    # for column in enumerate(column_query_result):


def update_gear(new_item):
    print("*--LOG: UPDATE GEAR SIGNAL RECEIVED")
    updated_item = read_item(new_item)
    updated_item.print_item()
    ui.simEngine.my_warr.gear_unequip(updated_item.item_inventory_type)
    ui.simEngine.my_warr.gear_equip(updated_item)

    update_attributes_table()
    update_melee_stats_table()


ui.setupUi(MainWindow)

custom_setup()

MainWindow.show()
sys.exit(app.exec())
