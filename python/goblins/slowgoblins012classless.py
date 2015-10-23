#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
part of http://ThePythonGameBook.com
source code: https://github.com/horstjens/ThePythonGameBook/blob/master/python/goblins/slowgoblins012classless.py

Stinky and Grunty reloaded, without classes by Github user yipyip.

This does the same as slowgoblins013.py but:
  + works with python2 AND python3
  + does NOT use classes
 
See this video:

http://pyvideo.org/video/880/stop-writing-classes

for more information about working without classes in python
"""

####

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
import random as rand
import sys

if sys.version_info[0] < 3:
    text_t = unicode
    binary_t = str
else:
    xrange = range
    text_t = str
    binary_t = bytes

####


def roll_die(min_val=1, max_val=6):
    """Roll a die"""
    assert 0 < min_val < max_val, "No valid die!"
    return rand.randint(min_val, max_val)

####


def make_goblin(name, attack_points=6, defend_points=6, health=10):
    """Spawn a goblin."""
    return dict(name=name, attack_points=6, defend_points=6, health=health)

####


def is_dead(goblin):
    """Check goblin health."""
    return goblin['health'] <= 0

####


def report(goblin):
    """Verbose goblin."""
    items = (
        "{0}:".format(goblin['name']),
        "Attack={0}".format(goblin['attack_points']),
        "Defend={0}".format(goblin['defend_points']),
        "Health={0}".format(goblin['health'])
    )
    return ' '.join(items)

####


def combat(goblin_a, goblin_b, max_rounds=100, dice=roll_die):
    """Multiple strikes, selected per random.
    """
    comments = []
    a = goblin_a
    b = goblin_b
    for i in xrange(1, max_rounds + 1):
        a, b = rand.choice(((a, b), (b, a)))
        result = strike(a, b, dice)
        comments.append(report_strike_stats(i, a, b, *result))
        if any((is_dead(a), is_dead(b))):
            break

    return comments

####


def strike(attacker, defender, dice):
    """One strike."""
    attack = attacker['attack_points'] + dice()
    defend = defender['defend_points'] + dice()
    damage = 0

    if attack > defend:
        damage = attack - defend
        defender['health'] -= damage

    return attack, defend, damage

####


def report_strike_stats(round, a, b, attack, defend, damage):
    """Strike results."""
    succ = "{name_a}(H={ha}) wins against {name_b}(H={hb}) with damage {damage}."
    fail = "{name_a}(H={ha}) defends sucessfully against {name_b}(H={hb})."
    args = dict(
        name_a=a['name'],
        name_b=b['name'],
        damage=damage,
        ha=a['health'],
        hb=b['health']
    )
    result_form = (fail, succ)[attack > defend].format(**args)

    return "{0:3d}-< {1}".format(round, result_form)

####


def output(strings):
    """Message interface.
    """
    print("\n".join(strings))

####


def main(conf):
    """Main procedure.
    """
    if conf['seed']:
        rand.seed(conf['seed'])
    available_dice = {'standard': roll_die}

    stinky = make_goblin("Stinky")
    grunty = make_goblin("Grunty")

    output((report(stinky), report(grunty)))
    results = combat(stinky, grunty, dice=available_dice[conf['dice']])
    output(results)

    for goblin in (stinky, grunty):
        if is_dead(goblin):
            output(("{0} is dead!".format(goblin['name']), ))

    ####

CONFIG =\
{'seed': None,
  'dice': 'standard'
 }

if __name__ == '__main__':
    """Module entry point.
    """
    main(CONFIG)
