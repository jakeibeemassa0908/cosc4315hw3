from infinitearithmetic._bigint import (BigInt, add, fromint, fromstring, lshift, tostring)


def test_add():
    # Adds BigInt nodesize 1
    term = BigInt([1, 5, 5], 1)
    observed = add(term, term)
    assert(observed == BigInt([2, 0, 1, 1], 1))

    # Adds BigInt nodesize 5
    term = BigInt([55554, 3], 5)
    observed = add(term, term)
    assert(observed == BigInt([11108, 7], 5))

    # Adds BigInt nodesize 10
    term = BigInt([1234567891, 575], 10)
    observed = add(term, term)
    assert(observed == BigInt([2469135782, 1150], 10))


def test_fromint():
    # Ensures expression equality
    assert(fromint(100, 1) == fromstring('100', 1))


def test_fromstring():
    # Converts with nodesize of 1
    assert(fromstring('500', 1) == BigInt([0, 0, 5], 1))

    # Converts with nodesize of 2
    assert(fromstring('545', 2) == BigInt([45, 5], 2))

    # Converts with nodesize of 5
    assert(fromstring('123456', 5) == BigInt([23456, 1], 5))

    # Converts with nodesize of 10
    assert(fromstring('59832345678901', 10) == BigInt([2345678901, 5983], 10))


def test_lshift():
    # Shifts nodesize 1 to the left
    assert(lshift(fromint(123, 1), 2) == fromint(12300, 1))

    # Shifts nodesize 10 to the left
    assert(lshift(fromint(123, 10), 1) == fromint(1230000000000, 10))


def test_tostring():
    # Prints out zero bigint
    assert(tostring(fromint(0, 1)) == '0')

    # Prints out non zero bigint
    assert(tostring(fromint(200, 1)) == '200')

    # Prints out large number bigint
    assert(tostring(fromint(139410928029381029300, 10)) == '139410928029381029300')