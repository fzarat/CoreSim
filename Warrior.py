import Character as ch
import attack_table
import warrior_formulas as wrf
import simpy
import random

random.seed()

CAST = 'cast'

MISS = 'miss'
DODGE = 'dodge'
PARRY = 'parry'
GLANCE = 'glance'
CRIT = 'crit'
HIT = 'hit'


class Warrior(ch.Character):
    bt_prio = 1
    ww_prio = 2
    rage_conv = wrf.calculate_rage_conversion_value(70)

    total_damage = 0

    def __init__(self, length=120):
        ch.Character.__init__(self, 70)
        print(f'Initialize warrior subclass {self}')
        self.sim_length = length
        self.env = None
        self.gcd_resource = None
        self.rage_pool = None

    def register_glance(self, attack_damage, ability): # TODO: Implement Glancing Blows
        print(f'{self.env.now : <10} | {ability} glancing hit for {attack_damage} (NOT YET IMPLEMENTED)')
        self.append_data_entry(self.env.now, GLANCE, f'{ability} glancing hit (NOT YET IMPLEMENTED)', attack_damage)

        self.total_damage += attack_damage

        rage_from_auto = wrf.calculate_rage_generated(attack_damage, self.rage_conv, self.wep_speed,
                                                      wrf.calculate_hit_factor("mainhand", "normal"))
        self.rage_pool.put(rage_from_auto)
        print(f'{self.env.now : <10} | Generated {rage_from_auto} rage, new total rage={self.rage_pool.level}')

    def register_crit(self, attack_damage, ability):
        attack_damage *= 2
        print(f'{self.env.now : <10} | {ability} critical hit for {attack_damage} ({attack_damage / 2} bonus damage)')
        self.append_data_entry(self.env.now, CRIT, f'{ability} critical hit', attack_damage)

        self.total_damage += attack_damage

        rage_from_auto = wrf.calculate_rage_generated(attack_damage, self.rage_conv, self.wep_speed,
                                                      wrf.calculate_hit_factor("mainhand", "crit"))
        self.rage_pool.put(rage_from_auto)
        print(f'{self.env.now : <10} | Generated {rage_from_auto} rage, new total rage={self.rage_pool.level}')

    def register_hit(self, attack_damage, ability):
        print(f'{self.env.now : <10} | {ability} hits for {attack_damage}')
        self.append_data_entry(self.env.now, HIT, f'{ability} hit', attack_damage)

        self.total_damage += attack_damage

        rage_from_auto = wrf.calculate_rage_generated(attack_damage, self.rage_conv, self.wep_speed,
                                                      wrf.calculate_hit_factor("mainhand", "normal"))
        self.rage_pool.put(rage_from_auto)
        print(f'{self.env.now : <10} | Generated {rage_from_auto} rage, new total rage={self.rage_pool.level}')

    def auto_attack(self, l_end, t_end):
        print(f'\t{self.env.now : <10} | Cast auto-attack')
        self.append_data_entry(self.env.now, CAST, 'Cast auto-attack', 0)

        auto_attack_damage = wrf.calculate_auto_attack(wrf.calculate_base_damage(l_end, t_end),
                                                       self.melee_stats['attack_power'], self.wep_speed)

        outcome_roll = random.randint(1, 10000)
        my_outcome = attack_table.determine_roll_table_outcome(self.current_attack_table, outcome_roll)

        if my_outcome == HIT:
            self.register_hit(auto_attack_damage, 'auto-attack')

        elif my_outcome == CRIT:
            self.register_crit(auto_attack_damage, 'auto-attack')
        elif my_outcome == MISS:
            print(f'{self.env.now : <10} | Auto-attack MISSED')
            self.append_data_entry(self.env.now, MISS, 'auto MISSED', 0)

        elif my_outcome == DODGE:
            print(f'{self.env.now : <10} | Auto-attack DODGED')
            self.append_data_entry(self.env.now, DODGE, 'auto DODGED', 0)

        elif my_outcome == PARRY:
            print(f'{self.env.now : <10} | Auto-attack PARRIED')
            self.append_data_entry(self.env.now, PARRY, 'auto PARRIED', 0)

        elif my_outcome == GLANCE:
            self.register_glance(auto_attack_damage, 'auto-attack')

        yield self.env.timeout(self.wep_speed)
        self.env.process(self.auto_attack(l_end, t_end))

    def bloodthirst(self, attack_power):
        with self.gcd_resource.request(priority=self.bt_prio) as request:
            print(f'{self.env.now : <10} | Current rage before BT: {self.rage_pool.level}')
            print(f'\t{self.env.now : <10} | Bloodthirst request invoked')
            yield request
            print(f'\t{self.env.now : <10} | Open GCD, successful Bloodthirst, lock GCD')
            yield self.rage_pool.get(30.0)
            self.append_data_entry(self.env.now, CAST, 'Cast Bloodthirst', 0)

            bloodthirst_damage = wrf.calculate_bloodthirst_damage(attack_power)

            outcome_roll = random.randint(1, 10000)
            my_outcome = attack_table.determine_roll_table_outcome(self.current_attack_table, outcome_roll)

            if my_outcome == HIT:
                self.register_hit(bloodthirst_damage, 'bloodthirst')

            elif my_outcome == CRIT:
                self.register_crit(bloodthirst_damage, 'bloodthirst')

            elif my_outcome == MISS:
                print(f'{self.env.now : <10} | bloodthirst MISSED')
                self.append_data_entry(self.env.now, MISS, 'bloodthirst MISSED', 0)

            elif my_outcome == DODGE:
                print(f'{self.env.now : <10} | bloodthirst DODGED')
                self.append_data_entry(self.env.now, DODGE, 'bloodthirst DODGED', 0)

            elif my_outcome == PARRY:
                print(f'{self.env.now : <10} | bloodthirst PARRIED')
                self.append_data_entry(self.env.now, PARRY, 'bloodthirst PARRIED', 0)

            elif my_outcome == GLANCE:
                self.register_glance(bloodthirst_damage, 'bloodthirst')

            yield self.env.timeout(self.base_gcd)
        yield self.env.timeout(6)
        self.env.process(self.bloodthirst(attack_power))

    def whirlwind(self, l_end, t_end, attack_power):
        with self.gcd_resource.request(priority=self.ww_prio) as request:
            print(f'{self.env.now : <10} | Current rage before WW: {self.rage_pool.level}')
            print(f'\t{self.env.now : <10} | Whirlwind request invoked')
            yield request
            print(f'\t{self.env.now : <10} | Open GCD, successful Whirlwind, lock GCD')
            yield self.rage_pool.get(25.0)
            self.append_data_entry(self.env.now, CAST, 'Cast Whirlwind', 0)

            whirlwind_damage = wrf.calculate_whirlwind_damage(wrf.calculate_base_damage(l_end, t_end), attack_power,
                                                              self.norm_wep_speed)

            outcome_roll = random.randint(1, 10000)
            my_outcome = attack_table.determine_roll_table_outcome(self.current_attack_table, outcome_roll)

            if my_outcome == HIT:
                self.register_hit(whirlwind_damage, 'whirlwind')

            elif my_outcome == CRIT:
                self.register_crit(whirlwind_damage, 'whirlwind')

            elif my_outcome == MISS:
                print(f'{self.env.now : <10} | whirlwind MISSED')
                self.append_data_entry(self.env.now, MISS, 'whirlwind MISSED', 0)

            elif my_outcome == DODGE:
                print(f'{self.env.now : <10} | whirlwind DODGED')
                self.append_data_entry(self.env.now, DODGE, 'whirlwind DODGED', 0)

            elif my_outcome == PARRY:
                print(f'{self.env.now : <10} | whirlwind PARRIED')
                self.append_data_entry(self.env.now, PARRY, 'whirlwind PARRIED', 0)

            elif my_outcome == GLANCE:
                self.register_glance(whirlwind_damage, 'whirlwind')

            yield self.env.timeout(self.base_gcd)
        yield self.env.timeout(10)
        self.env.process(self.whirlwind(l_end, t_end, attack_power))

    def initialize_rotation(self):
        print(f'DEBUG: ATTACK_POWER={self.melee_stats}')
        self.env.process(self.auto_attack(182, 339))
        self.env.process(self.bloodthirst(self.melee_stats['attack_power']))
        self.env.process(self.whirlwind(182, 339, self.melee_stats['attack_power']))

    def initialize_env(self):
        self.total_damage = 0
        self.env = simpy.Environment()
        self.gcd_resource = simpy.PriorityResource(self.env, capacity=1)
        self.rage_pool = simpy.Container(self.env, init=0.0, capacity=100.0)

        print(f'{self.env.now : <10} | Current rage: {self.rage_pool.level}')
        self.initialize_rotation()
        self.env.run(self.sim_length)
        print(f'Total Damage: {self.total_damage}')
