from __future__ import division

# 50/50 patterns
def odds(n):
    return [idx for idx in range(n) if idx % 2]


def evens(n):
    return [idx for idx in range(n) if not idx % 2]


def first_half(n):
    return range(0, n//2)


def second_half(n):
    return range(n//2, n)


def first_and_last_quarter(n):
    return range(0, n//2) + range(3*n//4, n)


# 70/30 patterns
def first_seventy(n):
    return range(0, 7*n//10)


# 90/10 patterns
def most(n):
    return range(0, 9*n//10)


# only last tree
def only_last(n):
    return [n-1]


pattern_dict = {'odds': odds,
                'evens': evens,
                'first_half': first_half,
                'second_half': second_half,
                'first_and_last_quarter': first_and_last_quarter,
                'first_seventy': first_seventy,
                'most': most,
                'only_last': only_last
                }