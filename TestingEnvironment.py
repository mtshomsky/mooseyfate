""" This module represents the testing framework used to
generate potential run scenarios for the framework"""

from random import random, randint
from WimpyHypothesis import WimpyHypothesis
from BraveHypothesis import BraveHypothesis

global COLOR_CATEGORY_1
global COLOR_CATEGORY_1_AGGRO
global COLOR_CATEGORY_2
global COLOR_CATEGORY_2_AGGRO

COLOR_CATEGORY_1 = 0.7
COLOR_CATEGORY_1_AGGRO = 0.6
COLOR_CATEGORY_2 = 1 - COLOR_CATEGORY_1
COLOR_CATEGORY_2_AGGRO = 0.05


def aggro_probability():
    p1 = COLOR_CATEGORY_1 * COLOR_CATEGORY_1_AGGRO
    p2 = COLOR_CATEGORY_2 * COLOR_CATEGORY_2_AGGRO
    return p1 + p2

def passive_probability():
    return 1 - aggro_probability()


class Monster(object):
    """Monster class encapsulates the aggressiveness and
    color. The aggressiveness should not be accessed and
    as such its name has been mangled """

    def __init__(self, aggressive, color, label):
        """Initializes the monster"""
        self._aggressive = aggressive
        self.color = color
        self.label = label

    def action(self, should_attack):
        """Act on the monster"""
        if not should_attack:
            return 0
        if self._aggressive:
            return -1
        return 1

def monster_generator(kind=False):

    if (kind):
        while True:
            yield Monster(1, color, 'A')


    """Provides a generator for monsters"""
    while True:
        color = random()
        if color <= COLOR_CATEGORY_1:
            if random() <= COLOR_CATEGORY_1_AGGRO:
                yield Monster(1, color, 'A')
            else:
                yield Monster(0, color, 'A')
        else:
            if random() <= COLOR_CATEGORY_2_AGGRO:
                yield Monster(1, color, 'B')
            else:
                yield Monster(0, color, 'B')



def run_tests(hypothesis, trials=100, called='hypothesis'):
    monster = monster_generator.next()

    score = 0.0
    max_score = 0.0
    fitness = 0.0


    for x in range(trials):
        print (called + ' fitness:' + str(fitness))

        monster = monster_generator.next()

        if monster._aggressive == 0:
            max_score += 1

        guess = hypothesis.get_guess(monster)
        outcome = monster.action(True)
        hypothesis.update(monster, guess, outcome)

        score += outcome

        fitness = hypothesis.fitness()

    print(called + ' Maximum Score: ' + str(max_score))
    print(called + ' Score        : ' + str(score))
    print(called + ' Success Rate : ' + str(score / max_score))
    print(called + ' ')
    print(called + ' True passive p-value : ' + str(passive_probability()))

def run_2tests(hypothesisA, hypothesisWimpy, trials=100, called='hypothesis'):
    monster = monster_generator.next()

    score = 0.0
    max_score = 0.0
    fitness = 0.0
    wimpy_fitness = 0.0


    for x in range(trials):
        print (called + ' brave fitness:' + str(fitness) + ' wimpy fitness:' +str(wimpy_fitness) )

        monster = monster_generator.next()

        if monster._aggressive == 0:
            max_score += 1

        guess = hypothesisA.get_guess(monster)
        outcome = monster.action(True)
        hypothesisA.update(monster, guess, outcome)
        hypothesisWimpy.update(monster, guess, outcome)

        score += outcome

        fitness = hypothesisA.fitness()
        wimpy_fitness = hypothesisWimpy.fitness()

    print(called + ' Maximum Score: ' + str(max_score))
    print(called + ' Score        : ' + str(score))
    print(called + ' Success Rate : ' + str(score / max_score))
    print(called + ' ')
    print(called + ' True passive p-value : ' + str(passive_probability()))


if __name__ == "__main__":
    monster_generator = monster_generator()

    """
    print('Exercise Generator ----------------')
    for x in range(10):
        monster = monster_generator.next()
        print(x)
        print(monster.label)
        print(monster._aggressive)
        print(monster.color)
        print('')
    """

    print('Run tests only on wimpy ----------------')
    wimpy = WimpyHypothesis()
    run_tests(wimpy, 10, 'Wimpy')

    print('Run tests only on brave ----------------')
    brave = BraveHypothesis()
    run_tests(brave, 10, 'Brave')

    print('Run 2tests only on brave versus wimpy ----------------')
    run_2tests(brave, wimpy, 10, 'Combined 2tests:')
