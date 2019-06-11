# flexstv

flexstv is a flexible implementation of the Single Transferrable Vote (STV) algorithm in Python by Lorenzo Losa.
Unlike most STV implementations, it allows tied rankings, prorating the vote for each candidate in
the tie by the number of candidates so-ranked which remain in each round.

Licensed: GPLv3

## Prerequisites
Requires Python 3.

## Usage example 

    flexstv.py votes.csv
