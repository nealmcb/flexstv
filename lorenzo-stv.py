#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Fractions are used in order to avoid rounding errors.

Usage:
...
"""

import csv
import itertools
import functools
from fractions import Fraction

class Vote:
    # weigth = 1.
    # ranking = []
    def __init__(self, *ranking, **kwargs):
        self.weigth = Fraction(1)
        self.name = kwargs.get('name')
        self.ranking = []
        for r in ranking:
            if isinstance(r, str):
                self.ranking.append([r])
            elif isinstance(r, (list, tuple)):
                self.ranking.append(list(r))
            else:
                raise ValueError

    def __repr__(self):
        assert type(self.weigth) is Fraction
        if self.ranking:
            return '<Vote with weigth %.2f: %s>' % (self.weigth,
                '; '.join("%d. %s" % (i+1, ', '.join(self.ranking[i]))
                    for i in range(len(self.ranking))))
        else:
            return '<empty vote>'

    def describe(self):
        assert type(self.weigth) is Fraction
        if self.ranking:
            if self.name:
                return '[%s; weigth %.2f] %s' % (self.name, self.weigth,
                        '; '.join("%d. %s" % (i+1, ', '.join(self.ranking[i]))
                                  for i in range(len(self.ranking))))
            else:
                return '[weigth %.2f] %s' % (self.weigth,
                        '; '.join("%d. %s" % (i+1, ', '.join(self.ranking[i]))
                                  for i in range(len(self.ranking))))
        else:
            return '<empty vote>'

    def candidates(self):
        assert type(self.weigth) is Fraction
        return functools.reduce(list.__add__, self.ranking, [])

    def remove(self, candidate, lighten=None):
        assert type(self.weigth) is Fraction
        # questa prima condizione gestisce il caso di un candidato vincente
        if lighten is not None and candidate in self.ranking[0]:
            # lighten should be a Fraction
            assert type(lighten) is Fraction
            self.weigth *= 1 -  lighten / len(self.ranking[0])
        for r in self.ranking:
            if candidate in r:
                r.remove(candidate)
        if [] in self.ranking:
            self.ranking.remove([])


class Election:
    # candidates = list of str
    # votes = list of votes (instances of Vote)
    # quota = float
    # seats = int
    # quota = int
    # elected = list of str
    # notelected = list of str
    def __init__(self, candidates, seats=1):
        self.seats = seats
        self.candidates = list(candidates)
        self.votes = []
        self.elected = []
        self.notelected = []


    def __repr__(self):
        return ("Election with %d candidates, %d seats and %d votes." %
            (len(self.candidates), self.seats, len(self.votes)))

    def print_status(self):
        current = list(self.count_current_votes().items())
        current.sort(key=lambda x: x[1], reverse=True)
        return '; '.join('%s (%.2f)' % x for x in current)

    def print_votes(self):
        current = '\n'.join(vote.describe() for vote in self.votes)
        return current

    def validate(self, vote):
        # validate modifica vote
        if not set(vote.candidates()).issubset(self.candidates):
            return False
        others = list(set(self.candidates).difference(vote.candidates()))
        if others:
            vote.ranking.append(others)
        return True

    def add(self, vote):
        if self.validate(vote):
            self.votes.append(vote)
        else:
            raise ValueError

    def count_current_votes(self):
        candidates = {c: Fraction(0) for c in self.candidates}
        for vote in self.votes:
            for c in vote.ranking[0]: # TODO gestire la fine
                candidates[c] += vote.weigth / len(vote.ranking[0])
        return candidates

    def step(self, verbose=True):
        current_votes = self.count_current_votes()
        # winners
        if max(current_votes.values()) >= self.quota:
            maxvotes = max(current_votes.values())
            assert type(maxvotes) is Fraction
            lighten = self.quota / maxvotes
            mostvoted = [c for c in current_votes if current_votes[c] == maxvotes]
            for candidate in mostvoted:
                if verbose:
                    print("  %s is selected." % candidate)
                for vote in self.votes:
                    vote.remove(candidate, lighten=lighten)
                self.candidates.remove(candidate)
                self.elected.append(candidate)
        # losers
        else:
            minvotes = min(current_votes.values())
            leastvoted = [c for c in current_votes if current_votes[c] == minvotes]
            self.notelected += leastvoted
            for candidate in leastvoted:
                if verbose:
                    print("  %s loses." % candidate)
                for vote in self.votes:
                    vote.remove(candidate)
                self.candidates.remove(candidate)
            if (verbose
                  and not self.candidates
                  and len(self.elected) < self.seats):
                print("\nSTALEMATE")

    # verbosity=0: quiet
    # verbosity=1: only the result of each step
    # verbosity=2: votes in each step
    def count(self, verbosity=2):
        self.votes.sort(key=lambda x: x.name)
        # Droop quota
        self.quota = len(self.votes) // (self.seats + 1) + 1
        assert type(self.quota) is int
        if verbosity:
            print('Counting the votes...')
            print()
            print('Total votes: %d' % len(self.votes))
            print("Quota: %d" % self.quota)
        for i in itertools.count(1):
            if verbosity == 1:
                print('Step %d. %s' % (i, self.print_status()))
            elif verbosity == 2:
                print('\nSTEP %d' % i)
                print('Votes:')
                print(self.print_votes())
                print('  Sums: %s' % self.print_status())
            self.step(verbose=(verbosity>0))
            if len(self.elected) >= self.seats or not self.candidates:
                return self.elected

def read_csv(filename):
    with open(filename) as fp:
        csvin = csv.reader(fp)
        header = next(csvin)
        candidates = [x.strip() for x in header[1:]]
        votes = {}
        for row in csvin:
            key = row[0].strip()
            vote = [(int(y), x) for x, y in zip(candidates, row[1:]) if y]
            if not vote:
                continue
            vote.sort()
            votes[key] = [[z[1] for z in y[1]]
                for y in itertools.groupby(vote, lambda x: x[0])]
    return candidates, votes

if __name__ == '__main__':
    candidates, votes = read_csv('votes.csv')

    asbs = Election(candidates, seats=2)

    for x in votes:
        asbs.add(Vote(*votes[x], name=x))

    asbs.count()
