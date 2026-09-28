import re

p = '/workspace/loop/variants/spell/character.py'
s = open(p).read()

old = """    def parse_spellcast_view(self):
        self.known_spells = dict()
        self.spell_fail_chance = dict()

        # TODO: parse for other spellcaster classes
        if self.role not in (self.HEALER,):
            return
"""
new = """    def parse_spellcast_view(self):
        # hypothesis: the wizard's attack spells are never used, so the wizard can only
        # grind xp with a quarterstaff; reading the cast menu (done at startup and on
        # every level up) makes the known attack spells available to combat.
        if self.role not in (self.HEALER, self.WIZARD):
            return
        known_spells, spell_fail_chance = {}, {}
"""
assert old in s
s = s.replace(old, new)

old = """                letter, spell_name, level, category, fail, retention = matches[0]
                assert len(letter) == 1, letter
                self.known_spells[spell_name] = letter
                self.spell_fail_chance[spell_name] = int(fail) / 100
        self.agent.step(A.Command.ESC)
"""
new = """                letter, spell_name, level, category, fail, retention = matches[0]
                assert len(letter) == 1, letter
                known_spells[spell_name] = letter
                spell_fail_chance[spell_name] = int(fail) / 100
        self.agent.step(A.Command.ESC)
        self.known_spells, self.spell_fail_chance = known_spells, spell_fail_chance

    def parse_spellcast_view_safe(self):
        # keep the previously known spells if the menu cannot be read: a wizard that
        # fails to open its cast menu must not kill the episode with an exception
        try:
            self.parse_spellcast_view()
        except BaseException:
            pass
"""
assert old in s
s = s.replace(old, new)

old = """    def update(self):
        if 'You feel feverish.' in self.agent.message:
            self.is_lycanthrope = True
        if 'You feel purified.' in self.agent.message:
            self.is_lyanthrope = False
"""
new = """    def update(self):
        if 'You feel feverish.' in self.agent.message:
            self.is_lycanthrope = True
        if 'You feel purified.' in self.agent.message:
            self.is_lyanthrope = False
        if self.role in (self.HEALER, self.WIZARD) and \\
                self.agent.blstats.experience_level != self.last_spellcast_level:
            # a new level adds a known spell, so the cast menu has to be read again
            self.last_spellcast_level = self.agent.blstats.experience_level
            self.parse_spellcast_view_safe()
"""
assert old in s
s = s.replace(old, new)

old = """        self.role = None
        self.alignment = None"""
new = """        self.role = None
        self.known_spells = dict()
        self.spell_fail_chance = dict()
        self.last_spellcast_level = None
        self.alignment = None"""
assert old in s
s = s.replace(old, new)
open(p, 'w').write(s)
print('character.py patched')
