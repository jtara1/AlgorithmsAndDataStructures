import functools
from os.path import join, dirname
import json
import os
from src.timer import time_it


class MemoizeMakeChange:
    # file path to where __cache is serialized (str should be formatted)
    json_file_path = join(dirname(__file__), 'make_change_{denominations}.json')

    def __init__(self, func):
        """Save the output of calls to make_change func to save time when future
        calls are made to the func
        self.__cache is a 2D list where each row is a denomination
        and the column index is the amount of change needed

        e.g.: for denom = [1, 5, 10, 25], we need to get numb of coins for $0.06
        (change = 6), our self.__cache will be built to equal
         [[0, 1, 2, 3, 4, 0, 1],
          [0, 0, 0, 0, 0, 1, 1],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0]]
        take the column of values from column at index 6 and we get [1, 1, 0, 0]
        which means we need 1 penny, 1 nickle, 0 dimes, 0 quarters as the
        smallest amount of coins to make up 6 change in total

        Note: make_change func will determine a single column in self.__cache
        while this class will handle the caching, calling, and serialization

        Note: self.func references were refactor to self.__func for
        "private visibility" since the func,
        make_change = MemoizeMakeChange(make_change_no_memoization), was later
        wrapped with an object of the class src.timer.TimeIt which initially
        also had an attribute, self.func, which replaced this self.func attr
        of this class which in effect reverted
        make_change to make_change_no_memoization

        :param func: make_change function (func this object is wrapping)
        """
        self.__cache = None
        self.__func = func
        # this object now wraps the func
        functools.update_wrapper(self, func)

    def __call__(self, change, denominations):
        """Overloading () operator
        Attempts to load output if there is no self.__cache loaded yet

        :param change: amount of change
        :param denominations: list of denominations
        :return: self.__func(n, denominations) (# of coins of each denomination)
        :rtype: list of integers
        """
        if self.__cache is None:
            # load serialization of cached function calls
            self._deserialize(denominations)

        try:
            return [self.__cache[i][change] for i in range(len(denominations))]
        # we haven't cached values for this amount of change or larger amounts
        except IndexError:
            return self._extend_cache(change, denominations)
        # self.__cache is None or non-index-able type
        # (no self.__cache.__get__(val))
        except TypeError:
            self.__cache = [[] for _ in range(len(denominations))]
            return self.__call__(change, denominations)

    def _extend_cache(self, change, denominations):
        """Call self.__func(change, denominations)
        for change in range [n+1 to change+1)
        saving each self.__func output in column, change, of self.__cache
        Serializes self.__cache after all calls to self.__func complete

        :param change: amount of change (as integer)
        :param denominations: list of denominations of coins / bills from least
            to greatest
        :return: self.__func(change, denominations)
        :rtype: list of integers
        """
        for amount in range(len(self.__cache[0]), change + 1):
            coins = self.__func(amount, denominations)
            for index, coins_for_denom in enumerate(coins):
                self.__cache[index].append(coins_for_denom)

        self._serialize(denominations)
        return coins

    def _serialize(self, denominations):
        file_path = MemoizeMakeChange.json_file_path.format(
            denominations=denominations)
        with open(file_path, 'w') as file:
            json.dump(self.__cache, file)

    def _deserialize(self, denominations):
        file_path = MemoizeMakeChange.json_file_path.format(
            denominations=denominations)
        try:
            with open(file_path, 'r') as file:
                self.__cache = json.load(file)
        except (FileNotFoundError, IOError):  # there is no serialized __cache
            self.__cache = None

    @staticmethod
    def clear_cache(denominations):
        try:
            os.remove(MemoizeMakeChange.json_file_path.format(
                      denominations=denominations))
        except (FileNotFoundError, IOError, OSError):
            pass


def make_change_no_memoization(change, denominations):
    """Returns the smallest amount of coins of the given denomination to total
    the amount of change.

    e.g.: for n = 6, denominations = [1, 5, 10, 25]
    return [1, 1, 0, 0]

    :param change: amount of change (as integer)
    :param denominations: list of denominations of coins / bills from least
            to greatest
    :return: number of coins of each denomination
    :rtype: list of integers
    """
    def find_next_coin():
        # iterate from last to first
        for i in range(len(denominations) - 1, -1, -1):
            if total + denominations[i] <= change:
                return i
        raise Exception("no solution")

    total = 0
    coins = [0] * len(denominations)

    while total < change:
        index = find_next_coin()
        coins[index] += 1
        total += denominations[index]

    return coins


# memoized version of make_change_no_memoization
make_change = MemoizeMakeChange(make_change_no_memoization)
make_change.__name__ = "make_change"


if __name__ == '__main__':
    @time_it
    def test():
        denom = [1, 5, 10, 25]
        # print(make_change(76, denom))
        # print(make_change(24, denom))
        # print(make_change_no_memoization(76, denom))
        # print(make_change_no_memoization(24, denom))
        denom2 = denom + [100, 500, 1000, 2000]
        print(make_change_no_memoization(4683, denom2))
        print(type(make_change))
        print(type(make_change_no_memoization))
    test()