UNDEFINED = 0
BAD = 1
NOT_SURE = 2
GOOD = 3

COSTS = [0, 0, 1, 2, 5, 7, 3, 9, 10]


def without_undefined(val):
    return NOT_SURE if val == UNDEFINED else val


def calc_rating(first, second):
    possibility = min(without_undefined(first.possibility), without_undefined(second.possibility))
    rating = min(without_undefined(first.rating), without_undefined(second.rating))
    return COSTS[(possibility-1)*3 + rating-1]


def check_possibility(first, second):
    return (first.possibility != BAD) and (second.possibility != BAD)
