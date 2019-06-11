# flexstv

flexstv is a flexible implementation of the Single Transferrable Vote (STV) algorithm in Python by Lorenzo Losa.
Unlike most STV implementations, it allows tied rankings, prorating the vote for each candidate in
the tie by the number of candidates so-ranked which remain in each round.

Licensed: GPLv3

## Prerequisites
Requires Python 3.

## Usage

    flexstv [-h] [-s SEATS] [-r] [-v VERBOSITY] cvr_file

The number of seats (winners) to assign defaults to 2
and the verbosity defaults to 2 (highest).

## Example

Reproduce the results in the example at
Single transferable vote - Wikipedia](https://en.wikipedia.org/wiki/Single_transferable_vote)

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
