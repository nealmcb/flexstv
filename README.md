# flexstv

flexstv is a flexible implementation of the Single Transferrable Vote (STV) algorithm in Python by Lorenzo Losa.
Unlike most STV implementations, it allows tied rankings, prorating the vote for each candidate in
the tie by the number of candidates so-ranked which remain in each round.

License: GPLv3

## Prerequisites
Requires Python 3.

## Usage

    flexstv [-h] [-s SEATS] [-r] [-v VERBOSITY] cvr_file

The number of seats (winners) to assign defaults to 2
and the verbosity defaults to 2 (highest).

## Example

Reproduce the results in the example at Wikipedia:
[Single transferable vote](https://en.wikipedia.org/wiki/Single_transferable_vote)

    $ flexstv.py -s 3 -v 1 votes.csv
    Counting the votes...

    Total votes: 20
    Quota: 6
    Step 1. Chocolate (12.00); Orange (4.00); Pear (2.00); Strawberry (1.00); Sweets (1.00)
      Chocolate is selected.
    Step 2. Strawberry (5.00); Orange (4.00); Sweets (3.00); Pear (2.00)
      Pear loses.
    Step 3. Orange (6.00); Strawberry (5.00); Sweets (3.00)
      Orange is selected.
    Step 4. Strawberry (5.00); Sweets (3.00)
      Sweets loses.
    Step 5. Strawberry (8.00)
      Strawberry is selected.

Contest with some equal rankings:

    $ flexstv.py -s 2 -v 1 some-equal-rankings.csv
    Counting the votes...

    Total votes: 18
    Quota: 7
    Step 1. A (7.67); B (4.17); C (3.83); E (2.00); D (0.33)
      A is selected.
    Step 2. B (4.41); C (3.98); E (2.13); D (0.48)
      D loses.
    Step 3. B (4.80); C (4.02); E (2.17)
      E loses.
    Step 4. B (5.89); C (5.11)
      C loses.
    Step 5. B (11.00)
      B is selected.
